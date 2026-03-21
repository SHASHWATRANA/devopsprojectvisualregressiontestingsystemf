/**
 * dashboard.js — Chart.js integration & form UX helper
 *
 * 1. Fetches aggregate stats from /api/stats
 * 2. Renders a doughnut chart (Pass vs Fail)
 * 3. Shows a loading overlay while a test is running
 */

document.addEventListener("DOMContentLoaded", () => {
    initChart();
    initFormLoader();
});


/* ──────────────── Chart.js ──────────────── */

async function initChart() {
    const canvas = document.getElementById("results-chart");
    if (!canvas) return;

    try {
        const res  = await fetch("/api/stats");
        const data = await res.json();

        const passed = data.passed || 0;
        const failed = data.failed || 0;

        // If no data yet, show a placeholder
        if (passed === 0 && failed === 0) {
            canvas.parentElement.innerHTML =
                '<p style="text-align:center;color:#8b90a0;padding:2rem;">No data yet — run a test first.</p>';
            return;
        }

        new Chart(canvas, {
            type: "doughnut",
            data: {
                labels: ["Passed", "Failed"],
                datasets: [{
                    data: [passed, failed],
                    backgroundColor: [
                        "rgba(16, 185, 129, .85)",   /* green */
                        "rgba(239, 68, 68, .85)",    /* red   */
                    ],
                    borderColor: [
                        "rgb(16, 185, 129)",
                        "rgb(239, 68, 68)",
                    ],
                    borderWidth: 2,
                    hoverOffset: 8,
                }],
            },
            options: {
                responsive: true,
                cutout: "65%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#e2e4eb",
                            font: { family: "'Inter', sans-serif", size: 13, weight: "600" },
                            padding: 16,
                            usePointStyle: true,
                            pointStyleWidth: 14,
                        },
                    },
                    tooltip: {
                        backgroundColor: "#1a1d27",
                        titleColor: "#e2e4eb",
                        bodyColor: "#e2e4eb",
                        borderColor: "#2e3345",
                        borderWidth: 1,
                        cornerRadius: 8,
                        padding: 12,
                    },
                },
                animation: {
                    animateRotate: true,
                    duration: 1000,
                },
            },
        });

    } catch (err) {
        console.error("Failed to load chart data:", err);
    }
}


/* ──────────── Form Loading Overlay ──────────── */

function initFormLoader() {
    const form    = document.getElementById("test-form");
    const overlay = document.getElementById("loading-overlay");
    if (!form || !overlay) return;

    form.addEventListener("submit", () => {
        overlay.classList.add("active");
    });
}
