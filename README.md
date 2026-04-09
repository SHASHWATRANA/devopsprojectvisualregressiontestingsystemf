# Visual Regression Testing System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-vrts--dashboard.onrender.com-brightgreen?style=for-the-badge&logo=render)](https://vrts-dashboard.onrender.com)
[![CI](https://github.com/SHASHWATRANA/devopsprojectvisualregressiontestingsystemf/actions/workflows/ci.yml/badge.svg)](https://github.com/SHASHWATRANA/devopsprojectvisualregressiontestingsystemf/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)](https://hub.docker.com)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

> **Student Name:** Shashwat Rana  
> **Registration No:** 23fe10cse00101  
> **Course:** CSE3253 DevOps [PE6]  
> **Semester:** VI (2025–2026)  
> **Project Type:** Docker & CI/CD — Containerised Deployment with GitHub Actions  
> **Difficulty:** Intermediate

---

## 🚀 Live Deployment

> **🌐 [https://vrts-dashboard.onrender.com](https://vrts-dashboard.onrender.com)**

The application is deployed on **Render.com** using Docker. Click the link above to open the live dashboard.

> ⚠️ *Free tier: may take ~50 s to wake from idle. Refresh if the page is slow on first load.*

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
│
├── README.md                           # Main project documentation
├── .gitignore                          # Git ignore file
├── LICENSE                             # MIT License
│
├── src/                                # Source code
│   ├── main/
│   │   ├── app.py                      # Flask web dashboard & REST API
│   │   ├── cli.py                      # Command-line interface
│   │   ├── config/                     
│   │   │   ├── requirements.txt        # Python dependencies
│   │   │   └── render.yaml             # Render.com cloud deployment blueprint
│   │   ├── engine/                     # Core testing engine
│   │   │   ├── selenium_runner.py      
│   │   │   ├── image_compare.py        
│   │   │   └── result_manager.py       
│   │   ├── static/                     # CSS & JS assets
│   │   ├── templates/                  # HTML dashboard templates
│   │   └── screenshots/                # Generated screenshots (baseline/current/diff)
│   ├── test/                           
│   └── scripts/                        
│
├── infrastructure/                     # Infrastructure as Code
│   └── docker/                         
│       ├── Dockerfile                  # Container configuration (Python 3.12 + Chrome)
│       └── docker-compose.yml          
│
├── pipelines/                          # CI/CD Pipeline definitions
│   ├── Jenkinsfile                     # Jenkins declarative pipeline
│   └── .github/workflows/              
│       └── ci.yml                      # GitHub Actions automated workflow
│
├── tests/                              # Test suites
│   ├── unit/                           
│   ├── integration/                    
│   ├── selenium/                       
│   └── testdata/                       
│
├── docs/                               # Documentation
│   ├── projectplan.md                  # Project plan and timeline
│   ├── designdocument.md               # Technical design document
│   ├── userguide.md                    # User guide
│   ├── apidocumentation.md             # API documentation
│   ├── architecture/                   # Architecture diagrams
│   │   └── ARCHITECTURE.jpg            # System architecture diagram
│   └── screenshots/                    
│
├── presentations/                      # Presentation materials
│   └── Visual-Regression-Testing-System-VRTS.pptx.pptx  # Project presentation
│
└── deliverables/                       # Final deliverables
    ├── final-report.md                 # Technical project report
    ├── deployment-guide.md             # Cloud & Docker deployment instructions
    ├── troubleshooting-guide.md        # Debugging and FAQ guide
    └── assessment/                     
```

---

## 📚 Documentation

### Core Documentation

- [User Guide](docs/userguide.md)
- [API Documentation](docs/apidocumentation.md)
- [Design Document](docs/designdocument.md)
- [Project Plan](docs/projectplan.md)

### Deployment & Operations

- [Deployment Guide](deliverables/deployment-guide.md)
- [Troubleshooting Guide](deliverables/troubleshooting-guide.md)

### Architecture

- [Architecture Diagram](docs/architecture/ARCHITECTURE.jpg)

### Presentations & Reports

- [Project Presentation (PPTX)](presentations/Visual-Regression-Testing-System-VRTS.pptx.pptx)
- [Final Project Report](deliverables/final-report.md)


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
