"""Drain-like log parser for extracting templates and events."""
import re
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import numpy as np


class DrainLogParser:
    """
    Simplified Drain algorithm for log parsing.
    Extracts templates from raw logs.
    """

    def __init__(self, depth: int = 4, st: float = 0.5):
        """
        Initialize Drain parser.
        
        Args:
            depth: Max depth of the prefix tree
            st: Similarity threshold for grouping logs
        """
        self.depth = depth
        self.st = st
        self.tree = {}
        self.templates = {}
        self.log_clusters = defaultdict(list)
        self.template_count = 0

    def _tokenize(self, message: str) -> List[str]:
        """Split log message into tokens."""
        message = re.sub(r'\s+', ' ', message.strip())
        tokens = message.split()
        return tokens

    def _get_token_count(self, tokens: List[str]) -> int:
        """Get number of tokens in log message."""
        return len(tokens)

    def _calculate_similarity(self, template: List[str], tokens: List[str]) -> float:
        """
        Calculate similarity between template and tokens using token ratio.
        
        Args:
            template: Template tokens
            tokens: Log message tokens
            
        Returns:
            Similarity score [0, 1]
        """
        if len(template) != len(tokens):
            return 0.0

        match_count = sum(1 for t, s in zip(template, tokens) if t == s or t == '*')
        return match_count / len(template)

    def parse_line(self, line: str) -> Tuple[int, str]:
        """
        Parse a single log line and return event ID and template.
        
        Args:
            line: Raw log line
            
        Returns:
            Tuple of (event_id, template)
        """
        tokens = self._tokenize(line)
        token_count = self._get_token_count(tokens)

        # Find matching cluster or create new one
        cluster_id = None

        # Search in existing templates
        for template_id, template in self.templates.items():
            if self._get_token_count(template) != token_count:
                continue

            similarity = self._calculate_similarity(template, tokens)
            if similarity >= self.st:
                cluster_id = template_id
                # Update template with wildcard
                updated_template = [
                    '*' if t != s else t 
                    for t, s in zip(template, tokens)
                ]
                self.templates[template_id] = updated_template
                break

        # Create new cluster if not found
        if cluster_id is None:
            cluster_id = self.template_count
            self.templates[cluster_id] = tokens
            self.template_count += 1

        self.log_clusters[cluster_id].append(line)
        return cluster_id, self.get_template_string(cluster_id)

    def get_template_string(self, template_id: int) -> str:
        """Get template as formatted string."""
        if template_id in self.templates:
            return ' '.join(self.templates[template_id])
        return "UNKNOWN"

    def parse_logs(self, logs: List[str]) -> List[Dict]:
        """
        Parse multiple logs.
        
        Args:
            logs: List of raw log lines
            
        Returns:
            List of parsed log dictionaries
        """
        parsed = []
        for log in logs:
            event_id, template = self.parse_line(log)
            parsed.append({
                'event_id': event_id,
                'template': template,
                'raw_log': log
            })
        return parsed

    def get_statistics(self) -> Dict:
        """Get parser statistics."""
        return {
            'total_templates': len(self.templates),
            'total_clusters': len(self.log_clusters),
            'avg_cluster_size': np.mean([len(v) for v in self.log_clusters.values()]) 
                               if self.log_clusters else 0
        }
