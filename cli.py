#!/usr/bin/env python3
"""
cli.py — Command-Line Interface for Visual Regression Testing

Usage:
    python cli.py --url https://example.com
    python cli.py --url https://example.com --threshold 1.0

The CLI will:
  1. Capture a screenshot of the given URL with Selenium
  2. Compare against an existing baseline (if present)
  3. Print PASS / FAIL and relevant paths to the terminal
  4. If no baseline exists, the first capture becomes the baseline
"""

import argparse
import os
import shutil
import sys

from engine.selenium_runner import capture_screenshot
from engine.image_compare import compare_images
from engine.result_manager import add_result


# ---------------------------------------------------------------------------
# Directories
# ---------------------------------------------------------------------------

BASELINE_DIR = "screenshots/baseline"
CURRENT_DIR = "screenshots/current"
DIFF_DIR = "screenshots/diff"


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def run_test(url: str, threshold: float = 0.5) -> dict:
    """
    Execute a full visual regression test for *url*.

    Returns the result dict produced by the engine.
    """

    print(f"\n{'='*60}")
    print(f"  Running visual test for {url}")
    print(f"{'='*60}\n")

    # Step 1 — Capture current screenshot
    print("[1/4] Capturing screenshot …")
    current_path = capture_screenshot(url, output_dir=CURRENT_DIR)
    filename = os.path.basename(current_path)
    print(f"       Screenshot saved: {current_path}\n")

    # Step 2 — Check for an existing baseline
    baseline_path = os.path.join(BASELINE_DIR, filename)
    baseline_exists = os.path.exists(baseline_path)
    print(f"[2/4] Baseline exists: {'YES' if baseline_exists else 'NO'}")

    if not baseline_exists:
        # First run — promote current screenshot to baseline
        os.makedirs(BASELINE_DIR, exist_ok=True)
        shutil.copy2(current_path, baseline_path)
        print(f"       → Created new baseline: {baseline_path}\n")

        result = add_result(
            url=url,
            passed=True,
            diff_percent=0.0,
            baseline_path=os.path.abspath(baseline_path),
            current_path=os.path.abspath(current_path),
            diff_image_path="",
        )

        print("[3/4] Comparing screenshots … SKIPPED (new baseline)")
        print("[4/4] No diff image generated.\n")
        print(f"  Difference detected: NO")
        print(f"  TEST RESULT: PASS  (baseline created)\n")
        return result

    # Step 3 — Compare screenshots
    print(f"       Baseline path: {baseline_path}\n")
    print("[3/4] Comparing screenshots …")

    comparison = compare_images(
        baseline_path=baseline_path,
        current_path=current_path,
        diff_dir=DIFF_DIR,
        diff_percent_threshold=threshold,
    )

    diff_detected = not comparison["passed"]
    print(f"       Changed pixels: {comparison['changed_pixels']} / {comparison['total_pixels']}")
    print(f"       Diff percent:   {comparison['diff_percent']}%\n")

    # Step 4 — Show result
    print(f"[4/4] Diff image: {comparison['diff_image_path']}\n")
    print(f"  Difference detected: {'YES' if diff_detected else 'NO'}")
    print(f"  TEST RESULT: {comparison['message']}\n")

    # Record result
    result = add_result(
        url=url,
        passed=comparison["passed"],
        diff_percent=comparison["diff_percent"],
        baseline_path=comparison["baseline_path"],
        current_path=comparison["current_path"],
        diff_image_path=comparison["diff_image_path"],
    )

    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Visual Regression Testing — CLI",
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL of the web page to test.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Maximum allowed diff percentage before FAIL (default: 0.5).",
    )
    args = parser.parse_args()

    result = run_test(url=args.url, threshold=args.threshold)
    sys.exit(0 if result.get("passed", result.get("status") == "PASS") else 1)


if __name__ == "__main__":
    main()
