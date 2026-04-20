"""Hybrid anomaly detection pipeline combining LSTM and Isolation Forest."""
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path


class HybridAnomalyDetector:
    """
    Combines LSTM and Isolation Forest for robust anomaly detection.
    - LSTM: Detects sequential anomalies (unexpected event transitions)
    - Isolation Forest: Detects statistical anomalies (unusual frequencies)
    """

    def __init__(
        self,
        lstm_model=None,
        if_model=None,
        lstm_weight: float = 0.5,
        if_weight: float = 0.5
    ):
        """
        Initialize hybrid detector.
        
        Args:
            lstm_model: Trained LSTM model
            if_model: Trained Isolation Forest model
            lstm_weight: Weight for LSTM scores
            if_weight: Weight for Isolation Forest scores
        """
        self.lstm_model = lstm_model
        self.if_model = if_model
        self.lstm_weight = lstm_weight
        self.if_weight = if_weight

    def detect_anomalies(
        self,
        sequences: List[np.ndarray],
        features: np.ndarray
    ) -> Tuple[np.ndarray, Dict]:
        """
        Detect anomalies using hybrid approach.
        
        Args:
            sequences: List of event sequences
            features: Feature matrix for Isolation Forest
            
        Returns:
            Tuple of (anomaly_scores, detection_results)
        """
        lstm_scores = np.zeros(len(sequences))
        if_scores = np.zeros(len(sequences))

        # LSTM scores
        if self.lstm_model:
            for i, seq in enumerate(sequences):
                lstm_scores[i] = self.lstm_model.compute_anomaly_score(seq)

        # Isolation Forest scores
        if self.if_model:
            if_scores = self.if_model.get_anomaly_scores(features)

        # Combine scores
        hybrid_scores = (
            self.lstm_weight * lstm_scores +
            self.if_weight * if_scores
        )

        return hybrid_scores, {
            'lstm_scores': lstm_scores,
            'if_scores': if_scores,
            'hybrid_scores': hybrid_scores
        }

    def classify_anomalies(
        self,
        scores: np.ndarray,
        threshold: float = 0.5
    ) -> np.ndarray:
        """
        Classify scores as anomaly or normal.
        
        Args:
            scores: Anomaly scores
            threshold: Classification threshold
            
        Returns:
            Binary labels (1 = anomaly, 0 = normal)
        """
        return (scores >= threshold).astype(int)

    def get_detection_report(
        self,
        sequences: List[np.ndarray],
        features: np.ndarray,
        true_labels: np.ndarray = None,
        threshold: float = 0.5
    ) -> Dict:
        """
        Generate comprehensive detection report.
        
        Args:
            sequences: Event sequences
            features: Feature matrix
            true_labels: Ground truth labels (optional)
            threshold: Anomaly threshold
            
        Returns:
            Dictionary with detection results and metrics
        """
        scores, score_details = self.detect_anomalies(sequences, features)
        predictions = self.classify_anomalies(scores, threshold)

        report = {
            'total_samples': len(sequences),
            'anomalies_detected': int(np.sum(predictions)),
            'normal_detected': len(sequences) - int(np.sum(predictions)),
            'anomaly_rate': float(np.mean(predictions)),
            'scores': scores.tolist(),
            'predictions': predictions.tolist(),
            'score_details': {
                'lstm_scores': score_details['lstm_scores'].tolist(),
                'if_scores': score_details['if_scores'].tolist()
            }
        }

        # Add metrics if ground truth available
        if true_labels is not None:
            from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

            report['metrics'] = {
                'precision': float(precision_score(true_labels, predictions, zero_division=0)),
                'recall': float(recall_score(true_labels, predictions, zero_division=0)),
                'f1_score': float(f1_score(true_labels, predictions, zero_division=0))
            }

            cm = confusion_matrix(true_labels, predictions)
            report['confusion_matrix'] = cm.tolist()

        return report

    def explain_detection(
        self,
        sequence: np.ndarray,
        features: np.ndarray,
        threshold: float = 0.5
    ) -> Dict:
        """
        Provide explanation for detection decision.
        
        Args:
            sequence: Single event sequence
            features: Feature vector
            threshold: Anomaly threshold
            
        Returns:
            Explanation dictionary
        """
        # Compute both scores
        lstm_score = self.lstm_model.compute_anomaly_score(sequence) if self.lstm_model else 0
        if_score = self.if_model.get_anomaly_scores(features.reshape(1, -1))[0] if self.if_model else 0

        hybrid_score = (self.lstm_weight * lstm_score + self.if_weight * if_score)
        is_anomaly = hybrid_score >= threshold

        explanation = {
            'is_anomaly': bool(is_anomaly),
            'hybrid_score': float(hybrid_score),
            'threshold': threshold,
            'lstm': {
                'score': float(lstm_score),
                'interpretation': 'Unusual event transitions' if lstm_score > 0.7 else 'Normal transitions'
            },
            'isolation_forest': {
                'score': float(if_score),
                'interpretation': 'Unusual event frequencies' if if_score > 0.7 else 'Normal frequencies'
            }
        }

        return explanation
