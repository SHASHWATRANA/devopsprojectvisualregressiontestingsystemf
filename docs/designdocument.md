# Design Document — Visual Regression Testing System

**Author:** Shashwat Rana (23fe10cse00101)  
**Course:** CSE3253 DevOps [PE6] | Semester VI (2025–2026)  
**Date:** March 2026

---

## 1. Problem Statement

Modern web applications change frequently — layouts shift, colours change, and elements move due to CSS or JavaScript updates. Manual QA cannot keep pace with continuous deployment. **VRTS** solves this by automatically detecting unintended visual regressions between deployments.

---

## 2. Objectives

- Automatically detect visual changes in web pages across deployments
- Support both CLI (for CI/CD integration) and Web Dashboard (for manual testing)
- Generate visual diff reports that highlight exactly which pixels changed
- Be containerised and deployable to any cloud environment
- Integrate with GitHub Actions for automated testing on every push

---

## 3. System Architecture

VRTS is structured as three loosely-coupled layers:

```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                  │
│   ┌──────────────────┐  ┌────────────────────┐  │
│   │  Web Dashboard   │  │  CLI Interface     │  │
│   │  (Flask/HTML)    │  │  (cli.py)          │  │
│   └────────┬─────────┘  └────────┬───────────┘  │
└────────────┼────────────────────┼───────────────┘
             │                    │
┌────────────▼────────────────────▼───────────────┐
│              Engine Layer (engine/)              │
│  ┌──────────────────────────────────────────┐   │
│  │  selenium_runner.py  (Screenshot Capture) │  │
│  │  image_compare.py    (OpenCV Comparison)  │  │
│  │  result_manager.py   (Result Tracking)    │  │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│             Storage Layer                        │
│   screenshots/baseline/   (Reference images)     │
│   screenshots/current/    (Latest captures)      │
│   screenshots/diff/       (Highlighted diffs)    │
│   test_results.json       (Result history)       │
└─────────────────────────────────────────────────┘
```

---

## 4. Component Design

### 4.1 Selenium Runner (`engine/selenium_runner.py`)

**Responsibility:** Launch headless Chrome, navigate to a URL, and save a full-page screenshot.

**Key Design Decisions:**
- Uses `webdriver-manager` to auto-install the matching ChromeDriver version — eliminates manual driver management.
- `--headless=new` flag uses Chrome's next-gen headless mode (more stable than legacy `--headless`).
- `--no-sandbox` and `--disable-dev-shm-usage` flags enable operation inside Docker containers.
- A 2-second sleep after page load allows SPAs to hydrate before capture.
- URL-to-filename sanitisation uses regex to create safe, readable filenames.

### 4.2 Image Comparator (`engine/image_compare.py`)

**Responsibility:** Compare two PNG screenshots using OpenCV and produce a quantitative diff.

**Algorithm:**
1. Load both images with `cv2.imread()`.
2. Resize current image to baseline dimensions if they differ.
3. Compute absolute pixel difference: `cv2.absdiff(baseline, current)`.
4. Convert to greyscale and apply binary threshold (default: 30) to suppress noise.
5. Count non-zero pixels → divide by total → diff percentage.
6. Overlay red pixels on changed regions of the current screenshot → save as diff image.

**Threshold Design:**
- `PIXEL_THRESHOLD = 30` — ignores rendering noise (antialiasing, subpixel differences).
- `DIFF_PERCENT_THRESHOLD = 0.5 %` — a configurable PASS/FAIL boundary.

### 4.3 Result Manager (`engine/result_manager.py`)

**Responsibility:** Store, retrieve, and aggregate test results in memory (with optional JSON persistence).

**Design:** In-memory list for the current session; `test_results.json` provides optional persistence between restarts.

### 4.4 Web Dashboard (`app.py`, `templates/`, `static/`)

**Responsibility:** Provide a human-friendly interface for running tests and viewing results.

**Routes:**

| Route             | Method | Purpose                              |
|-------------------|--------|--------------------------------------|
| `/`               | GET    | Dashboard with history & chart       |
| `/run-test`       | POST   | Execute a test                       |
| `/results`        | GET    | Show latest result details           |
| `/api/stats`      | GET    | JSON aggregate stats (Chart.js feed) |
| `/api/results`    | GET    | JSON all results                     |
| `/screenshots/<p>`| GET    | Serve screenshot images              |

### 4.5 CLI (`cli.py`)

**Responsibility:** Provide a scriptable, single-command interface for use in terminal or CI pipelines.

---

## 5. Data Flow

```
User Input (URL)
      │
      ▼
selenium_runner.capture_screenshot()
      │  saves → screenshots/current/<slug>.png
      ▼
baseline exists?
  ├─ NO  → copy to baseline, return PASS
  └─ YES → image_compare.compare_images()
                │  saves → screenshots/diff/<slug>.png
                ▼
           result_manager.add_result()
                │  stores → in-memory + test_results.json
                ▼
           Return PASS / FAIL + metrics
```

---

## 6. Technology Choices

| Technology       | Role                         | Rationale                                      |
|------------------|------------------------------|------------------------------------------------|
| Python 3.12      | Application language         | Rich ecosystem; excellent for automation       |
| Flask 3.1        | Web framework                | Lightweight; no ORM overhead needed            |
| Selenium 4       | Browser automation           | Industry standard for web UI testing           |
| OpenCV           | Image processing             | High-performance pixel comparison; C-backed    |
| webdriver-manager| ChromeDriver management      | Eliminates manual driver version management    |
| Gunicorn         | Production WSGI server       | Multi-worker; battle-tested with Flask         |
| Docker           | Containerisation             | Consistent environment across dev/CI/prod      |
| GitHub Actions   | CI/CD                        | Native GitHub integration; free for public repos |
| Chart.js         | Dashboard visualisation      | Zero-dependency; client-side charting          |

---

## 7. Security Considerations

- VRTS does not authenticate users. For production use, place it behind a reverse proxy (nginx) with HTTP basic auth or OAuth.
- Browser automation (Selenium) runs with `--no-sandbox` inside Docker — acceptable in an isolated container; **not recommended** to run as root on the host.
- Screenshot images are served by Flask's `send_from_directory` with a limited base path to prevent path traversal.

---

## 8. Scalability & Limitations

- **Concurrency:** Flask's dev server is single-threaded. Gunicorn is configured with `--workers 2` for production. Selenium is synchronous; parallel testing would require a Selenium Grid or separate worker processes.
- **Storage:** Screenshots are saved to the local filesystem. In production, consider mounting a cloud storage bucket or using an object store.
- **Baseline Management:** Baselines are stored as flat files. A larger system would use a database-backed baseline registry with version control.

---

## 9. Future Enhancements

- [ ] Support authenticated test flows (login before screenshot)
- [ ] Configurable viewport presets (mobile, tablet, desktop)
- [ ] Email / Slack notifications on FAIL
- [ ] Selenium Grid integration for parallel test execution
- [ ] Baseline versioning with Git or S3
- [ ] REST API authentication (JWT / API keys)
