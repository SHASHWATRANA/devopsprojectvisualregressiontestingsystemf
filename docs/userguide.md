# User Guide — Visual Regression Testing System

**Author:** Shashwat Rana (23fe10cse00101)  
**Course:** CSE3253 DevOps [PE6] | Semester VI (2025–2026)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Requirements](#2-system-requirements)
3. [Installation](#3-installation)
4. [Using the Web Dashboard](#4-using-the-web-dashboard)
5. [Using the CLI](#5-using-the-cli)
6. [Understanding Test Results](#6-understanding-test-results)
7. [Managing Baselines](#7-managing-baselines)
8. [Running with Docker](#8-running-with-docker)
9. [FAQ](#9-faq)

---

## 1. Introduction

The **Visual Regression Testing System (VRTS)** automatically detects visual changes in web pages by:

- Capturing a **current screenshot** using headless Chrome (Selenium)
- Comparing it pixel-by-pixel against a stored **baseline screenshot** (OpenCV)
- Producing a **diff image** that highlights changed regions in red
- Reporting a **PASS** or **FAIL** result with a precise diff percentage

VRTS can be operated via a browser-based **Web Dashboard** or a **Command-Line Interface (CLI)** — both use the same underlying comparison engine.

---

## 2. System Requirements

| Requirement       | Minimum Version |
|-------------------|----------------|
| Python            | 3.10+          |
| Google Chrome     | Latest stable  |
| pip               | 22+            |
| Docker (optional) | 20+            |
| RAM               | 2 GB           |
| Disk              | 500 MB         |

---

## 3. Installation

### Clone the Repository

```bash
git clone https://github.com/<your-username>/devops_vrts.git
cd devops_vrts
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `webdriver-manager` automatically downloads the correct ChromeDriver on first run. An internet connection is required.

---

## 4. Using the Web Dashboard

### Start the Server

```bash
python app.py
```

Open your browser and navigate to **[http://localhost:5000](http://localhost:5000)**.

### Running a Test

1. Enter the URL of the page you want to test in the input box (e.g., `https://example.com`).
2. Click **Run Test**.
3. VRTS captures a screenshot, compares it with the stored baseline, and redirects you to the **Results** page.

### Results Page

The Results page shows:
- **Status:** PASS ✅ or FAIL ❌
- **Diff Percentage:** Proportion of pixels that changed
- **Changed Pixels / Total Pixels**
- Side-by-side: **Baseline**, **Current**, and **Diff** images

### Dashboard Charts

The homepage chart (powered by Chart.js) visualises historical pass/fail counts across all tests run in the current session.

---

## 5. Using the CLI

Run a test directly from the terminal:

```bash
python cli.py --url https://example.com
```

#### Full Options

| Flag              | Default                  | Description                        |
|-------------------|--------------------------|------------------------------------|
| `--url`           | *(required)*             | URL of the page to test            |
| `--baseline-dir`  | `screenshots/baseline`   | Path to the baseline folder        |
| `--current-dir`   | `screenshots/current`    | Path to save current screenshots   |
| `--diff-dir`      | `screenshots/diff`       | Path to save diff images           |
| `--threshold`     | `0.5`                    | % diff threshold for FAIL          |

#### Example

```bash
python cli.py --url https://mysite.com --threshold 1.0
```

CLI output example:

```
[VRTS] Capturing screenshot for: https://example.com
[VRTS] Comparing against baseline...
[VRTS] Result: PASS  |  Diff: 0.0012%
```

---

## 6. Understanding Test Results

| Field              | Meaning                                                     |
|--------------------|-------------------------------------------------------------|
| **PASS**           | Diff percentage ≤ threshold (default 0.5 %)                |
| **FAIL**           | Diff percentage > threshold                                 |
| **Diff %**         | `(changed_pixels / total_pixels) × 100`                    |
| **Diff Image**     | Red pixels = regions that changed between baseline & current |

---

## 7. Managing Baselines

- **First run:** If no baseline exists for a URL, the current screenshot is saved as the baseline automatically (auto-PASS).
- **Updating baseline:** Delete the baseline image from `screenshots/baseline/` and run the test again.
- **Resetting all baselines:** Delete the entire `screenshots/baseline/` directory.

---

## 8. Running with Docker

```bash
# Build the image
docker build -t vrts .

# Run the container (maps port 5000)
docker run -p 5000:5000 vrts
```

Access the dashboard at **[http://localhost:5000](http://localhost:5000)**.

To persist screenshots between container restarts, mount a local volume:

```bash
docker run -p 5000:5000 -v $(pwd)/screenshots:/app/screenshots vrts
```

---

## 9. FAQ

**Q: ChromeDriver download fails behind a corporate proxy.**  
A: Set the `HTTPS_PROXY` environment variable before running, or pre-download ChromeDriver and point `Service()` to its local path.

**Q: My test always passes even though the page changed.**  
A: Lower the `--threshold` value. The default is 0.5 % — very small cosmetic changes might be under this limit.

**Q: Can I test pages that require login?**  
A: The current version does not support authenticated sessions. You can extend `selenium_runner.py` to inject cookies or run pre-test login steps.

**Q: Screenshots look different locally vs in CI.**  
A: This is usually a font or rendering difference between operating systems. Run tests inside Docker for a consistent environment.
