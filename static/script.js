function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        if (data.response) {
            addMessage(data.response, "bot");
        } else {
            addMessage("Xatolik yuz berdi!", "bot");
        }
    })
    .catch(() => {
        addMessage("Serverga ulanishda xatolik.", "bot");
    });
}

function addMessage(text, sender) {
    let chatBox = document.getElementById("chat-box");
    let div = document.createElement("div");
    div.classList.add("message", sender);
    div.textContent = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}
