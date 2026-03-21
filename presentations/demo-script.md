# VRTS Demo Script

## 1. Introduction
"Hello, my name is Shashwat Rana, Registration Number 23fe10cse00101. This is my presentation for CSE3253 DevOps [PE6]. Today I will demonstrate my Visual Regression Testing System (VRTS)."

## 2. Infrastructure & Code Walkthrough
- Show the DevOps directory structure (`src/`, `infrastructure/`, `pipelines/`, `docs/`).
- Show the `Dockerfile` and explain the inclusion of headless Chrome.
- Show the `.github/workflows/ci.yml` file and explain the automated CI/CD pipeline.

## 3. Web Dashboard Demo
- Run `docker-compose up -d` or `python src/main/app.py`.
- Open `localhost:5000`.
- Enter `https://example.com` and run the test.
- Show the first run resulting in an automatic PASS (baseline created).

## 4. Visual Regression Detection (CLI or Web)
- Run `python src/main/cli.py --url https://github.com/SHASHWATRANA`.
- Explain how OpenCV compares the pixels and generates the highlighted diff image.
- Show the final PASS/FAIL result.

## 5. Cloud Deployment
- Navigate to the live Render.com URL: `https://vrts-dashboard.onrender.com`.
- Demonstrate that the container runs seamlessly in the cloud automatically built from GitHub.

## 6. Conclusion
"VRTS solves the problem of unintended visual changes by catching them automatically in the CI/CD pipeline via Docker and Selenium. Thank you."
