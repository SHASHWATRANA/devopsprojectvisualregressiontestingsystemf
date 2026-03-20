# API Documentation — Visual Regression Testing System

**Author:** Shashwat Rana (23fe10cse00101)  
**Course:** CSE3253 DevOps [PE6] | Semester VI (2025–2026)

---

## Overview

VRTS exposes a lightweight **REST API** built with Flask. All JSON endpoints return `Content-Type: application/json`. There is no authentication required for local or self-hosted deployments.

**Base URL (local):** `http://localhost:5000`

---

## Endpoints

### 1. `GET /`

**Description:** Renders the main web dashboard.

**Response:** HTML page (`text/html`).

---

### 2. `POST /run-test`

**Description:** Executes a visual regression test for the given URL.

**Request:** `application/x-www-form-urlencoded`

| Field | Type   | Required | Description           |
|-------|--------|----------|-----------------------|
| `url` | string | ✅ Yes    | The URL to screenshot |

**Behaviour:**
1. Captures a screenshot of `url` using headless Chrome.
2. If no baseline exists for that URL → saves screenshot as baseline (PASS).
3. If baseline exists → runs pixel comparison, records result.
4. Redirects to `GET /results`.

**Example (curl):**

```bash
curl -X POST http://localhost:5000/run-test \
     -d "url=https://example.com"
```

**Response:** `302 Redirect` → `/results`

---

### 3. `GET /results`

**Description:** Renders the results page showing the most recent test.

**Response:** HTML page (`text/html`).

---

### 4. `GET /api/stats`

**Description:** Returns aggregate statistics for all tests run in the current session.

**Response:** `200 OK` — JSON object

```json
{
  "total": 10,
  "passed": 8,
  "failed": 2,
  "pass_rate": 80.0
}
```

| Field       | Type    | Description                              |
|-------------|---------|------------------------------------------|
| `total`     | integer | Total number of tests run                |
| `passed`    | integer | Number of tests that PASSed              |
| `failed`    | integer | Number of tests that FAILed              |
| `pass_rate` | float   | `(passed / total) × 100`, 0 if no tests |

**Example:**

```bash
curl http://localhost:5000/api/stats
```

---

### 5. `GET /api/results`

**Description:** Returns the full list of test results recorded this session.

**Response:** `200 OK` — JSON array

```json
[
  {
    "url": "https://example.com",
    "timestamp": "2026-03-21T00:05:00",
    "passed": true,
    "diff_percent": 0.0012,
    "baseline_path": "/app/screenshots/baseline/example_com.png",
    "current_path": "/app/screenshots/current/example_com.png",
    "diff_image_path": "/app/screenshots/diff/example_com.png"
  }
]
```

| Field             | Type    | Description                              |
|-------------------|---------|------------------------------------------|
| `url`             | string  | Tested URL                               |
| `timestamp`       | string  | ISO 8601 datetime of the test            |
| `passed`          | boolean | `true` = PASS, `false` = FAIL            |
| `diff_percent`    | float   | Percentage of pixels that changed        |
| `baseline_path`   | string  | Absolute path to baseline screenshot     |
| `current_path`    | string  | Absolute path to current screenshot      |
| `diff_image_path` | string  | Absolute path to diff image (or `""`)    |

---

### 6. `GET /screenshots/<path>`

**Description:** Serves screenshot images stored on the server.

**Path Parameter:** Relative path within the `screenshots/` directory.

**Response:** Image file (`image/png`)

**Example:**

```
GET /screenshots/current/example_com.png
GET /screenshots/diff/example_com.png
GET /screenshots/baseline/example_com.png
```

---

## Internal Python API

These modules are importable for programmatic use.

### `engine.selenium_runner`

```python
from engine.selenium_runner import capture_screenshot

path = capture_screenshot(
    url="https://example.com",
    output_dir="screenshots/current",
    window_width=1920,
    window_height=1080,
)
# Returns: absolute path (str) to saved PNG
```

---

### `engine.image_compare`

```python
from engine.image_compare import compare_images

result = compare_images(
    baseline_path="screenshots/baseline/example_com.png",
    current_path="screenshots/current/example_com.png",
    diff_dir="screenshots/diff",
    pixel_threshold=30,
    diff_percent_threshold=0.5,
)
```

**Return value:**

```python
{
    "passed": True,
    "diff_percent": 0.0012,
    "changed_pixels": 150,
    "total_pixels": 2073600,
    "diff_image_path": "/abs/path/to/diff.png",
    "baseline_path": "/abs/path/...",
    "current_path": "/abs/path/...",
    "message": "PASS",
}
```

---

### `engine.result_manager`

```python
from engine.result_manager import add_result, get_all_results, get_statistics

add_result(url, passed, diff_percent, baseline_path, current_path, diff_image_path)

results = get_all_results()   # list of result dicts
stats   = get_statistics()    # { total, passed, failed, pass_rate }
```

---

## Error Handling

| Scenario                       | Behaviour                                      |
|--------------------------------|------------------------------------------------|
| Empty / missing `url` in POST  | Redirects back to `/` (no test runs)           |
| Baseline image not found       | `FileNotFoundError` raised by `compare_images` |
| Chrome not installed           | `WebDriverException` from Selenium             |
| Invalid URL / unreachable page | Selenium timeout after 30 s                    |

All unhandled exceptions bubble up as HTTP 500 responses in debug mode.
