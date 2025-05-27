# Smart Article Search - Version 2.0

This updated version enhances the original Smart Article Search by integrating Kubernetes to orchestrate and manage all services (backend, frontend, Elasticsearch) within a cluster. It demonstrates real-world container orchestration and deployment best practices using Minikube for local Kubernetes management and monitoring.
## New Features in Version 2.0

- **Kubernetes Integration**: The backend, frontend, and Elasticsearch are deployed as Kubernetes pods, managed by Deployments for scalability and self-healing.
- **Services for Communication**: Each component is exposed through Kubernetes Services to enable networking between pods and external access where needed.
- **ConfigMaps and Secrets**: Application configuration and sensitive environment variables (such as credentials) are securely stored and injected using Kubernetes ConfigMaps and Secrets.
- **Minikube Dashboard Visualization**: The Minikube dashboard provides a visual interface to monitor pods, deployments, services, and cluster health in real-time.

## Tech Stack (Version 2.0)

- **Container Orchestration**: Kubernetes (Minikube)
- **Backend**: FastAPI (containerized & deployed on Kubernetes)
- **Frontend**: Streamlit (containerized & deployed on Kubernetes)
- **Search Engine**: Elasticsearch (deployed in Kubernetes)
- **Configuration Management**: Kubernetes ConfigMaps & Secrets
- **Visualization**: Minikube Kubernetes Dashboard

## Prerequisites

Before running the project, make sure you have the following installed:

- Docker
- Docker Compose
- Kubectl
- minikube

## How to Run Version 2.0


### 1. Build Docker Images

```bash
docker build -t smart-article-backend:latest ./backend
docker build -t smart-article-frontend:latest ./frontend
docker build -t smart-article-elasticsearch:latest ./elasticsearch
```


### 2. Load Images into Minikube

```bash
minikube image load smart-article-backend:latest
minikube image load smart-article-frontend:latest
minikube image load smart-article-elasticsearch:latest
```


### 3. Apply yaml files
```bash
kubectl apply -f k8s/
```


### 4. Verify Deployment Status
```bash
kubectl get pods
kubectl get services
```


### 5. Monitor with Minikube Dashboard
```bash
minikube dashboard
```


## Project Structure
```bash
│── backend/                  # Backend logic
│   ├── api/                  # API-related files
│   │   ├── routes.py
│   │   ├── guardian_api.py
│   │   ├── models.py
│   ├── db/
│   │   ├── insert_data.py
│   ├── main.py               # FastAPI app entry point
    │── Dockerfile                # Dockerfile for building the backend
│── frontend/                 # Streamlit interface
│   ├── app.py                # Main Streamlit file
    │── Dockerfile                # Dockerfile for building the frontend
│── docker-compose.yml        # Docker Compose configuration
│── requirements.txt          # List of required Python packages
│── .env                      # Environment variables for configuration
│── README.md                 # Project documentation
```
