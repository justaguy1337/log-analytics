# 📊 Distributed Log Analytics Platform with ML-Based Anomaly Detection

A production-grade system for analyzing distributed logs using hybrid machine learning models (LSTM + Isolation Forest) to detect anomalies in real-time.

## 🚀 Quick Start

```bash
# Activate virtual environment and run both services
source venv/bin/activate && trap 'kill $(jobs -p) 2>/dev/null' EXIT; python -m uvicorn backend.main:app --reload & (cd frontend && npm run dev) & wait
```

Or use the startup script:
```bash
chmod +x scripts/start.sh && ./scripts/start.sh
```

**Access Points:**
- 🎨 **Frontend**: http://localhost:5173
- 🔌 **API**: http://localhost:8000
- 📖 **API Docs**: http://localhost:8000/docs

## 📚 Documentation

Complete documentation is in the [docs/](docs/) folder:

- **[START_HERE.md](docs/START_HERE.md)** - Master guide and feature overview
- **[QUICKSTART.md](docs/QUICKSTART.md)** - 5-minute setup guide
- **[PROJECT_README.md](docs/PROJECT_README.md)** - Complete reference with API documentation
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design and data flow
- **[PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)** - Comprehensive technical overview (1,200+ lines)

For file-by-file documentation, see [docs/FILES_REFERENCE.md](docs/FILES_REFERENCE.md).

## ✨ Features

✅ **Hybrid ML Pipeline** - LSTM + Isolation Forest for robust anomaly detection
✅ **Three Datasets** - HDFS, BGL, OpenStack pre-integrated
✅ **Real-time Dashboard** - Modern dark-theme React UI with live log streaming
✅ **Professional API** - 7 RESTful endpoints with full Swagger documentation
✅ **Docker Ready** - `docker-compose up` deployment
✅ **Modular Architecture** - Easy to extend and customize

## 📂 Project Structure

```
├── backend/                    Python FastAPI server
├── frontend/                   React Vite application
├── datasets/                   Sample log datasets (HDFS, BGL, OpenStack)
├── docker/                     Dockerfiles and docker-compose configuration
├── scripts/                    Startup automation scripts
├── docs/                       Complete documentation (1,200+ lines)
├── requirements.txt            Python dependencies
├── .gitignore                  Git configuration
└── README.md                   This file
```

## 🔧 Requirements

- Python 3.8+
- Node.js 16+
- 2GB RAM (for PyTorch models)

## 📖 Learn More

- Full architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- ML models explained: [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)
- API reference: [docs/PROJECT_README.md](docs/PROJECT_README.md)
- Project structure: [docs/PROJECT_TREE.md](docs/PROJECT_TREE.md)

---

**License**: MIT