#!/usr/bin/env python3
"""
Seed script: populates TaskBoard with sample tasks for demo purposes.
Usage:
    python scripts/seed-data.py [--url http://localhost:8000]
"""
import argparse
import json
import urllib.request
import urllib.error

SAMPLE_TASKS = [
    {"title": "Set up CI/CD pipeline", "description": "Configure GitHub Actions workflow with pytest and Docker build stages", "status": "done", "priority": "critical", "assignee": "alice", "due_date": "2026-10-01", "tags": "devops,ci-cd"},
    {"title": "Design database schema", "description": "Create ERD and implement SQLAlchemy models with Alembic migrations", "status": "done", "priority": "high", "assignee": "bob", "due_date": "2026-10-05", "tags": "backend,database"},
    {"title": "Implement REST API", "description": "FastAPI endpoints for CRUD operations on tasks with validation", "status": "done", "priority": "high", "assignee": "alice", "due_date": "2026-10-10", "tags": "backend,api"},
    {"title": "Build React dashboard", "description": "SaaS-style dark themed UI with KPI cards and task table", "status": "in_progress", "priority": "high", "assignee": "carol", "due_date": "2026-10-20", "tags": "frontend,ui"},
    {"title": "Write Terraform infrastructure", "description": "AWS VPC, EKS cluster, and node groups using Terraform modules", "status": "in_progress", "priority": "high", "assignee": "bob", "due_date": "2026-10-25", "tags": "terraform,aws,infrastructure"},
    {"title": "Create Helm chart", "description": "Package Kubernetes manifests into a reusable Helm chart", "status": "in_progress", "priority": "medium", "assignee": "alice", "due_date": "2026-10-28", "tags": "helm,kubernetes"},
    {"title": "Configure Prometheus monitoring", "description": "Deploy kube-prometheus-stack and configure ServiceMonitor for FastAPI", "status": "review", "priority": "medium", "assignee": "carol", "due_date": "2026-11-01", "tags": "monitoring,prometheus"},
    {"title": "Set up Grafana dashboards", "description": "Create dashboards for HTTP metrics, error rates, and HPA scaling", "status": "review", "priority": "medium", "assignee": "bob", "due_date": "2026-11-05", "tags": "monitoring,grafana"},
    {"title": "Security scan integration", "description": "Add Trivy scanning for HIGH and CRITICAL CVEs in pipeline", "status": "todo", "priority": "high", "assignee": "alice", "due_date": "2026-11-10", "tags": "security,trivy"},
    {"title": "Configure Ingress controller", "description": "Install nginx-ingress and configure routing for frontend and API", "status": "todo", "priority": "medium", "assignee": "carol", "due_date": "2026-11-12", "tags": "kubernetes,ingress"},
    {"title": "Test HPA autoscaling", "description": "Run load test and verify HPA scales backend pods under CPU pressure", "status": "todo", "priority": "medium", "assignee": "bob", "due_date": "2026-11-15", "tags": "kubernetes,hpa,testing"},
    {"title": "Prepare final presentation", "description": "Demo walkthrough: git to CI to Docker to security scan to GHCR to EKS to Helm to monitoring", "status": "todo", "priority": "critical", "assignee": "alice", "due_date": "2026-11-20", "tags": "presentation"},
]


def seed(base_url: str):
    print(f"[+] Seeding TaskBoard at {base_url}")
    success = 0
    for task in SAMPLE_TASKS:
        data = json.dumps(task).encode()
        req = urllib.request.Request(
            f"{base_url}/api/tasks",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
                print(f"  Created [{result['id']:>3}] {task['title']}")
                success += 1
        except urllib.error.HTTPError as e:
            print(f"  Failed: {task['title']} -- {e}")

    print(f"\n[+] Done: {success}/{len(SAMPLE_TASKS)} tasks created")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000", help="Backend base URL")
    args = parser.parse_args()
    seed(args.url)
