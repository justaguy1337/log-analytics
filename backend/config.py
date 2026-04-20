"""Configuration for the backend application."""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Dataset paths
HDFS_V1_DIR = DATASETS_DIR / "HDFS_v1"
BGL_DIR = DATASETS_DIR / "BGL"
OPENSTACK_DIR = DATASETS_DIR / "OpenStack"

# Processing
SEQUENCE_LENGTH = 50  # Number of events in a sequence
ANOMALY_THRESHOLD = 0.5  # Threshold for anomaly detection
BATCH_SIZE = 32

# Model paths
LSTM_MODEL_PATH = MODELS_DIR / "lstm_model.pt"
IF_MODEL_PATH = MODELS_DIR / "isolation_forest.pkl"

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
