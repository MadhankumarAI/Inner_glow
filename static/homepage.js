document.addEventListener("DOMContentLoaded", () => {
    console.log("Homepage Loaded");

    const featureButtons = document.querySelectorAll(".feature-button");
    featureButtons.forEach(button => {
        button.addEventListener("click", () => {
            alert(`Navigating to ${button.innerText} page.`);
            window.location.href = button.dataset.target;
        });
    });
});
