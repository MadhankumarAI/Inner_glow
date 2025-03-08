document.addEventListener("DOMContentLoaded", function () {
    const prevButton = document.querySelector(".prev-btn");
    const nextButton = document.querySelector(".next-btn");

    // List of pages in the correct order
    const pages = ["basic_info.html", "skin image.html", "skin _concerns.html", "skin_results.html"];
    
    // Get the current page filename
    const currentPage = window.location.pathname.split("/").pop();
    const currentIndex = pages.indexOf(currentPage);

    // Disable "Previous" button on first step
    if (currentIndex === 0) {
        prevButton.style.display = "none"; // Hide previous button on the first page
    } else {
        prevButton.href = pages[currentIndex - 1]; // Set previous page link
    }

    // Disable "Next" button on the last step
    if (currentIndex === pages.length - 1) {
        nextButton.style.display = "none"; // Hide next button on the last page
    } else {
        nextButton.href = pages[currentIndex + 1]; // Set next page link
    }
});
