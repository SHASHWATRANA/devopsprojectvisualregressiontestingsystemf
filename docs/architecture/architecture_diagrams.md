# Architecture Diagrams — Visual Regression Testing System

**Author:** Shashwat Rana (23fe10cse00101)  
**Course:** CSE3253 DevOps [PE6] | Semester VI (2025–2026)

---

## 1. High-Level System Architecture

```
                   ┌──────────────────────────────────────────────┐
                   │             USER INTERFACES                   │
                   │                                              │
                   │  ┌──────────────────┐  ┌─────────────────┐  │
                   │  │  Web Dashboard   │  │   CLI (cli.py)  │  │
                   │  │  (Flask + HTML)  │  │  $ python cli.py│  │
                   │  │  localhost:5000  │  │  --url <URL>    │  │
                   │  └────────┬─────────┘  └────────┬────────┘  │
                   └───────────┼─────────────────────┼───────────┘
                               │                     │
                   ┌───────────▼─────────────────────▼───────────┐
                   │          CORE ENGINE  (engine/)              │
                   │                                              │
                   │  ┌─────────────────────────────────────┐    │
                   │  │  selenium_runner.py                 │    │
                   │  │  • Launch headless Chrome            │    │
                   │  │  • Navigate to URL                   │    │
                   │  │  • capture_screenshot() → PNG        │    │
                   │  └─────────────────────────────────────┘    │
                   │                 │                            │
                   │  ┌──────────────▼──────────────────────┐    │
                   │  │  image_compare.py                   │    │
                   │  │  • compare_images()                  │    │
                   │  │  • OpenCV absdiff + threshold        │    │
                   │  │  • Generate diff PNG (red overlay)   │    │
                   │  └─────────────────────────────────────┘    │
                   │                 │                            │
                   │  ┌──────────────▼──────────────────────┐    │
                   │  │  result_manager.py                  │    │
                   │  │  • add_result()                      │    │
                   │  │  • get_all_results()                 │    │
                   │  │  • get_statistics()                  │    │
                   │  └─────────────────────────────────────┘    │
                   └──────────────────────┬───────────────────────┘
                                          │
                   ┌──────────────────────▼───────────────────────┐
                   │              FILE STORAGE                     │
                   │                                              │
                   │  screenshots/baseline/  ← Reference PNGs    │
                   │  screenshots/current/   ← Latest PNGs       │
                   │  screenshots/diff/      ← Diff PNGs         │
                   │  test_results.json      ← Result history    │
                   └──────────────────────────────────────────────┘
```

---

## 2. Request Flow Diagram (Web Dashboard)

```
Browser                  Flask (app.py)          Engine                  Storage
  │                           │                     │                       │
  │── POST /run-test ─────────▶                     │                       │
  │   { url: "https://..." }  │                     │                       │
  │                           │── capture_screenshot(url) ──────────────────▶
  │                           │                     │  (headless Chrome)     │
  │                           │◀─ /path/to/curr.png ─────────────────────────
  │                           │                     │                       │
  │                           │── baseline exists? ──────────────────────────▶
  │                           │                     │                       │
  │                           │   NO ───────────────────────────────────────▶
  │                           │     copy curr → baseline (auto-PASS)        │
  │                           │                     │                       │
  │                           │   YES ──────────────▶                       │
  │                           │          compare_images(baseline, curr) ─────▶
  │                           │◀─ { passed, diff_percent, diff_path } ───────
  │                           │                     │                       │
  │                           │── add_result() ─────▶                       │
  │                           │                     │── write test_results.json
  │                           │                     │                       │
  │◀── 302 Redirect /results ─│                     │                       │
  │                           │                     │                       │
  │── GET /results ───────────▶                     │                       │
  │◀── HTML (PASS/FAIL page) ─│                     │                       │
```

---

## 3. Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          app.py                                 │
│                                                                 │
│  @route("/run-test")  ──────►  capture_screenshot()            │
│                                      │                         │
│                         ┌───────────▼────────────┐            │
│                         │  selenium_runner.py    │            │
│                         │  webdriver.Chrome()    │            │
│                         │  driver.get(url)       │            │
│                         │  driver.save_screenshot│            │
│                         └───────────┬────────────┘            │
│                                     │ PNG file path            │
│  @route("/run-test")  ──────►  compare_images()               │
│                                      │                         │
│                         ┌───────────▼────────────┐            │
│                         │  image_compare.py      │            │
│                         │  cv2.imread()          │            │
│                         │  cv2.absdiff()         │            │
│                         │  cv2.threshold()       │            │
│                         │  cv2.imwrite() (diff)  │            │
│                         └───────────┬────────────┘            │
│                                     │ result dict              │
│  @route("/run-test")  ──────►  add_result()                   │
│                                      │                         │
│                         ┌───────────▼────────────┐            │
│                         │  result_manager.py     │            │
│                         │  _results[] in memory  │            │
│                         │  test_results.json     │            │
│                         └────────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. CI/CD Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Repository                           │
│                                                                 │
│   Developer push / PR to `main`                                 │
│           │                                                     │
│           ▼                                                     │
│   ┌───────────────────────────────────────────────────────┐    │
│   │              GitHub Actions Runner                    │    │
│   │                 (ubuntu-latest)                       │    │
│   │                                                       │    │
│   │  Step 1: actions/checkout@v4                          │    │
│   │       ↓                                               │    │
│   │  Step 2: actions/setup-python@v5 (Python 3.12)       │    │
│   │       ↓                                               │    │
│   │  Step 3: Install Google Chrome (apt-get)              │    │
│   │       ↓                                               │    │
│   │  Step 4: pip install -r requirements.txt              │    │
│   │       ↓                                               │    │
│   │  Step 5: python cli.py --url https://example.com      │    │
│   │       ↓                                               │    │
│   │  Step 6: actions/upload-artifact@v4 (screenshots/)   │    │
│   └───────────────────────────────────────────────────────┘    │
│           │                                                     │
│   ┌───────▼───────────┐      ┌──────────────────────────┐      │
│   │  ✅ PASS           │  OR  │  ❌ FAIL                  │      │
│   │  CI badge: green   │      │  CI badge: red            │      │
│   │  Merge allowed     │      │  PR blocked               │      │
│   └────────────────────┘      └──────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Docker Container Architecture

```
┌──────────────────────────────────────────────────────┐
│               Docker Container (vrts)                │
│                                                      │
│   Base Image: python:3.12-slim                       │
│                                                      │
│   Installed:                                         │
│   ├── Google Chrome (headless)                       │
│   ├── ChromeDriver (via webdriver-manager at runtime)│
│   ├── Python packages (requirements.txt)             │
│   └── Project files (/app/)                          │
│                                                      │
│   /app/                                              │
│   ├── app.py                                         │
│   ├── cli.py                                         │
│   ├── engine/                                        │
│   ├── templates/                                     │
│   ├── static/                                        │
│   └── screenshots/  ◄──── Volume mount point        │
│                                                      │
│   EXPOSE 5000                                        │
│   CMD: gunicorn --bind 0.0.0.0:5000 --workers 2     │
│                                                      │
└─────────────────────────┬────────────────────────────┘
                          │ Port 5000
            ┌─────────────▼───────────────┐
            │         Host Machine         │
            │    http://localhost:5000     │
            └─────────────────────────────┘
```

---

## 6. Data Model

```
TestResult {
  url              : string   — Tested URL
  timestamp        : datetime — When the test ran
  passed           : bool     — PASS or FAIL
  diff_percent     : float    — % pixels changed (0.0–100.0)
  changed_pixels   : int      — Absolute changed pixel count
  total_pixels     : int      — Total pixels in image
  baseline_path    : string   — Absolute path to baseline PNG
  current_path     : string   — Absolute path to current PNG
  diff_image_path  : string   — Absolute path to diff PNG (or "")
  message          : string   — "PASS" or "FAIL"
}

Statistics {
  total     : int   — Total tests run
  passed    : int   — Passing tests
  failed    : int   — Failing tests
  pass_rate : float — passed/total × 100
}
```
