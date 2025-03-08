document.addEventListener("DOMContentLoaded", () => {
    console.log("Website Loaded");

    // Dark Mode Toggle
    const themeToggle = document.querySelector("#themeToggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            document.body.classList.toggle("dark-mode");
        });
    }

    // Validate Forms
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", (event) => {
            if (!validateForm(form)) {
                event.preventDefault();
                alert("Please fill out all required fields.");
            }
        });
    });

    function validateForm(form) {
        let isValid = true;
        form.querySelectorAll("input[required]").forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add("error");
            } else {
                input.classList.remove("error");
            }
        });
        return isValid;
    }
});
