"""
image_compare.py — OpenCV Image Comparison Engine

Responsibilities:
  1. Load the baseline and current screenshots
  2. Resize images to the same dimensions (if necessary)
  3. Compute pixel-level differences using OpenCV
  4. Generate a highlighted diff image
  5. Return a result dict with PASS / FAIL status and diff metrics
"""

import os

import cv2
import numpy as np


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Pixel-difference threshold (0-255).  Differences below this are ignored.
PIXEL_THRESHOLD = 30

# Percentage of changed pixels required to flag a FAIL.
DIFF_PERCENT_THRESHOLD = 0.5  # 0.5 %

DIFF_DIR = "screenshots/diff"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compare_images(
    baseline_path: str,
    current_path: str,
    diff_dir: str = DIFF_DIR,
    pixel_threshold: int = PIXEL_THRESHOLD,
    diff_percent_threshold: float = DIFF_PERCENT_THRESHOLD,
) -> dict:
    """
    Compare two screenshots and produce a diff image.

    Parameters
    ----------
    baseline_path : str
        Path to the baseline (reference) image.
    current_path : str
        Path to the current (new) image.
    diff_dir : str
        Directory where the diff image will be saved.
    pixel_threshold : int
        Per-channel intensity delta to consider "changed".
    diff_percent_threshold : float
        Percentage of changed pixels that triggers a FAIL.

    Returns
    -------
    dict
        Keys: passed (bool), diff_percent (float), diff_image_path (str),
              baseline_path (str), current_path (str), message (str).
    """

    os.makedirs(diff_dir, exist_ok=True)

    # --- Load images --------------------------------------------------------
    baseline = cv2.imread(baseline_path)
    current = cv2.imread(current_path)

    if baseline is None:
        raise FileNotFoundError(f"Baseline image not found: {baseline_path}")
    if current is None:
        raise FileNotFoundError(f"Current image not found: {current_path}")

    # --- Resize current to match baseline if dimensions differ --------------
    if baseline.shape != current.shape:
        current = cv2.resize(current, (baseline.shape[1], baseline.shape[0]))

    # --- Compute absolute difference ----------------------------------------
    diff = cv2.absdiff(baseline, current)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply threshold to ignore negligible noise
    _, thresh = cv2.threshold(gray_diff, pixel_threshold, 255, cv2.THRESH_BINARY)

    # --- Calculate diff statistics ------------------------------------------
    total_pixels = thresh.shape[0] * thresh.shape[1]
    changed_pixels = int(np.count_nonzero(thresh))
    diff_percent = round((changed_pixels / total_pixels) * 100, 4)

    passed = diff_percent <= diff_percent_threshold

    # --- Generate diff image ------------------------------------------------
    # Highlight changed regions in red on top of the current screenshot
    diff_visual = current.copy()
    diff_visual[thresh > 0] = [0, 0, 255]  # Red overlay for changed pixels

    diff_filename = os.path.basename(current_path)
    diff_path = os.path.join(diff_dir, diff_filename)
    cv2.imwrite(diff_path, diff_visual)

    return {
        "passed": passed,
        "diff_percent": diff_percent,
        "changed_pixels": changed_pixels,
        "total_pixels": total_pixels,
        "diff_image_path": os.path.abspath(diff_path),
        "baseline_path": os.path.abspath(baseline_path),
        "current_path": os.path.abspath(current_path),
        "message": "PASS" if passed else "FAIL",
    }
