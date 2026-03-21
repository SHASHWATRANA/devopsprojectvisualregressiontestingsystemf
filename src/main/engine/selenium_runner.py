"""
selenium_runner.py — Selenium WebDriver Screenshot Capture Engine

Responsibilities:
  1. Launch Chrome in headless mode
  2. Navigate to a given URL
  3. Capture a full-page screenshot
  4. Save the screenshot to the designated folder
  5. Return the saved file path
"""

import os
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sanitize_filename(url: str) -> str:
    """Convert a URL into a safe filename slug."""
    name = re.sub(r"https?://", "", url)
    name = re.sub(r"[^\w\-.]", "_", name)
    return name.strip("_") or "screenshot"


def _ensure_dirs(*dirs: str) -> None:
    """Create directories if they do not already exist."""
    for d in dirs:
        os.makedirs(d, exist_ok=True)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def capture_screenshot(
    url: str,
    output_dir: str = "screenshots/current",
    window_width: int = 1920,
    window_height: int = 1080,
) -> str:
    """
    Open *url* in headless Chrome, capture a screenshot, and save it.

    Parameters
    ----------
    url : str
        The web page URL to screenshot.
    output_dir : str
        Directory where the screenshot will be stored.
    window_width : int
        Browser viewport width in pixels.
    window_height : int
        Browser viewport height in pixels.

    Returns
    -------
    str
        Absolute path to the saved screenshot image.
    """

    _ensure_dirs(output_dir)

    # --- Configure headless Chrome -------------------------------------------
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--window-size={window_width},{window_height}")

    # Use webdriver-manager to auto-install the matching ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.set_page_load_timeout(30)
        driver.get(url)

        # Allow the page a moment to finish rendering / lazy-load content
        time.sleep(2)

        # Build output path
        filename = f"{_sanitize_filename(url)}.png"
        filepath = os.path.join(output_dir, filename)

        driver.save_screenshot(filepath)
        return os.path.abspath(filepath)

    finally:
        driver.quit()
