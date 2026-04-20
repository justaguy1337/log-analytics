"""Dataset loader for HDFS, BGL, and OpenStack logs."""
import os
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from pathlib import Path
import csv


class DatasetLoader:
    """Load and preprocess log datasets."""

    def __init__(self, dataset_dir: Path):
        self.dataset_dir = dataset_dir

    def load_hdfs_v1(self) -> Tuple[Dict, Dict]:
        """
        Load HDFS_v1 dataset.
        
        Returns:
            Tuple of (logs_dict, labels_dict)
        """
        hdfs_dir = self.dataset_dir / "HDFS_v1"
        
        if not hdfs_dir.exists():
            return {}, {}

        logs = {}
        labels = {}

        # Load preprocessed data if available
        preprocessed_dir = hdfs_dir / "preprocessed"
        if preprocessed_dir.exists():
            # Load event traces
            traces_file = preprocessed_dir / "Event_traces.csv"
            if traces_file.exists():
                df = pd.read_csv(traces_file)
                for _, row in df.iterrows():
                    block_id = row.get('BlockId', 'unknown')
                    event_id = row.get('EventId', -1)
                    if block_id not in logs:
                        logs[block_id] = []
                    logs[block_id].append(int(event_id))

            # Load anomaly labels
            labels_file = preprocessed_dir / "anomaly_label.csv"
            if labels_file.exists():
                df = pd.read_csv(labels_file)
                for _, row in df.iterrows():
                    block_id = row.get('BlockId', row.get('block_id', 'unknown'))
                    label = row.get('Label', row.get('label', 0))
                    labels[block_id] = int(label)

        return logs, labels

    def load_bgl(self) -> Tuple[List[str], List[int]]:
        """
        Load BGL dataset.
        
        Returns:
            Tuple of (log_lines, labels)
        """
        bgl_dir = self.dataset_dir / "BGL"
        
        if not bgl_dir.exists():
            return [], []

        logs = []
        labels = []

        # Try to load BGL.log file
        log_file = bgl_dir / "BGL.log"
        if log_file.exists():
            with open(log_file, 'r', errors='ignore') as f:
                for line in f:
                    logs.append(line.strip())
                    # Simple heuristic: check if line contains error indicators
                    label = 1 if any(x in line.lower() for x in ['error', 'fail', 'exception']) else 0
                    labels.append(label)

        return logs, labels

    def load_openstack(self) -> Tuple[List[str], List[int]]:
        """
        Load OpenStack dataset.
        
        Returns:
            Tuple of (log_lines, labels)
        """
        openstack_dir = self.dataset_dir / "OpenStack"
        
        if not openstack_dir.exists():
            return [], []

        logs = []
        labels = []

        # Try to load OpenStack logs
        labels_file = openstack_dir / "anomaly_labels.txt"
        if labels_file.exists():
            with open(labels_file, 'r', errors='ignore') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        labels.append(int(parts[-1]))  # Last value is label

        return logs, labels

    def load_dataset(self, dataset_name: str) -> Dict:
        """
        Load a specific dataset.
        
        Args:
            dataset_name: 'hdfs', 'bgl', or 'openstack'
            
        Returns:
            Dictionary containing dataset information
        """
        dataset_name = dataset_name.lower()

        if dataset_name == 'hdfs':
            logs, labels = self.load_hdfs_v1()
            return {
                'name': 'HDFS v1',
                'logs': logs,
                'labels': labels,
                'type': 'sequences'
            }
        elif dataset_name == 'bgl':
            logs, labels = self.load_bgl()
            return {
                'name': 'BGL',
                'logs': logs,
                'labels': labels,
                'type': 'lines'
            }
        elif dataset_name == 'openstack':
            logs, labels = self.load_openstack()
            return {
                'name': 'OpenStack',
                'logs': logs,
                'labels': labels,
                'type': 'lines'
            }
        else:
            return {'error': f'Unknown dataset: {dataset_name}'}

    def get_available_datasets(self) -> List[str]:
        """Get list of available datasets."""
        available = []
        if (self.dataset_dir / "HDFS_v1").exists():
            available.append('hdfs')
        if (self.dataset_dir / "BGL").exists():
            available.append('bgl')
        if (self.dataset_dir / "OpenStack").exists():
            available.append('openstack')
        return available
