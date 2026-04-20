# Distributed Log Analytics Platform with ML-Based Anomaly Detection

A full-stack distributed log monitoring platform featuring ML-powered anomaly detection with a modern, minimal UI inspired by NVIDIA's design language.

![Platform Overview](./docs/overview.md)

## 🎯 Features

- **Real-time Log Processing**: Stream logs from HDFS, BGL, and OpenStack datasets
- **Hybrid Anomaly Detection**: Combines LSTM and Isolation Forest models for robust detection
- **Interactive Dashboard**: Real-time visualization with live log streaming
- **Model Insights**: Detailed performance metrics, confusion matrices, and ROC curves
- **Advanced Log Exploration**: Search, filter, and export log data
- **Modern UI**: Dark theme with neon accents, smooth animations, responsive design

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python)
- **ML Models**: PyTorch (LSTM), Scikit-learn (Isolation Forest)
- **Processing**: Pandas, NumPy
- **Parsing**: Drain-like log parser

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS with custom animations
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React

### Data Pipeline
```
Raw Logs → Parsing → Sequence Generation → Feature Encoding → 
LSTM Model (Sequential Anomalies) & Isolation Forest (Statistical Anomalies) → 
Hybrid Scoring → Detection Results → Dashboard
```

## 📋 Project Structure

```
log-analytics/
├── backend/
│   ├── api/
│   │   ├── routes.py          # API endpoints
│   │   └── schemas.py         # Pydantic models
│   ├── parsers/
│   │   ├── drain_parser.py    # Log parsing
│   │   └── dataset_loader.py  # Dataset loading
│   ├── models/
│   │   ├── lstm_model.py      # LSTM model
│   │   └── isolation_forest.py # IF model
│   ├── pipeline/
│   │   ├── sequence_generator.py # Sequence generation
│   │   ├── feature_encoder.py   # Feature encoding
│   │   └── anomaly_detector.py  # Hybrid detector
│   ├── config.py              # Configuration
│   └── main.py                # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API client
│   │   ├── App.jsx            # Main app
│   │   └── index.css          # Global styles
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── datasets/
│   ├── HDFS_v1/
│   ├── BGL/
│   └── OpenStack/
├── requirements.txt           # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Start the backend server**:
```bash
python -m backend.main
# or
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Frontend Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Start development server**:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Access the Platform

- **Dashboard**: http://localhost:5173
- **API**: http://localhost:8000/api/v1
- **API Docs**: http://localhost:8000/docs

## 📊 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/datasets` | GET | Available datasets |
| `/api/v1/process` | POST | Process logs |
| `/api/v1/detect` | POST | Detect anomalies |
| `/api/v1/metrics` | GET | Model metrics |
| `/api/v1/stream` | POST | Stream logs |
| `/api/v1/train` | POST | Train models |

### Example: Process Logs

```bash
curl -X POST http://localhost:8000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "hdfs",
    "sequence_length": 50,
    "batch_size": 32
  }'
```

### Example: Detect Anomalies

```bash
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "hdfs",
    "threshold": 0.5,
    "use_lstm": true,
    "use_isolation_forest": true
  }'
```

## 🧠 ML Models

### LSTM Model
- **Purpose**: Detect sequential anomalies
- **Architecture**: 2-layer LSTM with 128 hidden units
- **Input**: Sequences of 50 event IDs
- **Output**: Prediction error (anomaly score)
- **Anomaly Detection**: Events with high prediction error are flagged as anomalous

### Isolation Forest Model
- **Purpose**: Detect statistical anomalies
- **Features**: 
  - Unique event count
  - Event frequency variance
  - Average event ID
  - Event sequence length
  - Max/min event IDs
- **Trees**: 100
- **Anomaly Detection**: Events with unusual frequency patterns are flagged

### Hybrid Approach
- Combines LSTM and Isolation Forest scores with configurable weights
- Default: 50% LSTM + 50% Isolation Forest
- More robust than individual models

## 📈 Metrics & Evaluation

The system computes standard ML metrics:

- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **AUC-ROC**: Area under the receiver operating characteristic curve
- **Confusion Matrix**: TP, TN, FP, FN breakdown

## 🎨 UI Components

### Dashboard
- Real-time stats (logs, anomalies, rates)
- Live log stream with anomaly highlights
- Anomaly detection timeline
- System health status

### Analysis Page
- Model performance comparison
- Confusion matrix visualization
- ROC curve analysis
- Feature importance

### Logs Explorer
- Advanced search and filtering
- Date range selection
- Anomaly status filtering
- Export functionality

### Settings
- Anomaly threshold configuration
- Sequence length adjustment
- Model weight tuning
- Auto-refresh settings

## 🔧 Configuration

### Key Settings (backend/config.py)

```python
SEQUENCE_LENGTH = 50          # Events per sequence
ANOMALY_THRESHOLD = 0.5       # Classification threshold
BATCH_SIZE = 32               # Processing batch size
LSTM_WEIGHT = 0.5             # LSTM model weight
IF_WEIGHT = 0.5               # Isolation Forest weight
```

### Environment Variables (.env)

```bash
DEBUG=true                    # Debug mode
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
API_CORS_ORIGINS=*
```

## 📚 Data Formats

### Log Processing Pipeline

1. **Raw Logs** → Parsed Templates
   - Extract event IDs, timestamps, templates
   - Remove duplicates

2. **Templates** → Event Sequences
   - Group by block ID (HDFS) or window (BGL/OpenStack)
   - Create sliding windows of 50 events

3. **Sequences** → Features
   - Encode events using vocabulary
   - Extract statistical features

4. **Features** → Anomaly Scores
   - LSTM: Predict next event
   - Isolation Forest: Anomaly score
   - Hybrid: Combined score

## 🚦 Anomaly Detection Flow

```
Input Log Sequence
    ↓
[Event IDs: [1, 5, 2, 9, ...]]
    ↓
├─→ LSTM Model
│   ├─ Embed events
│   ├─ Process through LSTM
│   ├─ Predict next event
│   └─ Calculate prediction error
│
├─→ Isolation Forest Model
│   ├─ Extract statistical features
│   ├─ Compute anomaly score
│   └─ Normalize to [0, 1]
│
├─ Combine Scores
│   score = 0.5 * lstm_score + 0.5 * if_score
│
└─→ Classification
    if score >= threshold → ANOMALY
    else → NORMAL
```

## 🧪 Testing

### Manual Testing via Dashboard
1. Navigate to Dashboard
2. Select a dataset (HDFS, BGL, OpenStack)
3. View real-time statistics
4. Navigate to Analysis to view metrics
5. Explore logs in Logs viewer

### API Testing
```bash
# Check health
curl http://localhost:8000/api/v1/health

# Get datasets
curl http://localhost:8000/api/v1/datasets

# Process logs
curl -X POST http://localhost:8000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"dataset": "hdfs", "sequence_length": 50}'
```

## 🔮 Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Kafka integration for log streaming
- [ ] Model retraining pipeline
- [ ] Alert system with email/Slack notifications
- [ ] Multi-tenancy support
- [ ] Distributed processing with Ray
- [ ] Advanced visualizations (3D embeddings)
- [ ] Model explainability (SHAP values)
- [ ] Custom log parsers
- [ ] Backup and recovery

## 📝 Model Training (Pseudo-code)

```python
from backend.models.lstm_model import LSTMModel
from backend.models.isolation_forest import IsolationForestModel
from backend.parsers.dataset_loader import DatasetLoader
from backend.pipeline.sequence_generator import SequenceGenerator
from backend.pipeline.feature_encoder import FeatureEncoder

# Load data
loader = DatasetLoader("./datasets")
data = loader.load_dataset("hdfs")

# Generate sequences
gen = SequenceGenerator(sequence_length=50)
sequences, labels, ids = gen.generate_sequences_from_dict(data['logs'], data['labels'])

# Encode features
encoder = FeatureEncoder()
encoder.build_vocabulary(sequences)
features = encoder.extract_statistical_features(sequences)
features_normalized = encoder.normalize_features(features, fit=True)

# Train LSTM
lstm_model = LSTMModel(vocab_size=encoder.vocab_size)
optimizer = torch.optim.Adam(lstm_model.parameters())
for epoch in range(10):
    loss = lstm_model.train_epoch(sequences, optimizer)
    print(f"Epoch {epoch}: Loss = {loss}")
lstm_model.save("./models/lstm_model.pt")

# Train Isolation Forest
if_model = IsolationForestModel(contamination=0.1)
if_model.fit(features_normalized)
if_model.save("./models/isolation_forest.pkl")
```

## 📊 Supported Datasets

### HDFS v1
- **Source**: Distributed file system logs
- **Size**: 11,175 sequences
- **Format**: Block ID → Event sequences
- **Labels**: Normal/Anomalous

### BGL
- **Source**: Blue Gene/L supercomputer
- **Size**: ~4.7M events
- **Format**: Raw log lines
- **Labels**: Heuristic-based

### OpenStack
- **Source**: Cloud computing platform
- **Size**: ~207K events
- **Format**: Raw log lines
- **Labels**: Anomaly labels file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file

## 👥 Authors

- AI Assistant
- Built with ❤️ for distributed systems monitoring

## 🆘 Troubleshooting

### Backend Issues

**Port Already in Use**
```bash
# Change port in config.py or use environment variable
python -m backend.main --port 8001
```

**Import Errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**Port Already in Use**
```bash
# Vite will automatically use the next available port
npm run dev
```

**API Connection Failed**
- Ensure backend is running on port 8000
- Check CORS settings in backend/config.py
- Verify API endpoint in frontend/src/services/apiService.js

### Model Training Issues

**CUDA Not Available**
- Update config to use CPU: `torch.device("cpu")`
- Install CPU-only PyTorch: `pip install torch-cpu`

## 📞 Support

For issues, questions, or suggestions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with details

---

**Last Updated**: April 2026
**Version**: 1.0.0
