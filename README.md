# Visual Regression Testing System

> **Student Name:** Shashwat Rana  
> **Registration No:** 23fe10cse00101  
> **Course:** CSE3253 DevOps [PE6]  
> **Semester:** VI (2025–2026)  
> **Project Type:** Docker & CI/CD — Containerised Deployment with GitHub Actions  
> **Difficulty:** Intermediate

---

## 📋 Project Overview

### Problem Statement

Modern web applications undergo continuous changes — UI updates, CSS resets, dependency upgrades — any of which can silently break the visual appearance of pages. Manual QA cannot match the speed of continuous delivery. This project solves the problem by building an **automated Visual Regression Testing System (VRTS)** that captures screenshots of web pages and compares them pixel-by-pixel against stored baselines, detecting unintended visual changes before they reach production.

### Objectives

- [x] Build a unified testing engine that works in both CLI and Web Dashboard modes
- [x] Automatically detect visual differences using OpenCV pixel comparison
- [x] Generate highlighted diff images showing exactly which regions changed
- [x] Containerise the application with Docker (including headless Chrome)
- [x] Integrate with GitHub Actions for automated CI/CD testing on every push
- [x] Deploy to a cloud platform (Render.com) via Docker blueprint

### Key Features

- 🖥️ **Web Dashboard** — Flask-powered UI with URL input, screenshot viewer, and Chart.js result graphs
- ⌨️ **CLI Mode** — Single-command testing for use in terminal or CI pipelines
- 📸 **Selenium Engine** — Headless Chrome captures pixel-perfect screenshots at 1920×1080
- 🔍 **OpenCV Comparison** — Detects pixel-level visual differences with configurable thresholds
- 🔴 **Diff Images** — Changed regions are highlighted in red for instant visual feedback
- 🐳 **Docker Ready** — Containerised with Chrome pre-installed; works the same everywhere
- ⚙️ **CI/CD Pipeline** — GitHub Actions runs smoke tests on every push to `main`
- ☁️ **Cloud Deployment** — One-click deploy to Render.com via `render.yaml` blueprint

---

## 🛠️ Technology Stack

| Layer            | Technology                  | Version  | Purpose                           |
|------------------|-----------------------------|----------|-----------------------------------|
| Language         | Python                      | 3.12     | Application logic                 |
| Web Framework    | Flask                       | 3.1.0    | Web dashboard & REST API          |
| Browser Engine   | Selenium                    | 4.27.1   | Headless Chrome automation        |
| Image Processing | OpenCV (headless)           | 4.10     | Pixel comparison & diff rendering |
| Image Utility    | Pillow                      | 11.1.0   | Image loading support             |
| Numerical        | NumPy                       | 2.2.1    | Pixel count calculations          |
| Driver Manager   | webdriver-manager           | 4.0.2    | Auto-install ChromeDriver         |
| WSGI Server      | Gunicorn                    | 23.0.0   | Production Flask server           |
| Containerisation | Docker                      | 20+      | Consistent runtime environment    |
| CI/CD            | GitHub Actions              | —        | Automated testing pipeline        |
| Cloud Hosting    | Render.com                  | —        | Cloud deployment target           |
| Frontend Charts  | Chart.js (CDN)              | —        | Dashboard visualisation           |

---

## 🚀 Quick Start

### 1 · Install Dependencies

```bash
pip install -r requirements.txt
```

### 2 · CLI Usage

```bash
python cli.py --url https://example.com
```

### 3 · Web Dashboard

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### 4 · Docker

```bash
docker build -t vrts .
docker run -p 5000:5000 vrts
```

---

## 📁 Project Structure

```
devops_vrts/
├── app.py                       # Flask web dashboard & REST API
├── cli.py                       # Command-line interface
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration (Python + Chrome)
├── render.yaml                  # Render.com cloud deployment blueprint
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline
├── engine/
│   ├── __init__.py
│   ├── selenium_runner.py       # Headless Chrome screenshot capture
│   ├── image_compare.py         # OpenCV image comparison engine
│   └── result_manager.py        # Test result tracking & statistics
├── templates/
│   ├── index.html               # Dashboard homepage
│   └── results.html             # Test results page
├── static/
│   ├── css/styles.css           # Dashboard stylesheet
│   └── js/dashboard.js          # Chart.js integration
├── screenshots/
│   ├── baseline/                # Reference screenshots
│   ├── current/                 # Latest test screenshots
│   └── diff/                    # Highlighted difference images
└── docs/
    ├── userguide.md             # User Guide
    ├── apidocumentation.md      # API Documentation
    ├── designdocument.md        # Design Document
    ├── deployment.md            # Deployment Guide
    ├── troubleshooting.md       # Troubleshooting Guide
    └── architecture/
        └── architecture_diagrams.md  # System Architecture Diagrams
```

---

## 📚 Documentation

### User Documentation

- [User Guide](docs/userguide.md)
- [API Documentation](docs/apidocumentation.md)

### Technical Documentation

- [Design Document](docs/designdocument.md)
- [Architecture Diagrams](docs/architecture/)

### DevOps Documentation

- [Deployment Guide](docs/deployment.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

---

## 🔄 How It Works

```
1. User provides a URL
       │
       ▼
2. Selenium captures a screenshot (headless Chrome)
       │
       ▼
3. No baseline? → Save as baseline → PASS (first run)
       │
       ▼
4. Baseline exists? → OpenCV pixel comparison
       │
       ├── diff % ≤ 0.5% → ✅ PASS
       └── diff % > 0.5% → ❌ FAIL + red diff image
```

---

## ⚙️ CI/CD Pipeline

On every push to `main`, GitHub Actions:

1. ✅ Checks out the repository
2. ✅ Sets up Python 3.12
3. ✅ Installs Google Chrome
4. ✅ Installs Python dependencies
5. ✅ Runs a CLI smoke test against `https://example.com`
6. ✅ Uploads screenshots as CI artifacts (retained 7 days)

---

## 🐳 Docker & Cloud Deployment

- **Dockerfile** — Multi-layer build with Python 3.12 + headless Chrome + Gunicorn
- **render.yaml** — One-click Render.com deployment blueprint (Docker-based, free plan)

See [Deployment Guide](docs/deployment.md) for detailed instructions.

---

## License

MIT
