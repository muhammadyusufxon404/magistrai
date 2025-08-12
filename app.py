import os
import json
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string, session
import base64
import mimetypes

# Flask ilovasini yaratish
app = Flask(__name__)
# Session ishlashi uchun maxfiy kalit. Bu loyihani boshqa joyda ishga tushirsangiz o'zgartiring.
app.secret_key = "super_secret_key"

# --- API kalitini sozlash ---
# Sizning haqiqiy API kalitingizni bu yerga joylashtiring
GOOGLE_API_KEY = "AIzaSyDeiBvSI8aXD6YZUHSAUTgYDaDAVQ3NYA4"
genai.configure(api_key=GOOGLE_API_KEY)

# --- Modelni sozlash ---
system_instruction = """
Sen "MAGISTR AI" nomli sun'iy intellekt yordamchisan.
Sening asosiy vazifang - O'zbekistondagi abituriyentlarga va "MAGISTR" o‘quv markazi o‘quvchilariga yordam berish.

MAGISTR o‘quv markazi haqida ma’lumot:
- Magistr o‘quv markazi turk tili, ingliz tili, tarix, matematika va boshqa fanlardan kurslar taklif etadi.
- Markaz abituriyentlarni OTM'ga tayyorlash, bojxona, ichki ishlar akademiyasi, Temurbeklar maktabiga tayyorlash bo‘yicha ham faoliyat yuritadi.
- Qo‘shimcha ravishda, 5 yillik tajribaga ega malakali ustozlar dars beradi.
- O‘quv markazi interaktiv darslar, test sinovlari va amaliy mashg‘ulotlar orqali samarali ta’lim beradi.
- Magistr o‘quv markazining juda ko‘p filiallari mavjud.

O‘quv markaz filiallari haqida so‘ralganda quyidagicha javob ber:
"Magistr o‘quv markazining quyidagi filiallari mavjud: Guliston filiali, Katlavondagi Asosiy bino, Katlavondagi English CENTRE, Shirinda filial va Sirdaryo hamda boshqa hududlarda filiallar faoliyat yuritadi."

Rahbarlar haqida so‘ralganda quyidagicha javob ber:
"Magistr o‘quv markazi asoschisi va rahbari — Odiljon Abduahadov. Katlavondagi filiallar rahbari — Orifjon Abduahadov. Guliston filiali rahbari esa — Hulkar Yusupova."

Aloqa ma’lumotlari (MAGISTR o‘quv markazi filiallari raqamlari):
- Guliston filiali: +998 99 810 34 34
- Asosiy markaz: +998 99 477 67 57
- English CENTRE: +998 95 022 34 34

Ijtimoiy tarmoqlar:  
- Instagram: magistr_guliston1, magistr_edu_  
- Telegram: magistr_guliston, magistr_boyovut

Yaratuvchi:
- Ushbu sun’iy intellektni Yusupov Muhammadyusufxon yaratgan.

Qoidalar:
- Har doim javobni oddiy matnda yoz, Markdown belgilarisiz.
- Har bir javob oxirida yangi qatorda "Instagram: magistr_guliston1" yoz.
- Foydalanuvchiga do‘stona ohangda, ammo aniq va foydali javob ber.
- Ko‘p salom bermasdan, qisqa va to‘g‘ri javob berishga harakat qil.
- Agar foydalanuvchi markaz yoki rahbar haqida so‘rasa, yuqoridagi ma’lumotlardan foydalanib tushuntir.
- Agar foydalanuvchi “Zerikdim, boshqa mavzuga o‘taylik” yoki shunga o‘xshash gap aytsa, shunday javob ber: "Men faqat ilmiy narsalarga javob beraman. Mendan faqat bilimlaringizni mustahkamlashda foydalaning."
- Agar foydalanuvchi boshqa mavzuda savol bersa, ilmiy va aniq javob ber.
"""

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=system_instruction
)

# Dark mode HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAGISTR AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
        }
        .dot-flashing {
            position: relative;
            width: 10px;
            height: 10px;
            border-radius: 5px;
            background-color: #6d28d9; /* Indigo-700 */
            color: #6d28d9;
            animation: dotFlashing 1s infinite linear alternate;
            animation-delay: 0s;
        }
        .dot-flashing::before, .dot-flashing::after {
            content: '';
            display: inline-block;
            position: absolute;
            top: 0;
        }
        .dot-flashing::before {
            left: -15px;
            width: 10px;
            height: 10px;
            border-radius: 5px;
            background-color: #6d28d9;
            color: #6d28d9;
            animation: dotFlashing 1s infinite alternate;
            animation-delay: 0.5s;
        }
        .dot-flashing::after {
            left: 15px;
            width: 10px;
            height: 10px;
            border-radius: 5px;
            background-color: #6d28d9;
            color: #6d28d9;
            animation: dotFlashing 1s infinite alternate;
            animation-delay: 1s;
        }
        @keyframes dotFlashing {
            0% {
                background-color: #6d28d9;
            }
            50%, 100% {
                background-color: #4c1d95; /* Indigo-900 */
            }
        }
        .message-fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        #image-preview-container {
            display: flex;
            gap: 8px;
            margin-top: 8px;
            flex-wrap: wrap;
        }
        .image-preview {
            position: relative;
            width: 100px;
            height: 100px;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #475569; /* Slate-600 */
        }
        .image-preview img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .remove-image {
            position: absolute;
            top: 4px;
            right: 4px;
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 12px;
        }
        .user-message {
            background-color: #3b82f6; /* Blue-500 */
            color: white;
            border-radius: 1rem 0.25rem 1rem 1rem;
        }
        .bot-message {
            background-color: #334155; /* Slate-700 */
            color: white;
            border-radius: 0.25rem 1rem 1rem 1rem;
        }
        /* Markdown support styles */
        .bot-message strong, .bot-message b {
            font-weight: bold;
        }
        .bot-message em, .bot-message i {
            font-style: italic;
        }
        .bot-message ul {
            list-style-type: disc;
            padding-left: 20px;
        }
        .bot-message li {
            margin-bottom: 5px;
        }
        .bot-message h1, .bot-message h2, .bot-message h3 {
            font-size: 1.25em;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 5px;
        }
    </style>
</head>
<body class="flex flex-col h-screen bg-gray-900 text-gray-200 font-sans">

    <header class="p-4 bg-gray-800 shadow-lg">
        <div class="container mx-auto max-w-2xl">
            <h1 class="text-2xl font-bold text-center text-indigo-400">MAGISTR AI</h1>
        </div>
    </header>

    <main id="chat-container" class="flex-1 overflow-y-auto p-4 space-y-4 max-w-2xl mx-auto w-full">
        <div class="flex justify-start space-x-2 max-w-full">
            <div class="p-3 rounded-2xl max-w-sm lg:max-w-md shadow-lg bot-message message-fade-in">
                Men Magistr AI'man. Sizga qanday yordam bera olaman?
                <br>
                Instagram: magistr_guliston1
            </div>
        </div>
    </main>

    <footer class="p-4 bg-gray-800 shadow-lg">
        <div class="container mx-auto max-w-2xl">
            <div id="image-preview-container" class="mb-2"></div>
            
            <form id="chat-form" class="flex items-end space-x-2" enctype="multipart/form-data">
                <label class="cursor-pointer flex-shrink-0">
                    <input type="file" id="image-upload" accept="image/*" class="hidden" multiple>
                    <div class="p-3 bg-gray-700 text-indigo-400 rounded-xl hover:bg-gray-600 transition-colors duration-200">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-image"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>
                    </div>
                </label>

                <textarea
                    id="user-input"
                    class="flex-1 p-3 rounded-xl bg-gray-700 text-gray-200 resize-none outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200"
                    placeholder="Xabar yozing..."
                    rows="1"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                ></textarea>
                
                <button
                    type="submit"
                    id="send-btn"
                    class="flex-shrink-0 bg-indigo-600 text-white p-3 rounded-xl font-semibold shadow-md hover:bg-indigo-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-send"><path d="m22 2-7 20-4-9-9-4 20-7Z"/><path d="M15 15l-4 4"/></svg>
                </button>
            </form>
        </div>
    </footer>

    <script>
        const form = document.getElementById('chat-form');
        const input = document.getElementById('user-input');
        const imageInput = document.getElementById('image-upload');
        const chatContainer = document.getElementById('chat-container');
        const sendButton = document.getElementById('send-btn');
        const imagePreviewContainer = document.getElementById('image-preview-container');
        let isLoading = false;
        let selectedFiles = [];

        // Image upload change event
        imageInput.addEventListener('change', () => {
            selectedFiles = [...selectedFiles, ...Array.from(imageInput.files)];
            imageInput.value = null; // Clear input to allow re-selection of the same file
            updateImagePreview();
        });

        // Update image preview
        function updateImagePreview() {
            imagePreviewContainer.innerHTML = '';
            selectedFiles.forEach((file, index) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const previewDiv = document.createElement('div');
                    previewDiv.className = 'image-preview';
                    previewDiv.innerHTML = `
                        <img src="${e.target.result}" alt="Preview">
                        <span class="remove-image" data-index="${index}">&times;</span>
                    `;
                    imagePreviewContainer.appendChild(previewDiv);
                };
                reader.readAsDataURL(file);
            });
        }
        
        // Remove image from preview
        imagePreviewContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-image')) {
                const index = e.target.getAttribute('data-index');
                selectedFiles.splice(index, 1);
                updateImagePreview();
            }
        });

        // Form submit
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userMessageText = input.value.trim();
            const imagesToUpload = selectedFiles;

            if ((!userMessageText && imagesToUpload.length === 0) || isLoading) {
                return;
            }

            addMessageToChat('user', userMessageText, imagesToUpload);
            input.value = '';
            input.style.height = 'auto';
            selectedFiles = []; // Clear selected files
            imagePreviewContainer.innerHTML = '';
            input.focus();

            showLoadingIndicator();
            isLoading = true;
            sendButton.disabled = true;

            const formData = new FormData();
            formData.append('message', userMessageText);
            imagesToUpload.forEach(file => {
                formData.append('images', file);
            });

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error('Serverdan javob olishda xatolik yuz berdi.');
                }

                const data = await response.json();
                
                hideLoadingIndicator();
                
                addMessageToChat('bot', data.response);

            } catch (error) {
                console.error("Xatolik:", error);
                hideLoadingIndicator();
                addMessageToChat('bot', "Server bilan bog'lanishda xatolik yuz berdi.");
            } finally {
                isLoading = false;
                sendButton.disabled = false;
                input.focus(); 
                scrollToBottom();
            }
        });

        // --- YANGI FUNKSIYA: MARKDOWN BELGILARINI HTMLGA O'TKAZISH ---
        function parseMarkdown(text) {
            // Qalin yozuv (***text***, **text**)
            text = text.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
            text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            // Egik yozuv (*text*, _text_)
            text = text.replace(/(?<!\*)\*(?!\*)(.*?)\*(?!\*)/g, '<em>$1</em>');
            text = text.replace(/_(.*?)_/g, '<em>$1</em>');
            // Ro'yxatlar (-)
            text = text.replace(/^- (.*)/gm, '<li>$1</li>');
            if (text.includes('<li>')) {
                text = `<ul>${text}</ul>`;
            }
            // Yangi qator (\\n)
            text = text.replace(/\\n/g, '<br>');
            return text;
        }

        // Add message to the chat display, now with image support
        function addMessageToChat(sender, text, imageFiles = []) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('flex', 'space-x-2', 'max-w-full', 'message-fade-in');
            
            let contentHtml = '';
            if (imageFiles.length > 0) {
                contentHtml += '<div class="flex flex-wrap gap-2 mb-2">';
                imageFiles.forEach(file => {
                    const imageUrl = URL.createObjectURL(file);
                    contentHtml += `<img src="${imageUrl}" alt="Yuborilgan rasm" class="rounded-lg max-w-full h-auto" style="max-height: 150px;">`;
                });
                contentHtml += '</div>';
            }
            if (text) {
                const formattedText = parseMarkdown(text);
                contentHtml += `<div>${formattedText}</div>`;
            }

            if (sender === 'user') {
                messageDiv.classList.add('justify-end');
                messageDiv.innerHTML = `
                    <div class="p-3 rounded-2xl max-w-sm lg:max-w-md shadow-lg user-message">
                        ${contentHtml}
                    </div>
                `;
            } else {
                messageDiv.classList.add('justify-start');
                messageDiv.innerHTML = `
                    <div class="p-3 rounded-2xl max-w-sm lg:max-w-md shadow-lg bot-message">
                        ${contentHtml}
                    </div>
                `;
            }
            chatContainer.appendChild(messageDiv);
            scrollToBottom();
        }

        // Show a loading indicator
        function showLoadingIndicator() {
            const loadingDiv = document.createElement('div');
            loadingDiv.id = 'loading-indicator';
            loadingDiv.classList.add('flex', 'justify-start');
            loadingDiv.innerHTML = `
                <div class="p-3 bg-gray-700 rounded-2xl rounded-bl-md max-w-sm shadow-lg">
                    <div class="dot-flashing"></div>
                </div>
            `;
            chatContainer.appendChild(loadingDiv);
            scrollToBottom();
        }

        // Hide the loading indicator
        function hideLoadingIndicator() {
            const loadingDiv = document.getElementById('loading-indicator');
            if (loadingDiv) {
                loadingDiv.remove();
            }
        }
        
        // Scroll to the bottom of the chat container
        function scrollToBottom() {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Allow 'Enter' key to send message without adding a new line
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                form.dispatchEvent(new Event('submit'));
            }
        });
        
    </script>
</body>
</html>
"""

def create_image_part(image_data, mime_type):
    """
    Rasm ma'lumotlarini modelga mos formatga o'tkazadi.
    """
    return {
        "inline_data": {
            "data": image_data,
            "mime_type": mime_type
        }
    }

# Asosiy sahifa yo'nalishi
@app.route("/")
def index():
    # Sahifa yuklanganda hech qanday so'rov jo'natilmaydi, birinchi xabar HTMLda bo'ladi.
    return render_template_string(HTML_TEMPLATE)

# Chat xabarlarini qayta ishlash uchun yo'nalish
@app.route("/chat", methods=["POST"])
def handle_chat():
    try:
        # Chat obyektini sessiondan olish, agar bo'lmasa yangisini yaratish
        if 'chat_history' not in session:
            session['chat_history'] = []

        user_message = request.form.get("message", "").strip()
        image_files = request.files.getlist("images")
        
        if not user_message and not image_files:
            return jsonify({"error": "Bo'sh xabar yoki rasm yuborish mumkin emas."}), 400

        # Modelga yuborish uchun kontentni yaratish
        content_parts = []
        if user_message:
            content_parts.append(user_message)

        for image_file in image_files:
            # Rasmni base64 formatiga o'tkazish
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            mime_type = image_file.mimetype or "image/jpeg"
            content_parts.append(create_image_part(base64_image, mime_type))
        
        # Har bir so'rovda chat tarixini modelga yuborish
        chat = model.start_chat(history=session['chat_history'])
        response = chat.send_message(content_parts)
        response_text = response.text
        
        # Chat tarixini yangilash
        user_parts = []
        if user_message:
            user_parts.append({"text": user_message})
        for image_file in image_files:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            mime_type = image_file.mimetype or "image/jpeg"
            user_parts.append(create_image_part(base64_image, mime_type))
        session['chat_history'].append({"role": "user", "parts": user_parts})
        
        session['chat_history'].append({"role": "model", "parts": [{"text": response_text}]})
        
        return jsonify({"response": response_text})

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return jsonify({"error": "Model bilan bog'lanishda xatolik yuz berdi."}), 500

if __name__ == "__main__":
    # Illovani ishga tushirish
    app.run(host='0.0.0.0', port=5000, debug=False)
