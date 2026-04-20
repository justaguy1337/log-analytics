"""Isolation Forest model for frequency-based anomaly detection."""
import numpy as np
import pickle
from pathlib import Path
from sklearn.ensemble import IsolationForest
from typing import Tuple, List, Dict


class IsolationForestModel:
    """
    Isolation Forest for detecting anomalies based on event frequency.
    """

    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        """
        Initialize Isolation Forest.
        
        Args:
            contamination: Expected proportion of anomalies [0, 1]
            random_state: Random seed for reproducibility
        """
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.is_fitted = False

    def fit(self, features: np.ndarray) -> None:
        """
        Fit the model on features.
        
        Args:
            features: Feature matrix (n_samples, n_features)
        """
        self.model.fit(features)
        self.is_fitted = True

    def predict(self, features: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies.
        
        Args:
            features: Feature matrix
            
        Returns:
            Tuple of (predictions, anomaly_scores)
            Predictions: -1 for anomaly, 1 for normal
            Scores: Anomaly scores in [-1, 1]
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")

        predictions = self.model.predict(features)
        scores = self.model.score_samples(features)

        # Normalize scores to [0, 1]
        scores_normalized = (scores + 1) / 2  # Convert from [-1, 0] to [0, 0.5] typically

        return predictions, scores_normalized

    def get_anomaly_scores(self, features: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores only.
        Higher score indicates more anomalous.
        
        Args:
            features: Feature matrix
            
        Returns:
            Anomaly scores in [0, 1]
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")

        scores = self.model.score_samples(features)
        # Normalize scores to [0, 1]
        scores_normalized = (scores + 1) / 2

        return scores_normalized

    def predict_single(self, features: np.ndarray) -> Tuple[int, float]:
        """
        Predict anomaly for single sample.
        
        Args:
            features: Single feature vector
            
        Returns:
            Tuple of (prediction, anomaly_score)
        """
        features = features.reshape(1, -1)
        predictions, scores = self.predict(features)
        return predictions[0], scores[0]

    def get_feature_importance(self) -> Dict[int, float]:
        """
        Get feature importance from the model.
        
        Returns:
            Dictionary mapping feature index to importance
        """
        # Isolation Forest doesn't have built-in feature importance
        # Return a simple approximation based on tree splits
        importance = np.zeros(self.model.n_features_in_)
        
        for estimator in self.model.estimators_:
            # Count feature usage in each tree
            feature_counts = np.zeros(self.model.n_features_in_)

            def count_features(node):
                if node.feature != -2:  # Not a leaf
                    feature_counts[node.feature] += 1
                    if node.children_left != -1:
                        count_features(node.children_left)
                    if node.children_right != -1:
                        count_features(node.children_right)

            count_features(estimator.tree_)
            importance += feature_counts

        importance = importance / len(self.model.estimators_)
        return {i: float(imp) for i, imp in enumerate(importance)}

    def save(self, path: Path) -> None:
        """Save model to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def load(self, path: Path) -> None:
        """Load model from disk."""
        with open(path, 'rb') as f:
            obj = pickle.load(f)
            self.__dict__.update(obj.__dict__)
