#!/usr/bin/env python3
"""
app.py — Flask Web Dashboard for Visual Regression Testing

Routes:
  GET  /                → Dashboard homepage (URL input, chart, history)
  POST /run-test        → Kick off a visual regression test
  GET  /results         → Show detailed results for the latest test
  GET  /api/stats       → JSON endpoint consumed by Chart.js
  GET  /api/results     → JSON list of all test results
  GET  /screenshots/<path> → Serve saved screenshot images
"""

import os
import shutil

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    send_from_directory,
)

from engine.selenium_runner import capture_screenshot
from engine.image_compare import compare_images
from engine.result_manager import add_result, get_all_results, get_statistics


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)

BASELINE_DIR = "screenshots/baseline"
CURRENT_DIR = "screenshots/current"
DIFF_DIR = "screenshots/diff"


# ---------------------------------------------------------------------------
# Routes — Pages
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the main dashboard page."""
    stats = get_statistics()
    results = get_all_results()
    return render_template("index.html", stats=stats, results=results)


@app.route("/run-test", methods=["POST"])
def run_test():
    """Execute a visual regression test and redirect to the results page."""
    url = request.form.get("url", "").strip()
    if not url:
        return redirect(url_for("index"))

    # 1. Capture current screenshot
    current_path = capture_screenshot(url, output_dir=CURRENT_DIR)
    filename = os.path.basename(current_path)

    # 2. Check / create baseline
    baseline_path = os.path.join(BASELINE_DIR, filename)
    if not os.path.exists(baseline_path):
        os.makedirs(BASELINE_DIR, exist_ok=True)
        shutil.copy2(current_path, baseline_path)
        # First run — automatic PASS
        add_result(
            url=url,
            passed=True,
            diff_percent=0.0,
            baseline_path=os.path.abspath(baseline_path),
            current_path=os.path.abspath(current_path),
            diff_image_path="",
        )
        return redirect(url_for("results"))

    # 3. Compare
    comparison = compare_images(
        baseline_path=baseline_path,
        current_path=current_path,
        diff_dir=DIFF_DIR,
    )

    # 4. Record result
    add_result(
        url=url,
        passed=comparison["passed"],
        diff_percent=comparison["diff_percent"],
        baseline_path=comparison["baseline_path"],
        current_path=comparison["current_path"],
        diff_image_path=comparison["diff_image_path"],
    )

    return redirect(url_for("results"))


@app.route("/results")
def results():
    """Show the results page with detailed info for the most recent test."""
    all_results = get_all_results()
    latest = all_results[-1] if all_results else None
    stats = get_statistics()
    return render_template("results.html", latest=latest, stats=stats, results=all_results)


# ---------------------------------------------------------------------------
# Routes — API (JSON)
# ---------------------------------------------------------------------------

@app.route("/api/stats")
def api_stats():
    """Return aggregate pass/fail/total statistics as JSON."""
    return jsonify(get_statistics())


@app.route("/api/results")
def api_results():
    """Return the full results list as JSON."""
    return jsonify(get_all_results())


# ---------------------------------------------------------------------------
# Routes — Static screenshot files
# ---------------------------------------------------------------------------

@app.route("/screenshots/<path:filepath>")
def serve_screenshot(filepath):
    """Serve screenshot images from the screenshots directory."""
    return send_from_directory("screenshots", filepath)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Ensure screenshot directories exist
    for d in [BASELINE_DIR, CURRENT_DIR, DIFF_DIR]:
        os.makedirs(d, exist_ok=True)

    app.run(debug=True, host="0.0.0.0", port=5000)
