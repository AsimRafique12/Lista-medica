// Example: Basic Form Validation
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", (event) => {
            const requiredFields = form.querySelectorAll("[required]");
            let isValid = true;

            requiredFields.forEach((field) => {
                if (!field.value.trim()) {
                    isValid = false;
                    alert(`${field.name} is required!`);
                    field.focus();
                }
            });

            if (!isValid) {
                event.preventDefault(); // Stop form submission
            }
        });
    }
});

// Example: Dismiss Alerts Automatically
document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.display = "none";
        }, 5000); // Hide after 5 seconds
    });
});
