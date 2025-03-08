document.addEventListener("DOMContentLoaded", () => {
    console.log("Dashboard Loaded");

    const menuItems = document.querySelectorAll(".menu-item");
    menuItems.forEach(item => {
        item.addEventListener("click", () => {
            alert(`Opening ${item.innerText}...`);
        });
    });

    document.querySelector("#logout").addEventListener("click", () => {
        alert("Logging out...");
        window.location.href = "login.html";
    });
});
