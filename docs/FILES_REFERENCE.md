# 📋 Project Files Reference Guide

## 🎯 Quick Navigation

This guide explains every file in the project and its purpose.

---

## 📂 Backend Files (Python)

### Core Application
| File | Purpose | Lines |
|------|---------|-------|
| `backend/main.py` | FastAPI application setup, routes, startup events | 60 |
| `backend/config.py` | Configuration constants and paths | 30 |
| `backend/__init__.py` | Package marker | 1 |

### API Layer (`backend/api/`)
| File | Purpose | Lines |
|------|---------|-------|
| `backend/api/routes.py` | All 7 API endpoints implementation | 250 |
| `backend/api/schemas.py` | Pydantic models for request/response validation | 100 |
| `backend/api/__init__.py` | Package marker | 1 |

### Log Processing (`backend/parsers/`)
| File | Purpose | Lines |
|------|---------|-------|
| `backend/parsers/drain_parser.py` | Drain-like log parsing algorithm | 120 |
| `backend/parsers/dataset_loader.py` | Load HDFS, BGL, OpenStack datasets | 140 |
| `backend/parsers/__init__.py` | Package marker | 1 |

### ML Models (`backend/models/`)
| File | Purpose | Lines |
|------|---------|-------|
| `backend/models/lstm_model.py` | LSTM model implementation (PyTorch) | 250 |
| `backend/models/isolation_forest.py` | Isolation Forest implementation (Scikit-learn) | 140 |
| `backend/models/__init__.py` | Package marker | 1 |

### Processing Pipeline (`backend/pipeline/`)
| File | Purpose | Lines |
|------|---------|-------|
| `backend/pipeline/sequence_generator.py` | Generate fixed-length sequences from logs | 180 |
| `backend/pipeline/feature_encoder.py` | Feature extraction and normalization | 150 |
| `backend/pipeline/anomaly_detector.py` | Hybrid anomaly detection (combine models) | 180 |
| `backend/pipeline/__init__.py` | Package marker | 1 |

---

## 🎨 Frontend Files (React/JavaScript)

### Configuration
| File | Purpose | Lines |
|------|---------|-------|
| `frontend/package.json` | NPM dependencies and scripts | 25 |
| `frontend/vite.config.js` | Vite bundler configuration | 18 |
| `frontend/tailwind.config.js` | TailwindCSS theme configuration | 30 |
| `frontend/postcss.config.js` | PostCSS configuration for Tailwind | 8 |
| `frontend/index.html` | HTML entry point | 15 |

### Global Styles & Entry
| File | Purpose | Lines |
|------|---------|-------|
| `frontend/src/index.css` | Global styles, animations, utilities | 120 |
| `frontend/src/main.jsx` | React entry point, render root | 10 |
| `frontend/src/App.jsx` | Main app component with routing | 70 |

### API Service (`frontend/src/services/`)
| File | Purpose | Lines |
|------|---------|-------|
| `frontend/src/services/apiService.js` | Axios API client for all endpoints | 40 |

### Components (`frontend/src/components/`)
| File | Purpose | Lines |
|------|---------|-------|
| `frontend/src/components/Sidebar.jsx` | Navigation sidebar with menu | 70 |
| `frontend/src/components/DatasetSelector.jsx` | Dataset selection cards | 80 |
| `frontend/src/components/StatCard.jsx` | Reusable stat display card | 40 |
| `frontend/src/components/AnomalyChart.jsx` | Line/Area chart for anomalies | 90 |
| `frontend/src/components/LiveLogStream.jsx` | Real-time log streaming display | 120 |
| `frontend/src/components/LogsViewer.jsx` | Table with logs and pagination | 150 |

### Pages (`frontend/src/pages/`)
| File | Purpose | Lines |
|------|---------|-------|
| `frontend/src/pages/Dashboard.jsx` | Main dashboard page | 120 |
| `frontend/src/pages/Analysis.jsx` | Model metrics and insights page | 280 |
| `frontend/src/pages/Logs.jsx` | Logs explorer page | 100 |
| `frontend/src/pages/Settings.jsx` | Settings configuration page | 150 |

---

## 📚 Documentation Files

| File | Purpose | Size |
|------|---------|------|
| `PROJECT_README.md` | Complete documentation (650+ lines) | 650+ |
| `QUICKSTART.md` | Quick setup guide (80 lines) | 80+ |
| `COMPLETED.md` | Project completion summary | 450+ |
| `ARCHITECTURE.md` | System architecture diagrams | 500+ |
| `README.md` | Original project README | 50+ |

---

## 🔧 Configuration & Setup Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies (13 packages) |
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore patterns |
| `docker-compose.yml` | Docker Compose multi-container setup |
| `Dockerfile.backend` | Backend container definition |
| `Dockerfile.frontend` | Frontend container definition |
| `start.sh` | Linux/Mac startup script |
| `start.bat` | Windows startup script |

---

## 📊 Datasets

| Directory | Contents | Format |
|-----------|----------|--------|
| `datasets/HDFS_v1/` | HDFS logs (11,175 sequences) | CSV + preprocessed |
| `datasets/BGL/` | BGL logs (~4.7M events) | Log file |
| `datasets/OpenStack/` | OpenStack logs (207K events) | Log file + labels |

---

## 🎯 Purpose of Each File Category

### Backend Core
- **main.py**: Entry point, FastAPI setup
- **config.py**: Centralized configuration

### Parsing Layer
- **drain_parser.py**: Parse raw logs into templates
- **dataset_loader.py**: Load and normalize different dataset formats

### Processing Pipeline
- **sequence_generator.py**: Convert logs to fixed-length sequences
- **feature_encoder.py**: Extract and normalize features

### ML Models
- **lstm_model.py**: Sequential anomaly detection
- **isolation_forest.py**: Statistical anomaly detection
- **anomaly_detector.py**: Hybrid scoring and classification

### Frontend Components
- **Sidebar.jsx**: Navigation
- **DatasetSelector.jsx**: Dataset selection UI
- **StatCard.jsx**: Metric display
- **AnomalyChart.jsx**: Data visualization
- **LiveLogStream.jsx**: Real-time log display
- **LogsViewer.jsx**: Detailed logs table

### Frontend Pages
- **Dashboard.jsx**: Overview and monitoring
- **Analysis.jsx**: Model metrics and insights
- **Logs.jsx**: Log search and filtering
- **Settings.jsx**: Configuration

---

## 🚀 Key File Statistics

| Metric | Count |
|--------|-------|
| **Total Files** | 35+ |
| **Python Files** | 12 |
| **React Components** | 10 |
| **Documentation Files** | 4 |
| **Configuration Files** | 8 |
| **Lines of Code** | 3,500+ |
| **Total Packages** | 20+ (Python) + 6 (Node) |

---

## 📋 Loading Order (for understanding)

### To Understand the Backend
1. `backend/config.py` - Understand configuration
2. `backend/main.py` - Entry point
3. `backend/api/schemas.py` - Data models
4. `backend/api/routes.py` - API endpoints
5. `backend/parsers/drain_parser.py` - Log parsing
6. `backend/pipeline/sequence_generator.py` - Sequences
7. `backend/pipeline/feature_encoder.py` - Features
8. `backend/models/lstm_model.py` - LSTM
9. `backend/models/isolation_forest.py` - Isolation Forest
10. `backend/pipeline/anomaly_detector.py` - Hybrid detection

### To Understand the Frontend
1. `frontend/src/index.css` - Styling
2. `frontend/src/App.jsx` - App structure
3. `frontend/src/components/Sidebar.jsx` - Navigation
4. `frontend/src/pages/Dashboard.jsx` - Main page
5. `frontend/src/services/apiService.js` - API calls
6. `frontend/src/components/` - UI components
7. `frontend/src/pages/` - Other pages

---

## 🔗 File Dependencies

```
main.py (entry point)
  └─ config.py
  └─ api/routes.py
      └─ api/schemas.py
      └─ parsers/dataset_loader.py
      └─ parsers/drain_parser.py
      └─ pipeline/sequence_generator.py
      └─ pipeline/feature_encoder.py
      └─ pipeline/anomaly_detector.py
          ├─ models/lstm_model.py
          └─ models/isolation_forest.py
```

---

## 💾 File Size Guide

| Category | Total Size | File Count |
|----------|-----------|-----------|
| Backend Code | ~2,100 lines | 12 files |
| Frontend Code | ~1,100 lines | 10 files |
| Documentation | ~2,000 lines | 4 files |
| Config/Setup | ~300 lines | 8 files |

---

## 🎓 Learning Path

### Beginner
1. Read `QUICKSTART.md` for setup
2. Read `PROJECT_README.md` sections 1-3
3. Run the application
4. Explore UI in browser

### Intermediate
1. Read `ARCHITECTURE.md` for design
2. Examine `backend/config.py` and `backend/main.py`
3. Check `frontend/src/App.jsx` and routing
4. Review one API endpoint in `backend/api/routes.py`

### Advanced
1. Study `backend/pipeline/anomaly_detector.py`
2. Understand `backend/models/lstm_model.py`
3. Review `backend/parsers/drain_parser.py`
4. Examine feature engineering in `backend/pipeline/feature_encoder.py`
5. Trace data flow through ML models

### Expert
1. Modify ML model parameters
2. Add new dataset support
3. Implement model training
4. Extend UI components
5. Deploy to production

---

## 📝 Documentation Quick Links

- **Getting Started**: See `QUICKSTART.md`
- **Full Documentation**: See `PROJECT_README.md`
- **Architecture**: See `ARCHITECTURE.md`
- **Project Summary**: See `COMPLETED.md`

---

## ✅ Verification Checklist

To verify all files are present:

```bash
# Backend
✓ backend/main.py
✓ backend/config.py
✓ backend/__init__.py
✓ backend/api/routes.py
✓ backend/api/schemas.py
✓ backend/api/__init__.py
✓ backend/parsers/drain_parser.py
✓ backend/parsers/dataset_loader.py
✓ backend/parsers/__init__.py
✓ backend/models/lstm_model.py
✓ backend/models/isolation_forest.py
✓ backend/models/__init__.py
✓ backend/pipeline/sequence_generator.py
✓ backend/pipeline/feature_encoder.py
✓ backend/pipeline/anomaly_detector.py
✓ backend/pipeline/__init__.py

# Frontend
✓ frontend/package.json
✓ frontend/vite.config.js
✓ frontend/tailwind.config.js
✓ frontend/postcss.config.js
✓ frontend/index.html
✓ frontend/src/index.css
✓ frontend/src/main.jsx
✓ frontend/src/App.jsx
✓ frontend/src/services/apiService.js
✓ frontend/src/components/*.jsx (6 files)
✓ frontend/src/pages/*.jsx (4 files)

# Documentation
✓ PROJECT_README.md
✓ QUICKSTART.md
✓ COMPLETED.md
✓ ARCHITECTURE.md

# Configuration
✓ requirements.txt
✓ .env.example
✓ .gitignore
✓ docker-compose.yml
✓ Dockerfile.backend
✓ Dockerfile.frontend
✓ start.sh
✓ start.bat
```

---

**Total Project**: 35+ files, 3,500+ lines of code, fully documented and ready to deploy! 🚀
