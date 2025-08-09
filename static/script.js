document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const sendButton = document.getElementById("send-button");

    // Forma yuborilganda...
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // Sahifani yangilanishini oldini olish

        const messageText = userInput.value.trim();
        if (!messageText) return; // Bo'sh xabar yubormaslik

        // Foydalanuvchi xabarini ekranga chiqarish
        addMessage(messageText, "user");
        userInput.value = ""; // Inputni tozalash
        sendButton.disabled = true; // Yuborish tugmasini bloklash

        // "Yozmoqda..." indikatorini ko'rsatish
        showTypingIndicator();

        try {
            // Backend'ga so'rov yuborish
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: messageText }),
            });

            // "Yozmoqda..." indikatorini o'chirish
            hideTypingIndicator();

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Serverda xatolik yuz berdi.");
            }

            const data = await response.json();
            // Bot javobini ekranga chiqarish
            addMessage(data.response, "bot");

        } catch (error) {
            // Xatolik xabarini ekranga chiqarish
            addMessage(`Uzr, xatolik yuz berdi: ${error.message}`, "bot");
            hideTypingIndicator(); // Xatolik bo'lsa ham indikatorni o'chirish
        } finally {
            sendButton.disabled = false; // Tugmani yana aktiv qilish
            userInput.focus(); // Inputga fokusni qaytarish
        }
    });

    // Ekranga xabar qo'shish funksiyasi
    function addMessage(text, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);

        const contentElement = document.createElement("div");
        contentElement.classList.add("message-content");
        contentElement.textContent = text;

        messageElement.appendChild(contentElement);
        chatBox.appendChild(messageElement);

        // Oynani pastga aylantirish
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // "Yozmoqda..." indikatorini ko'rsatish
    function showTypingIndicator() {
        const indicator = document.createElement("div");
        indicator.id = "typing-indicator";
        indicator.classList.add("message", "bot-message", "typing-indicator");
        indicator.innerHTML = `
            <div class="message-content">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        chatBox.appendChild(indicator);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // "Yozmoqda..." indikatorini o'chirish
    function hideTypingIndicator() {
        const indicator = document.getElementById("typing-indicator");
        if (indicator) {
            indicator.remove();
        }
    }
});
