document.addEventListener("DOMContentLoaded", function () {
    // Selecting navigation buttons
    const prevButton = document.querySelector(".prev-btn");
    const nextButton = document.querySelector(".next-btn");

    // Handling "Previous" button click (redirects to the previous step)
    if (prevButton) {
        prevButton.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "previous.html"; // Replace with actual previous page
        });
    }

    // Handling "Next" button click (redirects to the next step)
    if (nextButton) {
        nextButton.addEventListener("click", function (event) {
            event.preventDefault();
            window.location.href = "skin image.html"; // Redirect to next step
        });
    }
});
