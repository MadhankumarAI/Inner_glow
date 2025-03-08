document.addEventListener("DOMContentLoaded", () => {
    console.log("Login Page Loaded");

    document.querySelector("#loginForm").addEventListener("submit", (event) => {
        event.preventDefault();
        const email = document.querySelector("#email").value.trim();
        const password = document.querySelector("#password").value.trim();

        if (!email || password.length < 8) {
            alert("Invalid credentials.");
            return;
        }

        alert("Login Successful!");
        window.location.href = "dashboard.html";
    });
});
