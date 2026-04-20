"""LSTM model for sequence-based anomaly detection."""
import torch
import torch.nn as nn
import numpy as np
from typing import Tuple, List
from pathlib import Path


class LSTMModel(nn.Module):
    """
    LSTM model for predicting next event in log sequence.
    Anomalies detected when prediction error is high.
    """

    def __init__(
        self,
        vocab_size: int,
        embedding_dim: int = 64,
        hidden_dim: int = 128,
        num_layers: int = 2,
        dropout: float = 0.2,
        output_dim: int = None
    ):
        """
        Initialize LSTM model.
        
        Args:
            vocab_size: Size of event vocabulary
            embedding_dim: Dimension of event embeddings
            hidden_dim: Hidden dimension of LSTM
            num_layers: Number of LSTM layers
            dropout: Dropout rate
            output_dim: Output dimension (defaults to vocab_size for prediction)
        """
        super(LSTMModel, self).__init__()

        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.output_dim = output_dim or vocab_size

        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)

        # LSTM layers
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )

        # Output layer
        self.fc = nn.Linear(hidden_dim, self.output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        
        Args:
            x: Input tensor of shape (batch_size, sequence_length)
            
        Returns:
            Output tensor of shape (batch_size, sequence_length, output_dim)
        """
        # Embed input
        embedded = self.embedding(x)  # (batch_size, seq_len, embedding_dim)
        embedded = self.dropout(embedded)

        # LSTM
        lstm_out, _ = self.lstm(embedded)  # (batch_size, seq_len, hidden_dim)
        lstm_out = self.dropout(lstm_out)

        # Dense output
        output = self.fc(lstm_out)  # (batch_size, seq_len, output_dim)

        return output

    def encode_sequence(self, x: torch.Tensor) -> torch.Tensor:
        """
        Get LSTM hidden state as sequence encoding.
        
        Args:
            x: Input tensor
            
        Returns:
            Hidden state tensor
        """
        embedded = self.embedding(x)
        _, (hidden, _) = self.lstm(embedded)
        return hidden[-1]  # Last layer hidden state

    def predict_next_event(self, sequence: np.ndarray) -> Tuple[int, float]:
        """
        Predict next event in sequence.
        
        Args:
            sequence: Event sequence as numpy array
            
        Returns:
            Tuple of (predicted_event_id, confidence)
        """
        self.eval()
        with torch.no_grad():
            x = torch.tensor(sequence, dtype=torch.long).unsqueeze(0)
            output = self.forward(x)
            
            # Get prediction for last position
            last_pred = output[0, -1, :]  # (output_dim,)
            
            # Get top prediction
            predicted_id = torch.argmax(last_pred).item()
            confidence = torch.softmax(last_pred, dim=0)[predicted_id].item()

        return predicted_id, confidence

    def compute_anomaly_score(self, sequence: np.ndarray) -> float:
        """
        Compute anomaly score based on prediction error.
        Higher score indicates more anomalous.
        
        Args:
            sequence: Event sequence
            
        Returns:
            Anomaly score in [0, 1]
        """
        self.eval()
        with torch.no_grad():
            x = torch.tensor(sequence, dtype=torch.long).unsqueeze(0)
            output = self.forward(x)

            # Compute prediction loss for each position
            losses = []
            for i in range(len(sequence) - 1):
                pred = output[0, i, :]
                target = sequence[i + 1]

                # Cross-entropy loss
                loss = nn.functional.cross_entropy(
                    pred.unsqueeze(0),
                    torch.tensor([target], dtype=torch.long)
                )
                losses.append(loss.item())

            # Anomaly score: mean loss
            anomaly_score = np.mean(losses) if losses else 0.0

        return min(anomaly_score, 1.0)  # Clip to [0, 1]

    def train_epoch(
        self,
        sequences: np.ndarray,
        optimizer: torch.optim.Optimizer,
        device: str = "cpu"
    ) -> float:
        """
        Train for one epoch.
        
        Args:
            sequences: Training sequences
            optimizer: Optimizer
            device: Device to train on
            
        Returns:
            Average loss
        """
        self.train()
        self.to(device)

        total_loss = 0
        num_batches = 0

        # Prepare targets (next event)
        for seq in sequences:
            if len(seq) < 2:
                continue

            x = torch.tensor(seq[:-1], dtype=torch.long).unsqueeze(0).to(device)
            y = torch.tensor(seq[1:], dtype=torch.long).unsqueeze(0).to(device)

            optimizer.zero_grad()

            output = self.forward(x)

            # Reshape for loss computation
            output = output.view(-1, self.output_dim)
            y = y.view(-1)

            loss = nn.functional.cross_entropy(output, y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            num_batches += 1

        return total_loss / num_batches if num_batches > 0 else 0

    def save(self, path: Path):
        """Save model weights."""
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(self.state_dict(), path)

    def load(self, path: Path):
        """Load model weights."""
        self.load_state_dict(torch.load(path, map_location="cpu"))
