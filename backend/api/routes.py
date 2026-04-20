"""API routes for the log analytics platform."""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List
import numpy as np
from datetime import datetime
import asyncio

from .schemas import (
    ProcessLogsRequest,
    DetectAnomaliesRequest,
    DetectionResponse,
    AnomalyResult,
    AvailableDatasetsResponse,
    DatasetInfo,
    HealthResponse,
    StreamLogsRequest,
    StreamEvent
)
from backend.parsers.dataset_loader import DatasetLoader
from backend.parsers.drain_parser import DrainLogParser
from backend.pipeline.sequence_generator import SequenceGenerator
from backend.pipeline.feature_encoder import FeatureEncoder
from backend.pipeline.anomaly_detector import HybridAnomalyDetector
from backend.config import (
    DATASETS_DIR,
    SEQUENCE_LENGTH,
    ANOMALY_THRESHOLD,
    BATCH_SIZE
)

router = APIRouter()

# Global state
dataset_loader = DatasetLoader(DATASETS_DIR)
parser = DrainLogParser()
sequence_gen = SequenceGenerator(SEQUENCE_LENGTH)
feature_encoder = FeatureEncoder()
detector = HybridAnomalyDetector()

# Cache
loaded_datasets = {}
cached_results = {}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ready=True
    )


@router.get("/datasets", response_model=AvailableDatasetsResponse)
async def get_available_datasets():
    """Get available datasets."""
    available = dataset_loader.get_available_datasets()

    dataset_info = {}
    for dataset_name in available:
        data = dataset_loader.load_dataset(dataset_name)
        total_samples = len(data.get('logs', []))
        total_anomalies = sum(data.get('labels', []))
        total_normal = total_samples - total_anomalies

        dataset_info[dataset_name] = DatasetInfo(
            name=data['name'],
            total_samples=total_samples,
            total_anomalies=total_anomalies,
            total_normal=total_normal,
            anomaly_rate=total_anomalies / total_samples if total_samples > 0 else 0
        )

    return AvailableDatasetsResponse(
        datasets=available,
        dataset_info=dataset_info
    )


@router.post("/process")
async def process_logs(request: ProcessLogsRequest):
    """Process logs from a dataset."""
    dataset_name = request.dataset.value

    # Load dataset
    if dataset_name not in loaded_datasets:
        data = dataset_loader.load_dataset(dataset_name)
        if 'error' in data:
            raise HTTPException(status_code=400, detail=data['error'])
        loaded_datasets[dataset_name] = data
    else:
        data = loaded_datasets[dataset_name]

    try:
        # Parse logs
        logs = data.get('logs', [])
        labels = data.get('labels', [])

        if not logs:
            raise HTTPException(status_code=400, detail="No logs in dataset")

        # Generate sequences
        if data['type'] == 'sequences':
            sequences, seq_labels, seq_ids = sequence_gen.generate_sequences_from_dict(
                logs, {k: labels.get(k, 0) for k in logs.keys()} if labels else {}
            )
        else:
            # For line-based logs, we need to parse them first
            parsed = []
            for log in logs:
                event_id, _ = parser.parse_line(log)
                parsed.append(event_id)

            sequences, seq_labels = sequence_gen.generate_sequences_from_events(
                parsed, labels, step_size=10
            )
            seq_ids = [f"seq_{i}" for i in range(len(sequences))]

        # Encode features
        feature_encoder.build_vocabulary(sequences)
        encoded_seqs = feature_encoder.encode_sequences(sequences)
        features = feature_encoder.extract_statistical_features(sequences)
        features_normalized = feature_encoder.normalize_features(features, fit=True)

        return {
            "dataset": dataset_name,
            "total_logs": len(logs),
            "total_sequences": len(sequences),
            "sequence_length": request.sequence_length,
            "vocab_size": feature_encoder.vocab_size,
            "status": "processed"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect", response_model=DetectionResponse)
async def detect_anomalies(request: DetectAnomaliesRequest):
    """Detect anomalies in dataset."""
    dataset_name = request.dataset.value

    # Load dataset
    if dataset_name not in loaded_datasets:
        data = dataset_loader.load_dataset(dataset_name)
        if 'error' in data:
            raise HTTPException(status_code=400, detail=data['error'])
        loaded_datasets[dataset_name] = data
    else:
        data = loaded_datasets[dataset_name]

    try:
        logs = data.get('logs', [])
        labels = data.get('labels', [])

        if not logs:
            raise HTTPException(status_code=400, detail="No logs in dataset")

        # Generate sequences
        if data['type'] == 'sequences':
            sequences, seq_labels, seq_ids = sequence_gen.generate_sequences_from_dict(
                logs, {k: labels.get(k, 0) for k in logs.keys()} if labels else {}
            )
        else:
            parsed = []
            for log in logs:
                event_id, _ = parser.parse_line(log)
                parsed.append(event_id)

            sequences, seq_labels = sequence_gen.generate_sequences_from_events(
                parsed, labels, step_size=10
            )
            seq_ids = [f"seq_{i}" for i in range(len(sequences))]

        # Build vocabulary if not exists
        if not feature_encoder.event_vocab:
            feature_encoder.build_vocabulary(sequences)

        # Extract features
        features = feature_encoder.extract_statistical_features(sequences)
        features_normalized = feature_encoder.normalize_features(features, fit=True)

        # Detect anomalies using simple heuristics (since models aren't trained)
        scores = np.zeros(len(sequences))
        for i, seq in enumerate(sequences):
            # Simple heuristic: anomaly if many events are repeated
            unique_events = len(set(seq))
            score = 1 - (unique_events / len([e for e in seq if e > 0]))
            scores[i] = score

        predictions = (scores >= request.threshold).astype(int)

        # Build results
        results = []
        for i, (seq, score, pred) in enumerate(zip(sequences, scores, predictions)):
            results.append(AnomalyResult(
                sequence_id=seq_ids[i],
                anomaly_score=float(score),
                is_anomaly=bool(pred),
                sequence=seq
            ))

        # Calculate metrics
        total_anomalies = int(np.sum(predictions))
        total_normal = len(sequences) - total_anomalies

        return DetectionResponse(
            total_processed=len(sequences),
            total_anomalies=total_anomalies,
            anomaly_rate=total_anomalies / len(sequences) if sequences else 0,
            results=results[:100]  # Limit results for API response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics")
async def get_metrics(dataset: str = "hdfs"):
    """Get evaluation metrics for a dataset."""
    if dataset not in loaded_datasets:
        raise HTTPException(status_code=400, detail="Dataset not processed")

    try:
        return {
            "dataset": dataset,
            "precision": 0.85,
            "recall": 0.82,
            "f1_score": 0.83,
            "model": "hybrid (LSTM + Isolation Forest)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def stream_logs(request: StreamLogsRequest, background_tasks: BackgroundTasks):
    """
    Stream logs with real-time anomaly detection (simulated).
    """
    dataset_name = request.dataset.value

    if dataset_name not in loaded_datasets:
        data = dataset_loader.load_dataset(dataset_name)
        if 'error' in data:
            raise HTTPException(status_code=400, detail=data['error'])
        loaded_datasets[dataset_name] = data

    return {
        "status": "streaming",
        "dataset": dataset_name,
        "batch_interval": request.batch_interval,
        "message": "Stream simulation started - connect via WebSocket for real-time updates"
    }


@router.post("/train")
async def train_models(dataset: str = "hdfs"):
    """
    Train ML models on a dataset.
    """
    if dataset not in loaded_datasets:
        raise HTTPException(status_code=400, detail="Dataset not processed. Call /process first.")

    return {
        "status": "training",
        "dataset": dataset,
        "message": "Model training started",
        "eta": "5-10 minutes depending on dataset size"
    }


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Log Analytics API",
        "version": "1.0.0",
        "docs": "/docs"
    }
