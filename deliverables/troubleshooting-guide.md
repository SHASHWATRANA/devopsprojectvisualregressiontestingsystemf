# Troubleshooting Guide — Visual Regression Testing System

**Author:** Shashwat Rana (23fe10cse00101)  
**Course:** CSE3253 DevOps [PE6] | Semester VI (2025–2026)

---

## Table of Contents

1. [Chrome / ChromeDriver Issues](#1-chrome--chromedriver-issues)
2. [Screenshot Capture Issues](#2-screenshot-capture-issues)
3. [Image Comparison Issues](#3-image-comparison-issues)
4. [Flask / Web Dashboard Issues](#4-flask--web-dashboard-issues)
5. [Docker Issues](#5-docker-issues)
6. [GitHub Actions CI Failures](#6-github-actions-ci-failures)
7. [General Debugging Tips](#7-general-debugging-tips)

---

## 1. Chrome / ChromeDriver Issues

### Error: `WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Cause:** `webdriver-manager` failed to download or locate ChromeDriver.

**Fix:**
```bash
# Force reinstall webdriver-manager
pip install --upgrade webdriver-manager

# Clear the driver cache
rm -rf ~/.wdm
```
Or explicitly pass the driver path:
```python
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())
```

---

### Error: `SessionNotCreatedException: Current browser version is X, ChromeDriver only supports Y`

**Cause:** Chrome was updated but ChromeDriver was not (or vice versa).

**Fix:** Clear the `webdriver-manager` cache so it re-downloads the correct driver:
```bash
# Windows
rmdir /s /q %USERPROFILE%\.wdm

# Linux/macOS
rm -rf ~/.wdm
```

---

### Error: `Chrome failed to start: exited abnormally`

**Cause (Docker):** Chrome requires elevated privileges or a specific `--shm-size`.

**Fix (Docker):**
```bash
docker run --shm-size=2g -p 5000:5000 vrts
```

**Fix (Linux host, no Docker):**
```bash
# Run with sandbox disabled
# (already configured in selenium_runner.py via --no-sandbox flag)
```

---

## 2. Screenshot Capture Issues

### Screenshots are blank / all white

**Cause:** Page not fully loaded when screenshot is taken.

**Fix:** Increase the sleep delay in `selenium_runner.py`:
```python
time.sleep(5)  # Increase from default 2 seconds
```

---

### Screenshots look different between runs

**Cause:** Animations, dynamic content, or ads change between captures.

**Fix:**
- Disable animations via injected CSS: add a step in `selenium_runner.py` to execute `document.body.style.animation = 'none'`.
- Increase `DIFF_PERCENT_THRESHOLD` to tolerate minor dynamic changes.

---

### Error: `FileNotFoundError: Baseline image not found`

**Cause:** Baseline was deleted or never created for this URL.

**Fix:** Delete any partial baseline and re-run the test — the first run always auto-generates the baseline.

---

### Screenshots are cropped / partial

**Cause:** Default window size `1920×1080` does not capture the full page.

**Fix:** Use JavaScript to scroll and stitch, or adjust the window size in `selenium_runner.py`:
```python
driver.execute_script("document.body.style.overflow = 'visible'")
height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(1920, height)
```

---

## 3. Image Comparison Issues

### All tests return PASS even though the page changed

**Cause:** The diff percentage is below the threshold (default 0.5 %).

**Fix:** Lower the threshold:
```bash
python cli.py --url https://example.com --threshold 0.1
```

---

### Too many false FAILs (flapping tests)

**Cause:** Anti-aliasing, font rendering, or dynamic content causes noise.

**Fix:** Increase either threshold:
```python
# In engine/image_compare.py
PIXEL_THRESHOLD = 50           # Ignore more noise
DIFF_PERCENT_THRESHOLD = 1.0   # More lenient PASS/FAIL boundary
```

---

### Error: `cv2.error: OpenCV(4.x) error: (-215:Assertion failed) !_src.empty()`

**Cause:** OpenCV could not read the image file (corrupt file or wrong path).

**Fix:**
1. Verify the image file exists at the reported path.
2. Confirm the screenshot step succeeded before comparison.
3. Check disk space (`df -h`).

---

## 4. Flask / Web Dashboard Issues

### `Address already in use` on port 5000

**Cause:** Another process is using port 5000.

**Fix:**
```bash
# Find and kill the process (Linux/macOS)
lsof -i :5000 | grep LISTEN
kill -9 <PID>

# Windows PowerShell
netstat -ano | findstr :5000
Stop-Process -Id <PID> -Force
```
Or change the port:
```bash
python app.py  # Edit app.py → port=5001
```

---

### `ImportError: cannot import name 'X' from 'engine'`

**Cause:** Running `app.py` from the wrong directory, or a missing `__init__.py`.

**Fix:**
```bash
# Always run from the project root
cd c:\Users\shash\OneDrive\Desktop\devops_vrts
python app.py
```

---

### Dashboard shows no results / empty chart

**Cause:** No tests have been run in this session. Results are in-memory.

**Fix:** Run at least one test via the Web Dashboard or CLI. To persist across restarts, ensure `test_results.json` is not deleted.

---

## 5. Docker Issues

### `docker: command not found`

**Fix:** Install Docker Desktop: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

---

### Docker build fails: `apt-get update` or Chrome install error

**Cause:** Network issue or stale apt cache.

**Fix:**
```bash
docker build --no-cache -t vrts .
```

---

### Container starts but dashboard is unreachable

**Cause:** Port not mapped correctly.

**Fix:** Ensure you use `-p 5000:5000`:
```bash
docker run -p 5000:5000 vrts
```
Access at `http://localhost:5000` (not `http://0.0.0.0:5000`).

---

## 6. GitHub Actions CI Failures

### CI fails at "Install Google Chrome" step

**Cause:** Google's signing key URL changed.

**Fix:** Update the key URL in `.github/workflows/ci.yml`:
```yaml
- name: Install Google Chrome
  run: |
    sudo apt-get install -y google-chrome-stable
```
Using the `apt-get` shortcut (Ubuntu runners have Chrome in their apt repos).

---

### CI fails: `python cli.py --url https://example.com` times out

**Cause:** GitHub Actions runner cannot reach the external URL, or Chrome crashes.

**Fix:**
- Add `--timeout 60` to the CLI call.
- Use a local test server and URL instead of an external URL.

---

## 7. General Debugging Tips

1. **Enable Flask debug mode** for verbose error tracebacks:
   ```bash
   FLASK_DEBUG=1 python app.py
   ```

2. **Run the comparison engine in isolation:**
   ```python
   from engine.image_compare import compare_images
   result = compare_images("baseline.png", "current.png")
   print(result)
   ```

3. **Check the `test_results.json`** file for the raw result history:
   ```bash
   cat test_results.json
   ```

4. **Inspect screenshots directly** in the `screenshots/` folder — open `diff/*.png` in any image viewer to see highlighted changes.

5. **Docker logs:**
   ```bash
   docker logs <container_id> --tail 50
   ```
