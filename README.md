# Visual Regression Testing System

Automated visual regression testing powered by Selenium, OpenCV, and Flask.

## Features

- **CLI Mode** — Run tests from the terminal with a single command
- **Web Dashboard** — Flask-based UI with URL input, screenshot comparison, and Chart.js graphs
- **Selenium Engine** — Headless Chrome captures pixel-perfect screenshots
- **OpenCV Comparison** — Detects visual differences and generates highlighted diff images
- **Docker Ready** — Containerised with Chrome pre-installed
- **CI/CD** — GitHub Actions workflow included

## Quick Start

### 1 · Install Dependencies

```bash
pip install -r requirements.txt
```

### 2 · CLI Usage

```bash
python cli.py --url https://example.com
```

### 3 · Web Dashboard

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### 4 · Docker

```bash
docker build -t vrts .
docker run -p 5000:5000 vrts
```

## Project Structure

```
visual-regression-system/
├── app.py                     # Flask web dashboard
├── cli.py                     # Command-line interface
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── .github/workflows/ci.yml   # GitHub Actions CI pipeline
├── engine/
│   ├── selenium_runner.py     # Headless Chrome screenshot capture
│   ├── image_compare.py       # OpenCV image comparison engine
│   └── result_manager.py      # Test result tracking & stats
├── templates/
│   ├── index.html             # Dashboard homepage
│   └── results.html           # Test results page
├── static/
│   ├── css/styles.css         # Dashboard stylesheet
│   └── js/dashboard.js        # Chart.js integration
└── screenshots/
    ├── baseline/              # Reference screenshots
    ├── current/               # Latest screenshots
    └── diff/                  # Highlighted difference images
```

## License

MIT
