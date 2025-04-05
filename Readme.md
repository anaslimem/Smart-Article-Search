# Smart Article Search

This project is a simple news search engine built using **FastAPI**, **Streamlit**, and **Elasticsearch**. It allows users to index and search for articles through a web interface, making it an ideal showcase for utilizing Elasticsearch in a real-world application.

## Features

- **Index Articles**: Allows you to index articles into Elasticsearch.
- **Search Articles**: Allows you to search for articles by title, content, or source.
- **Delete Index**: Allows you to delete the Elasticsearch index.

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Search Engine**: Elasticsearch
- **Docker**: Docker Compose for multi-container setup

## Prerequisites

Before running the project, make sure you have the following installed:

- Docker
- Docker Compose

## How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```
### 2. Build and Start the Docker Containers

In the project root directory, run:

```bash
docker-compose up --build
```
This command will:
 - Build the Docker images using the Dockerfile.

 - Start the application with the newssearchengine service and Elasticsearch service.

### 3. Stopping the Containers
```bash
docker-compose down
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
