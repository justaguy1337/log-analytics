"""Sequence generation from parsed logs."""
import numpy as np
from typing import List, Dict, Tuple
from collections import defaultdict


class SequenceGenerator:
    """Generate fixed-length sequences from log events."""

    def __init__(self, sequence_length: int = 50):
        """
        Initialize sequence generator.
        
        Args:
            sequence_length: Length of each sequence
        """
        self.sequence_length = sequence_length

    def generate_sequences_from_events(
        self, 
        events: List[int], 
        labels: List[int] = None,
        step_size: int = 1
    ) -> Tuple[List[List[int]], List[int]]:
        """
        Generate sequences using sliding window.
        
        Args:
            events: List of event IDs
            labels: Anomaly labels for each event (optional)
            step_size: Sliding window step size
            
        Returns:
            Tuple of (sequences, sequence_labels)
        """
        sequences = []
        sequence_labels = []

        for i in range(0, len(events) - self.sequence_length + 1, step_size):
            seq = events[i:i + self.sequence_length]
            sequences.append(seq)

            # Label a sequence as anomalous if it contains any anomalous event
            if labels:
                label = max(labels[i:i + self.sequence_length])
            else:
                label = 0
            sequence_labels.append(label)

        return sequences, sequence_labels

    def generate_sequences_from_dict(
        self,
        logs_dict: Dict,
        labels_dict: Dict = None
    ) -> Tuple[List[List[int]], List[int], List[str]]:
        """
        Generate sequences from dictionary of log sequences.
        Used for HDFS where logs are already grouped by block ID.
        
        Args:
            logs_dict: Dictionary mapping IDs to event sequences
            labels_dict: Dictionary mapping IDs to labels
            
        Returns:
            Tuple of (sequences, labels, sequence_ids)
        """
        sequences = []
        sequence_labels = []
        sequence_ids = []

        for seq_id, event_list in logs_dict.items():
            if len(event_list) >= self.sequence_length:
                # Pad or truncate to sequence_length
                if len(event_list) > self.sequence_length:
                    # Use sliding window
                    for i in range(0, len(event_list) - self.sequence_length + 1):
                        sequences.append(event_list[i:i + self.sequence_length])
                        sequence_ids.append(f"{seq_id}_{i}")
                        
                        label = labels_dict.get(seq_id, 0) if labels_dict else 0
                        sequence_labels.append(label)
                else:
                    # Pad with zeros
                    padded = event_list + [0] * (self.sequence_length - len(event_list))
                    sequences.append(padded)
                    sequence_ids.append(seq_id)
                    
                    label = labels_dict.get(seq_id, 0) if labels_dict else 0
                    sequence_labels.append(label)

        return sequences, sequence_labels, sequence_ids

    def generate_batch_sequences(
        self,
        sequences: List[List[int]],
        batch_size: int = 32
    ) -> List[np.ndarray]:
        """
        Create batches of sequences as numpy arrays.
        
        Args:
            sequences: List of sequences
            batch_size: Batch size
            
        Returns:
            List of batched numpy arrays
        """
        batches = []
        for i in range(0, len(sequences), batch_size):
            batch = sequences[i:i + batch_size]
            # Pad batch if necessary
            if len(batch) < batch_size:
                padding = [
                    [0] * self.sequence_length 
                    for _ in range(batch_size - len(batch))
                ]
                batch = batch + padding
            
            batches.append(np.array(batch, dtype=np.int32))

        return batches

    def generate_feature_vectors(
        self,
        sequences: List[List[int]]
    ) -> np.ndarray:
        """
        Generate frequency-based feature vectors from sequences.
        Used for Isolation Forest model.
        
        Args:
            sequences: List of sequences
            
        Returns:
            Feature matrix (n_samples, n_events)
        """
        max_event_id = 0
        for seq in sequences:
            if seq:
                max_event_id = max(max_event_id, max(seq))

        feature_vectors = []
        for seq in sequences:
            # Count frequency of each event
            freq = [0] * (max_event_id + 1)
            for event_id in seq:
                if event_id > 0:
                    freq[event_id] += 1
            feature_vectors.append(freq)

        return np.array(feature_vectors, dtype=np.float32)
