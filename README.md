# ⬡ TaskBoard — DevOps Capstone Project

A production-grade, SaaS-style project management application demonstrating the full DevOps lifecycle — from a developer laptop to a monitored Kubernetes environment on AWS.

```
Developer → Git/GitHub → GitHub Actions → Docker → Trivy → GHCR → Terraform → EKS → Helm → Prometheus/Grafana
```

---

## 📋 Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start (Docker Compose)](#quick-start-docker-compose)
- [Run Backend Locally](#run-backend-locally)
- [Run Frontend Locally](#run-frontend-locally)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variables)
- [Docker](#docker)
- [CI/CD Pipeline](#cicd-pipeline)
- [Terraform (AWS Infrastructure)](#terraform-aws-infrastructure)
- [Kubernetes & Helm](#kubernetes--helm)
- [Monitoring](#monitoring)
- [Troubleshooting Exercises](#troubleshooting-exercises)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        Developer Machine                      │
│                                                              │
│   React + Vite (port 3000) ──→ FastAPI (port 8000)          │
│                                      │                       │
│                               PostgreSQL (port 5432)         │
└──────────────────────────────────────────────────────────────┘
                          │
                    git push
                          │
                          ▼
              ┌─────────────────────┐
              │    GitHub Actions   │
              │  pytest → build →   │
              │  trivy → push GHCR  │
              └──────────┬──────────┘
                         │
                   terraform apply
                         │
                         ▼
              ┌─────────────────────┐
              │    AWS (ap-south-1) │
              │  VPC + EKS Cluster  │
              └──────────┬──────────┘
                         │
                  helm upgrade
                         │
              ┌──────────▼──────────┐
              │   Kubernetes (EKS)  │
              │                     │
              │  [Frontend Pods]    │
              │  [Backend Pods]  ←HPA│
              │  [PostgreSQL Pod]   │
              │  [Ingress]          │
              │  [Prometheus]       │
              │  [Grafana]          │
              └─────────────────────┘
```

## Features

### Application
- ✅ Dark-themed SaaS dashboard with sidebar navigation
- ✅ KPI cards (Total, Todo, In Progress, Review, Done, High Priority)
- ✅ Task table with inline status updates and priority badges
- ✅ Create task modal with full form validation
- ✅ Activity feed with real-time action log
- ✅ Pipeline status indicator
- ✅ Status filter bar
- ✅ Loading, empty, and error states
- ✅ Responsive CSS (mobile, tablet, desktop)

### Backend APIs
- ✅ `GET /` — Application info
- ✅ `GET /health` — Kubernetes liveness probe
- ✅ `GET /ready` — Kubernetes readiness probe (checks DB)
- ✅ `GET /metrics` — Prometheus metrics endpoint
- ✅ `GET /api/tasks` — List tasks (filterable)
- ✅ `GET /api/tasks/{id}` — Get single task
- ✅ `POST /api/tasks` — Create task
- ✅ `PUT /api/tasks/{id}` — Update task
- ✅ `DELETE /api/tasks/{id}` — Delete task
- ✅ `GET /api/tasks/stats` — Dashboard KPI statistics
- ✅ Swagger UI at `/docs`

### DevOps
- ✅ Docker Compose for full local stack
- ✅ Multi-stage Dockerfiles (backend + frontend)
- ✅ GitHub Actions CI/CD (test → build → scan → push → deploy)
- ✅ Trivy container security scanning (HIGH + CRITICAL CVEs)
- ✅ GitHub Container Registry image publishing
- ✅ Terraform for AWS VPC + EKS infrastructure
- ✅ Helm chart with liveness/readiness probes
- ✅ Kubernetes Ingress routing (`/` → frontend, `/api` → backend)
- ✅ Horizontal Pod Autoscaler (CPU-based)
- ✅ Prometheus + Grafana monitoring stack
- ✅ Troubleshooting exercises (broken image, broken service)
- ✅ Seed data script and load test script

---

## Prerequisites

| Tool | Version | Required For |
|------|---------|-------------|
| Docker Desktop | Latest | Local stack |
| Docker Compose | v2+ | Local stack |
| Python | 3.12+ | Backend dev |
| Node.js | 20+ | Frontend dev |
| kubectl | Latest | Kubernetes |
| Helm | v3.15+ | Deployment |
| Terraform | v1.6+ | AWS infra |
| AWS CLI | v2 | AWS access |

---

## Quick Start (Docker Compose)

The fastest way to run the **complete stack** locally:

```bash
# Clone and enter the project
cd C:\Users\kommi\Downloads\taskboard-capstone

# Start everything (PostgreSQL + Backend + Frontend)
docker compose up --build

# Seed with sample data (in a new terminal)
python scripts/seed-data.py

# Stop
docker compose down

# Stop and wipe database
docker compose down -v
```

### Access Points

| Service | URL |
|---------|-----|
| Frontend (React) | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |
| Readiness check | http://localhost:8000/ready |
| Prometheus metrics | http://localhost:8000/metrics |

---

## Run Backend Locally

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.venv\Scripts\activate.bat

# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set database connection
$env:DATABASE_URL = "postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard"

# Run Alembic migrations
alembic upgrade head

# Start FastAPI
uvicorn app.main:app --reload --port 8000
```

---

## Run Frontend Locally

```bash
cd frontend

# Install dependencies
npm install

# Start development server (proxies /api → http://localhost:8000)
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

---

## Running Tests

```bash
cd backend

# Activate virtual environment first (see above)

# Run all tests (uses in-memory SQLite — no PostgreSQL needed)
pytest -q

# Verbose output
pytest -v

# With coverage
pip install pytest-cov
pytest --cov=app --cov-report=term-missing
```

### Test Coverage

| Test | Description |
|------|-------------|
| `test_root` | Application root endpoint |
| `test_health` | Health check endpoint |
| `test_ready` | Readiness endpoint |
| `test_create_task` | POST /api/tasks |
| `test_list_tasks` | GET /api/tasks |
| `test_get_task` | GET /api/tasks/{id} |
| `test_update_task` | PUT /api/tasks/{id} |
| `test_delete_task` | DELETE /api/tasks/{id} |
| `test_task_stats` | GET /api/tasks/stats |
| `test_get_task_not_found` | 404 handling |
| `test_filter_tasks_by_status` | Query parameter filtering |
| `test_create_task_missing_title` | 422 validation error |

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard` |
| `BACKEND_PORT` | Backend port | `8000` |
| `FRONTEND_PORT` | Frontend dev port | `3000` |

**GitHub Actions Secrets** (set in repo Settings → Secrets → Actions):

| Secret | Description |
|--------|-------------|
| `KUBECONFIG` | Base64-encoded kubeconfig for EKS cluster |
| `AWS_ACCESS_KEY_ID` | AWS access key (for Terraform) |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key (for Terraform) |

---

## Docker

### Build Images Manually

```bash
# Backend
docker build -t taskboard-backend:local ./backend

# Frontend
docker build -t taskboard-frontend:local ./frontend
```

### Run Backend with External PostgreSQL

```powershell
docker run --rm -p 8000:8000 `
  -e DATABASE_URL="postgresql+psycopg://taskboard:taskboard@host.docker.internal:5432/taskboard" `
  taskboard-backend:local
```

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) runs on every push to `main`:

```
Push to main
     │
     ▼
  [test job]
  ├── pytest (backend)
  └── npm build (frontend)
     │
     ▼ (only on main)
  [build-scan-push job]
  ├── docker build backend
  ├── docker build frontend
  ├── trivy scan backend (HIGH+CRITICAL)
  ├── trivy scan frontend (HIGH+CRITICAL)
  ├── push backend → GHCR (tag: commit SHA)
  └── push frontend → GHCR (tag: commit SHA)
     │
     ▼ (only on main)
  [deploy job]
  └── helm upgrade --install taskboard
```

**Image tagging strategy:** Every commit produces a uniquely tagged image using the Git SHA, giving full traceability from production back to source code.

### Required GitHub Secrets

1. `KUBECONFIG` — Configure in repo Settings → Secrets → Actions
2. GHCR authentication is automatic via `GITHUB_TOKEN`

---

## Terraform (AWS Infrastructure)

```bash
cd terraform

# Initialize providers
terraform init

# Review planned changes
terraform plan

# Create infrastructure (VPC + EKS)
terraform apply

# Configure kubectl after creation
aws eks update-kubeconfig --region ap-south-1 --name taskboard-cluster

# Destroy when finished
terraform destroy
```

### Infrastructure Created

| Resource | Details |
|----------|---------|
| VPC | 10.0.0.0/16 CIDR |
| Public Subnets | 3× across AZs (for Load Balancer) |
| Private Subnets | 3× across AZs (for EKS nodes) |
| NAT Gateway | Single NAT for private subnet outbound |
| EKS Cluster | v1.30, API endpoint public |
| Node Group | t3.medium, 2 desired / 1 min / 5 max |

**Default region:** `ap-south-1` (Mumbai). Change in `terraform/variables.tf`.

---

## Kubernetes & Helm

### Bootstrap Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### Deploy with Helm

```bash
# Standard deployment
helm upgrade --install taskboard ./helm/taskboard \
  --namespace taskboard \
  --create-namespace

# Dev deployment with Ingress + ServiceMonitor enabled
helm upgrade --install taskboard ./helm/taskboard \
  --namespace taskboard \
  --create-namespace \
  -f helm/taskboard/values-dev.yaml

# Deploy specific image versions (from CI/CD)
helm upgrade --install taskboard ./helm/taskboard \
  --namespace taskboard \
  --set backend.image.tag=<git-sha> \
  --set frontend.image.tag=<git-sha>
```

### Inspect Deployment

```bash
kubectl get pods -n taskboard
kubectl get svc -n taskboard
kubectl get ingress -n taskboard
kubectl get hpa -n taskboard
helm list -n taskboard
```

### Ingress Routing

Add to `/etc/hosts` (or `C:\Windows\System32\drivers\etc\hosts` on Windows):
```
<INGRESS-EXTERNAL-IP>  taskboard.local
```

Then access: http://taskboard.local

---

## Monitoring

### Deploy Prometheus + Grafana

```bash
# Add Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f monitoring/prometheus-values.yaml

# Access Grafana (default password: taskboard-admin)
kubectl port-forward svc/prometheus-grafana 3001:80 -n monitoring
```

Open: http://localhost:3001 (admin / taskboard-admin)

### FastAPI Metrics

The backend exposes Prometheus metrics at `/metrics` automatically via `prometheus-fastapi-instrumentator`. The ServiceMonitor (enabled in `values-dev.yaml`) tells Prometheus to scrape it.

**Key metrics to watch:**
- `http_requests_total` — Request count by endpoint/status
- `http_request_duration_seconds` — Response time histogram
- `process_cpu_seconds_total` — CPU usage (triggers HPA)

---

## Troubleshooting Exercises

### Exercise 1: ImagePullBackOff

```bash
kubectl apply -f troubleshooting/broken-image.yaml
kubectl get pods -n taskboard
kubectl describe pod <pod-name> -n taskboard
kubectl get events --sort-by=.lastTimestamp -n taskboard
```

**Expected:** `ErrImagePull` / `ImagePullBackOff`
**Root cause:** Image tag `does-not-exist` doesn't exist
**Fix:** Update image tag to a valid one

### Exercise 2: Broken Service (label mismatch)

```bash
kubectl apply -f troubleshooting/broken-service.yaml
kubectl get svc -n taskboard
kubectl get endpoints -n taskboard
kubectl get pods --show-labels -n taskboard
```

**Expected:** Service exists but Endpoints list is empty
**Root cause:** Selector `app: backend-WRONG` matches no Pods
**Fix:** Change selector to `app: backend`

### Load Testing (HPA Demo)

```bash
# Linux/macOS
bash scripts/load-test.sh http://localhost:8000 60

# Watch HPA respond
kubectl get hpa -n taskboard -w
```

### Seed Sample Data

```bash
# With backend running at localhost:8000
python scripts/seed-data.py

# Custom URL
python scripts/seed-data.py --url http://taskboard.local
```

---

## API Reference

### Tasks

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/tasks` | List all tasks (supports `?status=`, `?priority=`, `?assignee=` filters) |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/{id}` | Get task by ID |
| PUT | `/api/tasks/{id}` | Update task fields |
| DELETE | `/api/tasks/{id}` | Delete task |
| GET | `/api/tasks/stats` | Dashboard KPI statistics |

### Task Schema

```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "status": "todo | in_progress | review | done",
  "priority": "low | medium | high | critical",
  "assignee": "string (optional)",
  "due_date": "YYYY-MM-DD (optional)",
  "tags": "comma-separated string (optional)"
}
```

### System

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | App info + uptime |
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness check (verifies DB) |
| GET | `/metrics` | Prometheus metrics |
| GET | `/docs` | Swagger UI |
| GET | `/openapi.json` | OpenAPI schema |

---

## Project Structure

```
taskboard-capstone/
├── frontend/                     # React + Vite SaaS dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx       # Dark sidebar
│   │   │   ├── Header.jsx        # Dashboard header
│   │   │   ├── KpiCards.jsx      # KPI statistics cards
│   │   │   ├── TaskTable.jsx     # Task list with status/priority
│   │   │   ├── CreateTaskModal.jsx # New task form
│   │   │   └── ActivityFeed.jsx  # Activity log + pipeline
│   │   ├── styles/
│   │   │   ├── global.css        # CSS reset + variables
│   │   │   └── app.css           # Component styles
│   │   ├── App.jsx               # Root component
│   │   └── main.jsx              # React entry point
│   ├── nginx.conf                # Production Nginx config
│   ├── Dockerfile                # Multi-stage build
│   ├── vite.config.js            # Vite + API proxy config
│   └── package.json
│
├── backend/                      # FastAPI Python backend
│   ├── app/
│   │   ├── main.py               # FastAPI app + all endpoints
│   │   ├── models.py             # SQLAlchemy ORM models
│   │   ├── schemas.py            # Pydantic request/response schemas
│   │   ├── database.py           # DB engine + session
│   │   └── __init__.py
│   ├── tests/
│   │   ├── test_tasks.py         # 12 pytest tests
│   │   └── __init__.py
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── 001_initial_schema.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── Dockerfile                # Python 3.12 non-root image
│   ├── alembic.ini
│   └── requirements.txt
│
├── docker-compose.yml            # Full local stack
├── .env.example                  # Environment variable template
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # GitHub Actions pipeline
│
├── terraform/                    # AWS VPC + EKS infrastructure
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── helm/taskboard/               # Kubernetes Helm chart
│   ├── Chart.yaml
│   ├── values.yaml               # Default values
│   ├── values-dev.yaml           # Dev overrides (Ingress + monitoring)
│   └── templates/
│       ├── namespace.yaml
│       ├── postgres.yaml         # PostgreSQL PVC + Deployment + Service
│       ├── backend.yaml          # Backend Deployment + Service + ServiceMonitor
│       ├── frontend.yaml         # Frontend Deployment + Service
│       ├── ingress.yaml          # Nginx Ingress
│       └── hpa.yaml              # HPA for backend
│
├── k8s/
│   └── namespace.yaml            # Namespace bootstrap
│
├── monitoring/
│   └── prometheus-values.yaml    # Prometheus + Grafana Helm values
│
├── troubleshooting/
│   ├── broken-image.yaml         # Exercise 1: ImagePullBackOff
│   └── broken-service.yaml       # Exercise 2: Label mismatch
│
└── scripts/
    ├── seed-data.py              # Populate with 12 sample tasks
    └── load-test.sh              # HPA load test script
```

---

## How to Run (Windows)

### Option A — Full stack with Docker (Recommended)

```powershell
cd C:\Users\kommi\Downloads\taskboard-capstone
docker compose up --build
```

Open http://localhost:3000

### Option B — Backend only (dev mode)

```powershell
cd C:\Users\kommi\Downloads\taskboard-capstone\backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL = "postgresql+psycopg://taskboard:taskboard@localhost:5432/taskboard"
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Option C — Frontend only (dev mode, backend must be running)

```powershell
cd C:\Users\kommi\Downloads\taskboard-capstone\frontend
npm install
npm run dev
```

---

## Known Limitations & Manual Steps

| Item | Status | Notes |
|------|--------|-------|
| AWS Deployment | Requires AWS credentials | Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` |
| GitHub Actions deploy job | Requires `KUBECONFIG` secret | Must point to a live EKS cluster |
| Helm image repository | Must be updated | Change `YOUR_GITHUB_USERNAME` in `helm/taskboard/values.yaml` |
| Ingress | Requires nginx-ingress-controller | `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.1/deploy/static/provider/cloud/deploy.yaml` |
| HPA | Requires Metrics Server | `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml` |
| Grafana dashboards | Manual setup | Import via Grafana UI or provision via config |

---

## Git Status

```bash
# Initialize and commit locally (do NOT push until ready)
git init
git add .
git commit -m "initial TaskBoard capstone implementation"
git branch -M main

# Only when ready:
# git remote add origin <YOUR_GITHUB_REPO>
# git push -u origin main
```

---

*Built as a DevOps Final Capstone project — demonstrating the complete software delivery lifecycle from code to monitored Kubernetes production environment.*
