# Deployment Guide — Visual Regression Testing System

**Author:** Shashwat Rana (23fe10cse00101)  
**Course:** CSE3253 DevOps [PE6] | Semester VI (2025–2026)

---

## Table of Contents

1. [Local Development Deployment](#1-local-development-deployment)
2. [Docker Deployment](#2-docker-deployment)
3. [Render.com Cloud Deployment](#3-rendercom-cloud-deployment)
4. [GitHub Actions CI/CD Pipeline](#4-github-actions-cicd-pipeline)
5. [Environment Variables](#5-environment-variables)
6. [Production Checklist](#6-production-checklist)

---

## 1. Local Development Deployment

### Prerequisites
- Python 3.10+
- Google Chrome (latest stable)
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/devops_vrts.git
cd devops_vrts

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask development server
python app.py
```

The dashboard is available at **http://localhost:5000**.

---

## 2. Docker Deployment

### Build & Run

```bash
# Build the Docker image
docker build -t vrts .

# Run the container
docker run -p 5000:5000 vrts
```

### Persist Screenshots

```bash
docker run -p 5000:5000 \
  -v $(pwd)/screenshots:/app/screenshots \
  vrts
```

### Docker Compose (optional)

Create `docker-compose.yml` in the project root:

```yaml
version: "3.9"
services:
  vrts:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./screenshots:/app/screenshots
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

Then run:

```bash
docker compose up -d
```

---

## 3. Render.com Cloud Deployment

The project includes a `render.yaml` blueprint that enables **one-click deployment** from GitHub.

### Steps

1. **Push your repository to GitHub.**

2. **Log in to [Render.com](https://render.com/).**

3. Click **New → Blueprint** and connect your GitHub repository.

4. Render will read `render.yaml` automatically and create the service.

5. The service will build the Docker image and deploy it. Once live, you'll receive a public URL like:
   ```
   https://vrts-dashboard.onrender.com
   ```

> **✅ This project is already deployed at: [https://vrts-dashboard.onrender.com](https://vrts-dashboard.onrender.com)**

### `render.yaml` Reference

```yaml
services:
  - type: web
    name: vrts-dashboard
    runtime: docker
    dockerfilePath: ./Dockerfile
    plan: free
    envVars:
      - key: PYTHONUNBUFFERED
        value: "1"
      - key: FLASK_ENV
        value: "production"
```

> **Note:** The free plan on Render spins down after 15 minutes of inactivity. The first request after spin-down may be slow (cold start).

---

## 4. GitHub Actions CI/CD Pipeline

The pipeline (`.github/workflows/ci.yml`) runs automatically on every push or pull request to `main`.

### Pipeline Steps

| Step                    | Description                                      |
|-------------------------|--------------------------------------------------|
| Checkout repository     | Fetches the latest code                          |
| Set up Python 3.12      | Configures the Python version                    |
| Install Google Chrome   | Installs Chrome from Google's official repository|
| Install dependencies    | `pip install -r requirements.txt`                |
| Run CLI smoke test      | `python cli.py --url https://example.com`        |
| Upload screenshots      | Saves captured screenshots as CI artifacts       |

### Triggering a Manual Run

You can manually trigger the workflow from the **Actions** tab in GitHub:  
Repository → Actions → "CI — Visual Regression Tests" → **Run workflow**.

---

## 5. Environment Variables

| Variable            | Default       | Description                                 |
|---------------------|---------------|---------------------------------------------|
| `FLASK_ENV`         | `development` | Set to `production` for production deployments |
| `PYTHONUNBUFFERED`  | `1`           | Ensures logs stream in real time in Docker  |
| `FLASK_DEBUG`       | `0`           | Set to `1` only for local debugging         |

---

## 6. Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Use Gunicorn (not Flask's dev server) — already configured in `Dockerfile`
- [ ] Serve behind a reverse proxy (nginx/Caddy) for TLS/SSL
- [ ] Mount a persistent volume for `screenshots/`
- [ ] Consider rate-limiting on `/run-test` to prevent abuse
- [ ] Rotate screenshot storage periodically to avoid disk fill
- [ ] Monitor with a health-check endpoint (add `/health` route returning `200 OK`)
