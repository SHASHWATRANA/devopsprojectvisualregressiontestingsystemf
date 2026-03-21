# Final Project Report: Visual Regression Testing System (VRTS)

**Author:** Shashwat Rana  
**Registration No:** 23fe10cse00101  
**Course:** CSE3253 DevOps [PE6]  
**Semester:** VI (2025–2026)  
**Date:** March 2026

---

## 1. Executive Summary

In modern web development, continuous integration and continuous deployment (CI/CD) pipelines have drastically reduced the time needed to ship code. However, while unit and integration tests verify functional correctness, they frequently fail to catch *visual* errors. A simple CSS change in a shared component can silently break the layout of dozens of connected pages. Manual visual quality assurance (QA) is unscalable, error-prone, and too slow for modern DevOps pipelines.

To solve this problem, I developed the **Visual Regression Testing System (VRTS)**. VRTS is an automated tool that automatically detects unintended visual changes in web pages. It captures high-fidelity screenshots using headless browser automation and compares them via pixel-level image processing. Engineered with a DevOps-first mindset, VRTS is fully containerised via Docker, integrates directly into GitHub Actions for automated execution, and provides both a Command-Line Interface (CLI) for CI environments and a Flask-based Web Dashboard for manual QA review.

## 2. Problem Statement & Objectives

### 2.1 The Problem
When UI elements are altered, new dependencies are introduced, or code is refactored, the visual appearance of a web application can inadvertently change. These "visual regressions" result in overlapping text, broken layouts, or hidden buttons. Traditional DOM-based testing (like checking if an HTML element exists) cannot "see" if the element is actually visible or rendered correctly on the screen.

### 2.2 Project Objectives
The primary objectives of the VRTS project were to:
1. **Automate Visual Validation:** Build a system capable of capturing and comparing web page screenshots automatically.
2. **Dual Interfaces:** Provide a CLI for automated pipelines and a Web UI for human review.
3. **Containerisation:** Ensure environment consistency by packaging the entire application—including the complex headless Chrome browser—inside a Docker container.
4. **CI/CD Integration:** Implement an automated pipeline that runs smoke tests on every code push to protect the `main` branch.
5. **Cloud Deployment:** Deploy the dashboard to a cloud provider as a live service.

## 3. System Architecture & Component Design

The VRTS application is built on a modular, three-tier architecture:

### 3.1 The Presentation Layer
- **CLI (`cli.py`):** Designed for automation. It accepts a `--url` argument, triggers the testing engine, and exits with a standard `0` (PASS) or `1` (FAIL) status code.
- **Web Dashboard (`app.py`):** Built with Flask. It provides a user-friendly form to initiate tests, displays historical results using Chart.js, and serves the generated diff images side-by-side with the baseline.

### 3.2 The Core Engine Layer (`src/main/engine/`)
- **Selenium Runner (`selenium_runner.py`):** Uses Python Selenium and `webdriver-manager` to launch Google Chrome in headless mode. It requests the target URL, waits for rendering, and saves a 1920x1080 PNG screenshot.
- **Image Comparator (`image_compare.py`):** Utilises OpenCV (`cv2`). It loads the baseline (reference) image and the newly captured image, computes the absolute difference, applies a noise-cancelling threshold, and calculates the percentage of changed pixels. It outputs a composite image showing exactly which pixels changed in bright red.
- **Result Manager (`result_manager.py`):** Handles persistence, saving test metadata (timestamps, pass/fail status, diff percentage, and file paths) to `test_results.json`.

### 3.3 The Infrastructure Layer
- **Docker (`Dockerfile` & `docker-compose.yml`):** A custom Linux-based container that installs Python 3.12, system fonts, necessary graphics libraries (libgbm1, libx11), and Google Chrome.
- **CI/CD Pipeline (`ci.yml` & `Jenkinsfile`):** Automated workflows that build the environment from scratch, install dependencies, and run validation tests.

## 4. Technology Stack Justification

| Technology | Role | Justification |
|------------|------|---------------|
| **Python 3.12** | Core Language | Excellent ecosystem for both web (Flask) and data/image processing (OpenCV). |
| **Flask** | Web Framework | Lightweight and unopinionated; perfect for building the REST API and dashboard without unnecessary ORM bloat. |
| **Selenium 4** | Browser Automation | The industry standard for web automation. Used to drive headless Chrome for pixel-perfect standardisation. |
| **OpenCV** | Image Processing | High-performance, C-backed library capable of comparing multi-megabyte images in milliseconds. |
| **Docker** | Containerisation | Solves the "it works on my machine" problem. Browser versions and OS font rendering drastically affect screenshots; Docker guarantees the exact same rendering environment everywhere. |
| **GitHub Actions** | CI/CD | Native integration with the repository for immediate testing upon every commit. |
| **Render.com** | Cloud Hosting | Supports direct Docker container deployment via Infrastructure-as-Code (`render.yaml`). |

## 5. Development Methodology & Challenges

### 5.1 Project Restructure
The project was originally developed as a flat repository but was later refactored into a rigorous DevOps folder structure (`src/`, `infrastructure/`, `pipelines/`, `docs/`, `deliverables/`). This separation of concerns ensures that infrastructure code (Dockerfile) is decoupled from source code (`app.py`), mimicking enterprise best practices.

### 5.2 Key Challenges & Solutions
1. **The "Flapping Test" Problem:** Minor anti-aliasing differences between runs caused false failures.
   * **Solution:** I implemented a dual-threshold system in OpenCV. A `PIXEL_THRESHOLD` ignores minor colour variations (noise), while a `DIFF_PERCENT_THRESHOLD` allows a tiny percentage of pixels to change before declaring a hard FAIL.
2. **Containerising Chrome:** Running Chrome inside Docker often results in shared memory (shm) crashes.
   * **Solution:** Engineered the Selenium runner to inject `--no-sandbox` and `--disable-dev-shm-usage` flags, and configured the Dockerfile to install missing Debian libraries explicitly.
3. **Driver Version Sync:** ChromeDriver mismatch is a notorious pain point in Selenium automation.
   * **Solution:** Integrated `webdriver-manager` to dynamically detect the installed Chrome version and download the exact matching driver at runtime.

## 6. Project Outcomes & DevOps Principles Applied

The successful completion of VRTS demonstrates several core DevOps principles:
- **Infrastructure as Code (IaC):** The entire deployment environment is defined in code (`Dockerfile` and `render.yaml`), making it version-controlled and instantly reproducible.
- **Continuous Integration:** The GitHub Actions pipeline ensures that code pushed to the main branch is automatically tested. If `cli.py` fails, the build turns red, preventing broken code from merging.
- **Observability:** The Flask dashboard provides immediate visual feedback on the health of the application's UI, surfacing errors that traditional logs miss.

## 7. Conclusion & Future Work

The Visual Regression Testing System successfully meets all initial objectives. It provides a robust, automated mechanism for catching visual bugs, wrapped in a professional DevOps architecture. 

**Future Enhancements could include:**
- Implementing authenticated testing (cookie injection) to test pages behind login screens.
- Adding a PostgreSQL database to replace `test_results.json` for scalable, long-term history tracking.
- Integrating Slack or email notifications triggered directly by the GitHub Actions pipeline upon test failure.

This project provided invaluable hands-on experience in bridging software engineering (Python, OpenCV) with modern DevOps operations (Docker, CI/CD, Cloud Deployment).
