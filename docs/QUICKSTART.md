# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Option 1: Local Development (Recommended)

#### Prerequisites
- Python 3.8+
- Node.js 16+

#### Setup

1. **Install backend dependencies**:
```bash
pip install -r requirements.txt
```

2. **Install frontend dependencies**:
```bash
cd frontend && npm install && cd ..
```

3. **Start backend** (Terminal 1):
```bash
python -m uvicorn backend.main:app --reload
```

4. **Start frontend** (Terminal 2):
```bash
cd frontend && npm run dev
```

5. **Open browser**:
- Dashboard: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

### Option 2: Using Startup Script

**Linux/Mac**:
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

**Windows**:
```bash
scripts\start.bat
```

---

### Option 3: Docker

```bash
cd docker
docker-compose up
```

Then open http://localhost:5173

---

## 📊 First Steps

1. **Select a dataset**: Choose HDFS, BGL, or OpenStack
2. **View Dashboard**: Real-time stats and live log stream
3. **Check Analysis**: Model performance metrics
4. **Explore Logs**: Search and filter individual logs
5. **Configure**: Adjust thresholds in Settings

---

## 🔌 API Quick Reference

**Health Check**:
```bash
curl http://localhost:8000/api/v1/health
```

**Get Datasets**:
```bash
curl http://localhost:8000/api/v1/datasets
```

**Process Logs**:
```bash
curl -X POST http://localhost:8000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{"dataset": "hdfs", "sequence_length": 50, "batch_size": 32}'
```

**Detect Anomalies**:
```bash
curl -X POST http://localhost:8000/api/v1/detect \
  -H "Content-Type: application/json" \
  -d '{"dataset": "hdfs", "threshold": 0.5}'
```

---

## 🧠 How It Works

```
Raw Logs
   ↓
Drain Parser (Extract Templates)
   ↓
Sequence Generator (Fixed-length windows)
   ↓
Feature Encoder (Statistical features)
   ↓
├─ LSTM Model (Predict next event)
├─ Isolation Forest (Anomaly scoring)
   ↓
Hybrid Detector (Combine scores)
   ↓
Classification & Visualization
```

---

## 📈 Key Features

- **3 Datasets**: HDFS, BGL, OpenStack
- **Hybrid ML**: LSTM + Isolation Forest
- **Real-time UI**: Live log stream with anomaly highlights
- **Model Analytics**: Metrics, confusion matrix, ROC curves
- **Advanced Search**: Filter and export logs
- **Dark Theme**: NVIDIA-inspired design

---

## ⚙️ Configuration

Edit `backend/config.py`:
```python
SEQUENCE_LENGTH = 50        # Events per sequence
ANOMALY_THRESHOLD = 0.5     # Classification threshold
BATCH_SIZE = 32             # Processing batch size
```

---

## 🐛 Troubleshooting

**Backend won't start**:
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process: kill -9 <PID>
```

**Frontend won't start**:
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
```

**No data appearing**:
- Ensure datasets are in `datasets/` directory
- Check backend logs for errors
- Verify API connection in browser DevTools

---

## 📚 More Information

See `PROJECT_README.md` for:
- Detailed architecture
- Model training guide
- Full API documentation
- Advanced configuration
- Future enhancements

---

**Ready to go!** 🎉
