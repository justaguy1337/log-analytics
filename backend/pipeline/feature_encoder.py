"""Feature encoding and normalization."""
import numpy as np
from typing import Dict, Tuple, List
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class FeatureEncoder:
    """Encode and normalize features for ML models."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.event_vocab = {}
        self.vocab_size = 0

    def build_vocabulary(self, sequences: List[List[int]]) -> Dict[int, int]:
        """
        Build vocabulary of event IDs.
        
        Args:
            sequences: List of sequences containing event IDs
            
        Returns:
            Vocabulary mapping (event_id -> index)
        """
        unique_events = set()
        for seq in sequences:
            unique_events.update([e for e in seq if e >= 0])

        # Sort for consistency
        sorted_events = sorted(unique_events)
        self.event_vocab = {event: idx for idx, event in enumerate(sorted_events)}
        self.vocab_size = len(self.event_vocab)

        return self.event_vocab

    def encode_sequences(self, sequences: List[List[int]]) -> np.ndarray:
        """
        Encode sequences using vocabulary.
        Maps event IDs to vocabulary indices.
        
        Args:
            sequences: List of raw event sequences
            
        Returns:
            Encoded sequences as numpy array
        """
        encoded = []
        for seq in sequences:
            encoded_seq = [
                self.event_vocab.get(e, 0) for e in seq
            ]
            encoded.append(encoded_seq)

        return np.array(encoded, dtype=np.int32)

    def normalize_features(
        self,
        features: np.ndarray,
        fit: bool = True
    ) -> np.ndarray:
        """
        Normalize features using StandardScaler.
        
        Args:
            features: Feature matrix
            fit: Whether to fit the scaler
            
        Returns:
            Normalized features
        """
        if fit:
            self.scaler.fit(features)
            self.is_fitted = True

        if not self.is_fitted:
            raise ValueError("Scaler not fitted. Call normalize_features with fit=True first.")

        return self.scaler.transform(features)

    def get_embedding_matrix(self, embedding_dim: int = 64) -> np.ndarray:
        """
        Initialize embedding matrix for event sequences.
        
        Args:
            embedding_dim: Dimension of embeddings
            
        Returns:
            Embedding matrix (vocab_size, embedding_dim)
        """
        # Random initialization - in production would use pre-trained embeddings
        embedding_matrix = np.random.randn(self.vocab_size, embedding_dim).astype(np.float32)
        # Normalize embeddings
        embedding_matrix = embedding_matrix / np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
        return embedding_matrix

    def extract_statistical_features(
        self,
        sequences: List[List[int]]
    ) -> np.ndarray:
        """
        Extract statistical features from sequences for traditional ML.
        
        Args:
            sequences: List of sequences
            
        Returns:
            Feature matrix with statistical features
        """
        features = []

        for seq in sequences:
            seq_array = np.array(seq, dtype=np.float32)
            
            # Extract features
            feature_vector = [
                len(set(seq)),  # Unique events
                np.mean(seq_array),  # Mean event ID
                np.std(seq_array),  # Std of event IDs
                np.max(seq_array),  # Max event ID
                np.min(seq_array),  # Min event ID
                np.median(seq_array),  # Median event ID
            ]
            features.append(feature_vector)

        return np.array(features, dtype=np.float32)

    def encode_labels(self, labels: List[int]) -> np.ndarray:
        """
        Convert labels to numpy array.
        
        Args:
            labels: List of binary labels (0 or 1)
            
        Returns:
            Label array
        """
        return np.array(labels, dtype=np.int32)
