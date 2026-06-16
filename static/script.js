// ==========================
// Character Counter
// ==========================

document.addEventListener("DOMContentLoaded", () => {

    const textarea =
        document.querySelector("textarea");

    const counter =
        document.getElementById("char-count");

    if (textarea && counter) {

        textarea.addEventListener(
            "input",
            () => {

                counter.innerText =
                    `${textarea.value.length} characters`;

            }
        );

    }

});

// ==========================
// Loading Button
// ==========================

document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.querySelector("form");

    const button =
        document.getElementById("analyze-btn");

    if (form && button) {

        form.addEventListener(
            "submit",
            () => {

                button.innerText =
                    "Analyzing...";

                button.disabled = true;

            }
        );

    }

});

// ==========================
// Animated Risk Bar
// ==========================

document.addEventListener("DOMContentLoaded", () => {

    const riskBar =
        document.querySelector(".risk-bar");

    if (riskBar) {

        const width =
            riskBar.getAttribute(
                "data-score"
            );

        riskBar.style.width = "0%";

        setTimeout(() => {

            riskBar.style.width =
                width + "%";

        }, 200);

    }

});

// ==========================
// Copy AI Analysis
// ==========================

function copyAnalysis() {

    const analysis =
        document.querySelector(
            ".analysis-card pre"
        );

    if (!analysis) return;

    navigator.clipboard
        .writeText(
            analysis.innerText
        )
        .then(() => {

            alert(
                "Analysis copied successfully!"
            );

        });

}

// ==========================
// Clear History Confirmation
// ==========================

function confirmClearHistory() {

    return confirm(
        "Are you sure you want to delete all analysis history?\n\nThis action cannot be undone."
    );

}

// ==========================
// Dashboard Charts
// ==========================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const emailChartCanvas =
            document.getElementById(
                "emailChart"
            );

        if (emailChartCanvas) {

            new Chart(
                emailChartCanvas,
                {
                    type: "pie",

                    data: {

                        labels: [
                            "Safe Emails",
                            "Phishing Emails"
                        ],

                        datasets: [

                            {
                                data: [
                                    safeCount,
                                    phishingCount
                                ]
                            }

                        ]
                    }
                }
            );

        }

        const riskChartCanvas =
            document.getElementById(
                "riskChart"
            );

        if (riskChartCanvas) {

            new Chart(
                riskChartCanvas,
                {
                    type: "bar",

                    data: {

                        labels: [
                            "Critical",
                            "High",
                            "Medium",
                            "Low"
                        ],

                        datasets: [

                            {
                                label:
                                "Risk Distribution",

                                data: [
                                    criticalCount,
                                    highCount,
                                    mediumCount,
                                    lowCount
                                ]
                            }

                        ]
                    }
                }
            );

        }

    }
);