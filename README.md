# Dockerized API with CI/CD

A production-ready FastAPI application with Docker containerization, comprehensive testing, and automated CI/CD pipelines using GitHub Actions.

## 🚀 Features

- **FastAPI** web service with structured JSON logging
- **Docker** containerization with optimized multi-stage builds
- **CI/CD** pipelines with GitHub Actions
- **Automated testing** with pytest
- **Code quality** checks with ruff
- **Production-ready** configuration management

## 📋 API Endpoints

### `GET /health`
Health check endpoint that returns the service status.

**Response:**
```json
{
  "status": "ok"
}
```

### `GET /info`
Returns service metadata including name, version, git SHA, and uptime.

**Response:**
```json
{
  "service_name": "dockerized-api",
  "version": "1.0.0",
  "git_sha": "abc123",
  "uptime_seconds": 123.45
}
```

### `POST /echo`
Echoes back a message with a timestamp.

**Request:**
```json
{
  "message": "Hello, World!"
}
```

**Response:**
```json
{
  "message": "Hello, World!",
  "timestamp": "2026-02-16T10:30:00"
}
```

## 🛠️ Local Development

### Prerequisites

- Python 3.11+
- pip
- Docker (optional, for containerized runs)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd dockerized-api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

1. **Set environment variables (optional):**
   ```bash
   # Windows PowerShell
   $env:SERVICE_NAME="my-api"
   $env:ENV="development"
   $env:LOG_LEVEL="DEBUG"
   $env:GIT_SHA="local-dev"
   
   # Linux/Mac
   export SERVICE_NAME="my-api"
   export ENV="development"
   export LOG_LEVEL="DEBUG"
   export GIT_SHA="local-dev"
   ```

2. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Health check: http://localhost:8000/health
   - API docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

### Test Coverage

The test suite includes:
- Unit tests for all endpoints
- JSON schema validation tests
- Request ID header verification
- Error handling tests

## 🐳 Docker

### Build Docker Image

```bash
docker build -t dockerized-api:latest .
```

### Run Docker Container

```bash
# Basic run
docker run -p 8000:8000 dockerized-api:latest

# With environment variables
docker run -p 8000:8000 \
  -e SERVICE_NAME="my-api" \
  -e ENV="production" \
  -e LOG_LEVEL="INFO" \
  -e GIT_SHA="abc123" \
  dockerized-api:latest

# Run in detached mode
docker run -d -p 8000:8000 --name my-api dockerized-api:latest
```

### Docker Compose (Optional)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SERVICE_NAME=dockerized-api
      - ENV=production
      - LOG_LEVEL=INFO
      - GIT_SHA=${GIT_SHA:-unknown}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with:
```bash
docker-compose up -d
```

## 🔄 CI/CD Pipeline

### Continuous Integration (CI)

The CI pipeline runs on every pull request and push to `main` or `develop` branches:

1. **Checkout code**
2. **Set up Python 3.11**
3. **Install dependencies**
4. **Run linter (ruff)** - Checks code quality
5. **Run tests (pytest)** - Executes test suite
6. **Build Docker image** - Validates Dockerfile
7. **Test Docker image** - Verifies container runs correctly

**Workflow file:** `.github/workflows/ci.yml`

### Continuous Deployment (CD)

The CD pipeline runs on every push to `main` branch:

1. **Checkout code**
2. **Set up Docker Buildx**
3. **Login to GitHub Container Registry (GHCR)**
4. **Extract metadata** - Generates tags and labels
5. **Get Git SHA** - Captures commit hash
6. **Build and push Docker image** - Pushes to GHCR with tags:
   - `latest` (for main branch)
   - `main-<sha>` (commit-specific)
   - `main` (branch name)

**Workflow file:** `.github/workflows/cd.yml`

### Accessing GHCR Images

After the CD pipeline runs, your Docker image will be available at:

```
ghcr.io/<your-username>/<repo-name>:latest
```

To pull and run:
```bash
docker pull ghcr.io/<your-username>/<repo-name>:latest
docker run -p 8000:8000 ghcr.io/<your-username>/<repo-name>:latest
```

**Note:** Make sure your GitHub repository has packages enabled and you have the necessary permissions.

## 🚢 Deployment to Render

### Option 1: Connect GitHub Repository (Recommended)

1. **Sign up/Login to Render:**
   - Go to https://render.com
   - Sign up or log in with your GitHub account

2. **Create a New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select this repository

3. **Configure the Service:**
   - **Name:** `dockerized-api` (or your preferred name)
   - **Environment:** `Docker`
   - **Region:** Choose your preferred region
   - **Branch:** `main`
   - **Root Directory:** Leave empty (or `.` if needed)
   - **Dockerfile Path:** `Dockerfile`
   - **Docker Context:** `.`

4. **Set Environment Variables:**
   ```
   SERVICE_NAME=dockerized-api
   ENV=production
   LOG_LEVEL=INFO
   GIT_SHA=<will be set automatically or leave empty>
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy your Docker image
   - Your service will be available at `https://<service-name>.onrender.com`

### Option 2: Deploy from GHCR Image

1. **Create a New Web Service:**
   - Click "New +" → "Web Service"
   - Select "Deploy an existing image from a registry"

2. **Configure:**
   - **Registry:** GitHub Container Registry
   - **Image:** `ghcr.io/<your-username>/<repo-name>:latest`
   - **Registry Credentials:** Add your GitHub Personal Access Token
     - Create token at: https://github.com/settings/tokens
     - Scopes needed: `read:packages`

3. **Set Environment Variables** (same as above)

4. **Deploy**

### Render Auto-Deploy

Render automatically deploys when you push to the connected branch (usually `main`). You can also trigger manual deployments from the Render dashboard.

## 📁 Project Structure

```
dockerized-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── schemas.py           # Pydantic models
│   └── logging_middleware.py # Structured logging middleware
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Test suite
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI pipeline
│       └── cd.yml           # CD pipeline
├── Dockerfile               # Docker image definition
├── .dockerignore            # Docker ignore patterns
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVICE_NAME` | Name of the service | `dockerized-api` |
| `ENV` | Environment (development/production) | `development` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `GIT_SHA` | Git commit SHA | `None` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## 📊 Logging

The application uses structured JSON logging. Each request is logged with:
- HTTP method
- Request path
- Status code
- Latency in milliseconds
- Unique request ID

Example log entry:
```json
{
  "level": "INFO",
  "method": "GET",
  "path": "/health",
  "status_code": 200,
  "latency_ms": 2.45,
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## 🧹 Code Quality

### Linting

```bash
# Run ruff linter
ruff check app/ tests/

# Auto-fix issues
ruff check app/ tests/ --fix
```

### Formatting

```bash
# Format code (if using ruff format)
ruff format app/ tests/
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

For issues and questions, please open an issue on GitHub.
