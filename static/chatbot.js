document.addEventListener("DOMContentLoaded", () => {
    console.log("Chatbot Loaded");

    const chatInput = document.querySelector("#chatInput");
    const sendBtn = document.querySelector("#sendMessage");
    const chatBox = document.querySelector("#chatBox");

    sendBtn.addEventListener("click", () => {
        let userMessage = chatInput.value.trim();
        if (userMessage) {
            chatBox.innerHTML += `<div class="user-message">${userMessage}</div>`;
            chatInput.value = "";
            setTimeout(() => {
                chatBox.innerHTML += `<div class="bot-message">I'm still learning! 😊</div>`;
            }, 1000);
        }
    });
});
