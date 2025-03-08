document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("fileUpload");
    const preview = document.getElementById("photoPreview");
    const submitBtn = document.getElementById("submitBtn");

    // Show image preview when selected
    fileInput.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" class="preview-image">`;
            };
            reader.readAsDataURL(file);
        }
    });

    // Upload image to Flask server
    submitBtn.addEventListener("click", function () {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select an image first!");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        fetch("/skin_image", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});
