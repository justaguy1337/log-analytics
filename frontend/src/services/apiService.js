import axios from 'axios'

const API_BASE_URL = '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  // Health check
  health: () => api.get('/health'),

  // Datasets
  getAvailableDatasets: () => api.get('/datasets'),
  
  // Processing
  processLogs: (dataset, sequenceLength = 50, batchSize = 32) =>
    api.post('/process', {
      dataset,
      sequence_length: sequenceLength,
      batch_size: batchSize,
    }),

  // Anomaly detection
  detectAnomalies: (dataset, threshold = 0.5, useLstm = true, useIf = true) =>
    api.post('/detect', {
      dataset,
      threshold,
      use_lstm: useLstm,
      use_isolation_forest: useIf,
    }),

  // Metrics
  getMetrics: (dataset) => api.get('/metrics', { params: { dataset } }),

  // Streaming
  streamLogs: (dataset, batchInterval = 1.0, limit = null) =>
    api.post('/stream', {
      dataset,
      batch_interval: batchInterval,
      limit,
    }),

  // Training
  trainModels: (dataset) => api.post('/train', null, { params: { dataset } }),
}

export default apiService
