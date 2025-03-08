document.addEventListener("DOMContentLoaded", function () {
    const nextBtn = document.querySelector(".next-btn");
    const prevBtn = document.querySelector(".prev-btn");
    
    nextBtn.addEventListener("click", function (event) {
        event.preventDefault();
        
        // Validation before moving to the next step
        if (!validateSkinConcerns()) {
            alert("Please select at least one skin concern before proceeding.");
            return;
        }

        // Redirect to the next page
        window.location.href = "results.html";
    });

    prevBtn.addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = "skin _concerns.html";
    });

    function validateSkinConcerns() {
        const selectedConcerns = document.querySelectorAll('input[name="skinConcern"]:checked');
        return selectedConcerns.length > 0; // Returns true if at least one concern is selected
    }
});
