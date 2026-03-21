# ──────────────────────────────────────────────────────────────
#  Dockerfile — Visual Regression Testing System
#  Location: infrastructure/docker/Dockerfile
#  Build from project root:
#    docker build -f infrastructure/docker/Dockerfile .
#
#  Builds a container with:
#    . Python 3.12
#    . Google Chrome (headless)
#    . ChromeDriver (matching version, via webdriver-manager)
#    . Project Python dependencies
#    . Flask / Gunicorn served on port 5000
# ──────────────────────────────────────────────────────────────

FROM python:3.12-slim

# ── Environment ──────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# ── System dependencies + Chrome ─────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        gnupg2 \
        unzip \
        curl \
        fonts-liberation \
        libnss3 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libgbm1 \
        libasound2 \
        libpangocairo-1.0-0 \
        libcups2 \
        libdrm2 \
        xdg-utils \
    && wget -qO - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y --no-install-recommends google-chrome-stable \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Copy & install Python dependencies ─────────────────────
WORKDIR /app
COPY src/main/config/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ── Copy full project ───────────────────────────────────────
COPY . .

# ── Create screenshot directories ───────────────────────────
RUN mkdir -p src/main/screenshots/baseline src/main/screenshots/current src/main/screenshots/diff

# ── Set working directory to the Flask app ──────────────────
WORKDIR /app/src/main

# ── Expose Flask port ────────────────────────────────────────
EXPOSE 5000

# ── Start Gunicorn ───────────────────────────────────────────
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
