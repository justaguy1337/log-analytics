"""Pydantic models for API schemas."""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class DatasetEnum(str, Enum):
    """Available datasets."""
    HDFS = "hdfs"
    BGL = "bgl"
    OPENSTACK = "openstack"


class LogEntry(BaseModel):
    """Single log entry."""
    timestamp: Optional[str] = None
    event_id: int
    message: str
    template: Optional[str] = None
    anomaly_flag: int = 0


class ProcessLogsRequest(BaseModel):
    """Request to process logs."""
    dataset: DatasetEnum
    sequence_length: int = Field(50, ge=10, le=200)
    batch_size: int = Field(32, ge=1, le=256)


class DetectAnomaliesRequest(BaseModel):
    """Request to detect anomalies."""
    dataset: DatasetEnum
    threshold: float = Field(0.5, ge=0.0, le=1.0)
    use_lstm: bool = True
    use_isolation_forest: bool = True


class AnomalyResult(BaseModel):
    """Single anomaly detection result."""
    sequence_id: str
    anomaly_score: float
    is_anomaly: bool
    lstm_score: Optional[float] = None
    if_score: Optional[float] = None
    sequence: List[int]


class MetricsResponse(BaseModel):
    """Model metrics."""
    precision: float
    recall: float
    f1_score: float
    total_anomalies: int
    total_normal: int
    anomaly_rate: float


class DetectionResponse(BaseModel):
    """Response from anomaly detection."""
    total_processed: int
    total_anomalies: int
    anomaly_rate: float
    results: List[AnomalyResult]
    metrics: Optional[MetricsResponse] = None


class DatasetInfo(BaseModel):
    """Information about a dataset."""
    name: str
    total_samples: int
    total_anomalies: int
    total_normal: int
    anomaly_rate: float


class AvailableDatasetsResponse(BaseModel):
    """Response with available datasets."""
    datasets: List[str]
    dataset_info: Dict[str, DatasetInfo]


class StreamLogsRequest(BaseModel):
    """Request for streaming logs."""
    dataset: DatasetEnum
    batch_interval: float = Field(1.0, ge=0.1, le=10.0)
    limit: Optional[int] = None


class StreamEvent(BaseModel):
    """Single event in stream."""
    event_id: int
    timestamp: str
    anomaly_score: float
    is_anomaly: bool


class HealthResponse(BaseModel):
    """API health check."""
    status: str
    version: str
    ready: bool
