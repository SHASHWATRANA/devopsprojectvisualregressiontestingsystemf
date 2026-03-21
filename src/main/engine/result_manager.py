"""
result_manager.py — Test Result Tracking & Statistics

Responsibilities:
  1. Record individual test results (URL, status, paths, timestamp)
  2. Persist results to a JSON file so they survive server restarts
  3. Provide aggregate statistics (total, passed, failed)
"""

import json
import os
from datetime import datetime, timezone


RESULTS_FILE = "test_results.json"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_results(filepath: str = RESULTS_FILE) -> list:
    """Load previously saved results from disk."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return []


def _save_results(results: list, filepath: str = RESULTS_FILE) -> None:
    """Persist results list to disk as JSON."""
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, default=str)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def add_result(
    url: str,
    passed: bool,
    diff_percent: float = 0.0,
    baseline_path: str = "",
    current_path: str = "",
    diff_image_path: str = "",
) -> dict:
    """
    Record a new test result.

    Returns the newly created result dict.
    """

    result = {
        "url": url,
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "diff_percent": diff_percent,
        "baseline_path": baseline_path,
        "current_path": current_path,
        "diff_image_path": diff_image_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    results = _load_results()
    results.append(result)
    _save_results(results)
    return result


def get_all_results() -> list:
    """Return the full list of recorded results (newest last)."""
    return _load_results()


def get_statistics() -> dict:
    """
    Return aggregate statistics.

    Returns
    -------
    dict
        Keys: total (int), passed (int), failed (int).
    """

    results = _load_results()
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    failed = total - passed

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
    }


def clear_results() -> None:
    """Delete all recorded results."""
    _save_results([])
