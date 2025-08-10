# import os
# import json
# import requests
# import google.generativeai as genai
# from flask import Flask, request, jsonify, render_template_string, session

# # Flask ilovasini yaratish
# app = Flask(__name__)
# # Session ishlashi uchun maxfiy kalit. Bu loyihani boshqa joyda ishga tushirsangiz o'zgartiring.
# app.secret_key = "super_secret_key"

# # --- API kalitini sozlash ---
# # API kaliti Canvas muhiti tomonidan avtomatik ta'minlanadi
# GOOGLE_API_KEY = "AIzaSyDeiBvSI8aXD6YZUHSAUTgYDaDAVQ3NYA4"
# genai.configure(api_key=GOOGLE_API_KEY)

# # --- Modelni sozlash ---
# # Siz taqdim etgan tizim yo'riqnomasi
# system_instruction = """
# Sen "MAGISTR AI" nomli sun'iy intellekt yordamchisan.
# Sening asosiy vazifang - O'zbekistondagi abituriyentlarga va "MAGISTR" o‘quv markazi o‘quvchilariga yordam berish.

# MAGISTR o‘quv markazi haqida ma’lumot:
# - Magistr o‘quv markazi turk tili, ingliz tili, tarix, matematika va boshqa fanlardan kurslar taklif etadi.
# - Markaz abituriyentlarni OTM'ga tayyorlash, bojxona, ichki ishlar akademiyasi, Temurbeklar maktabiga tayyorlash bo‘yicha ham faoliyat yuritadi.
# - Qo‘shimcha ravishda, 5 yillik tajribaga ega malakali ustozlar dars beradi.
# - O‘quv markazi interaktiv darslar, test sinovlari va amaliy mashg‘ulotlar orqali samarali ta’lim beradi.
# - Magistr o‘quv markazining juda ko‘p filiallari mavjud.

# O‘quv markaz filiallari haqida so‘ralganda quyidagicha javob ber:
# "Magistr o‘quv markazining quyidagi filiallari mavjud: Guliston filiali, Katlavondagi Asosiy bino, Katlavondagi English CENTRE, Shirinda filial va Sirdaryo hamda boshqa hududlarda filiallar faoliyat yuritadi."

# Rahbarlar haqida so‘ralganda quyidagicha javob ber:
# "Magistr o‘quv markazi asoschisi va rahbari — Odiljon Abduahadov. Katlavondagi filiallar rahbari — Orifjon Abduahadov. Guliston filiali rahbari esa — Hulkar Yusupova."

# Aloqa ma’lumotlari (MAGISTR o‘quv markazi filiallari raqamlari):
# - Guliston filiali: +998 99 810 34 34
# - Asosiy markaz: +998 99 477 67 57
# - English CENTRE: +998 95 022 34 34

# Ijtimoiy tarmoqlar:  
# - Instagram: magistr_guliston1, magistr_edu_  
# - Telegram: magistr_guliston, magistr_boyovut

# Yaratuvchi:
# - Ushbu sun’iy intellektni Yusupov Muhammadyusufxon yaratgan.

# Qoidalar:
# - Har doim javobni oddiy matnda yoz, Markdown belgilarisiz.
# - Har bir javob oxirida yangi qatorda "Instagram: magistr_guliston1" yoz.
# - Foydalanuvchiga do‘stona ohangda, ammo aniq va foydali javob ber.
# - Ko‘p salom bermasdan, qisqa va to‘g‘ri javob berishga harakat qil.
# - Agar foydalanuvchi markaz yoki rahbar haqida so‘rasa, yuqoridagi ma’lumotlardan foydalanib tushuntir.
# - Agar foydalanuvchi “Zerikdim, boshqa mavzuga o‘taylik” yoki shunga o‘xshash gap aytsa, shunday javob ber: "Men faqat ilmiy narsalarga javob beraman. Mendan faqat bilimlaringizni mustahkamlashda foydalaning."
# - Agar foydalanuvchi boshqa mavzuda savol bersa, ilmiy va aniq javob ber.
# """

# model = genai.GenerativeModel(
#     model_name='gemini-2.5-flash',
#     system_instruction=system_instruction
# )

# # The HTML template for the chat interface. This is an all-in-one approach for simplicity.
# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Magistr AI Chat</title>
#     <!-- Tailwind CSS for styling -->
#     <script src="https://cdn.tailwindcss.com"></script>
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
#         body {
#             font-family: 'Inter', sans-serif;
#         }
#         .dot-flashing {
#             position: relative;
#             width: 10px;
#             height: 10px;
#             border-radius: 5px;
#             background-color: #9880ff;
#             color: #9880ff;
#             animation: dotFlashing 1s infinite linear alternate;
#             animation-delay: 0s;
#         }
#         .dot-flashing::before, .dot-flashing::after {
#             content: '';
#             display: inline-block;
#             position: absolute;
#             top: 0;
#         }
#         .dot-flashing::before {
#             left: -15px;
#             width: 10px;
#             height: 10px;
#             border-radius: 5px;
#             background-color: #9880ff;
#             color: #9880ff;
#             animation: dotFlashing 1s infinite alternate;
#             animation-delay: 0.5s;
#         }
#         .dot-flashing::after {
#             left: 15px;
#             width: 10px;
#             height: 10px;
#             border-radius: 5px;
#             background-color: #9880ff;
#             color: #9880ff;
#             animation: dotFlashing 1s infinite alternate;
#             animation-delay: 1s;
#         }
#         @keyframes dotFlashing {
#             0% {
#                 background-color: #9880ff;
#             }
#             50%, 100% {
#                 background-color: #6944ff;
#             }
#         }
#         .message-fade-in {
#             animation: fadeIn 0.5s ease-in-out;
#         }
#         @keyframes fadeIn {
#             from {
#                 opacity: 0;
#                 transform: translateY(10px);
#             }
#             to {
#                 opacity: 1;
#                 transform: translateY(0);
#             }
#         }
#     </style>
# </head>
# <body class="flex flex-col h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 font-sans">

#     <!-- Header -->
#     <header class="p-4 bg-white dark:bg-gray-800 shadow-md">
#         <div class="container mx-auto max-w-2xl">
#             <h1 class="text-2xl font-bold text-center">Magistr AI Chat</h1>
#         </div>
#     </header>

#     <!-- Chat Messages Container -->
#     <main id="chat-container" class="flex-1 overflow-y-auto p-4 space-y-4 max-w-2xl mx-auto w-full">
#         <!-- Messages will be dynamically added here -->
#     </main>

#     <!-- Chat Input Form -->
#     <footer class="p-4 bg-white dark:bg-gray-800 shadow-inner">
#         <div class="container mx-auto max-w-2xl">
#             <form id="chat-form" class="flex items-end space-x-2">
#                 <textarea
#                     id="user-input"
#                     class="flex-1 p-3 rounded-xl bg-gray-200 dark:bg-gray-700 resize-none outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
#                     placeholder="Xabar yozing..."
#                     rows="1"
#                     oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
#                 ></textarea>
#                 <button
#                     type="submit"
#                     id="send-btn"
#                     class="bg-blue-600 text-white p-3 rounded-xl font-semibold shadow-md hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
#                 >
#                     <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-send">
#                         <path d="m22 2-7 20-4-9-9-4 20-7Z"/><path d="M15 15l-4 4"/>
#                     </svg>
#                 </button>
#             </form>
#         </div>
#     </footer>

#     <script>
#         const form = document.getElementById('chat-form');
#         const input = document.getElementById('user-input');
#         const chatContainer = document.getElementById('chat-container');
#         const sendButton = document.getElementById('send-btn');
#         let isLoading = false;
#         let isFirstMessage = true;
        
#         // Function to handle the form submission
#         form.addEventListener('submit', async (e) => {
#             e.preventDefault();
#             const userMessageText = input.value.trim();
#             if (!userMessageText || isLoading) return;

#             addMessageToChat('user', userMessageText);
#             input.value = '';
#             input.style.height = 'auto'; // Reset textarea height
#             input.focus(); // Xabar yuborilgandan so'ng darhol fokusni qaytaramiz

#             showLoadingIndicator();
#             isLoading = true;
#             sendButton.disabled = true;

#             try {
#                 const response = await fetch('/chat', {
#                     method: 'POST',
#                     headers: { 'Content-Type': 'application/json' },
#                     body: JSON.stringify({ message: userMessageText })
#                 });

#                 if (!response.ok) {
#                     throw new Error('Serverdan javob olishda xatolik yuz berdi.');
#                 }

#                 const data = await response.json();
                
#                 hideLoadingIndicator();
                
#                 if (isFirstMessage) {
#                     isFirstMessage = false;
#                 }
                
#                 addMessageToChat('bot', data.response);

#             } catch (error) {
#                 console.error("Xatolik:", error);
#                 hideLoadingIndicator();
#                 addMessageToChat('bot', "Server bilan bog'lanishda xatolik yuz berdi.");
#             } finally {
#                 isLoading = false;
#                 sendButton.disabled = false;
#                 // Har ehtimolga qarshi, javob kelgandan keyin ham fokusni qaytaramiz
#                 input.focus(); 
#                 scrollToBottom();
#             }
#         });

#         // Add message to the chat display
#         function addMessageToChat(sender, text) {
#             const messageDiv = document.createElement('div');
#             messageDiv.classList.add('flex', 'space-x-2', 'max-w-full', 'message-fade-in');
            
#             if (sender === 'user') {
#                 messageDiv.classList.add('justify-end');
#                 messageDiv.innerHTML = `
#                     <div class="p-3 rounded-2xl max-w-sm lg:max-w-md shadow-lg bg-blue-500 text-white rounded-br-md">
#                         ${text}
#                     </div>
#                 `;
#             } else {
#                 messageDiv.classList.add('justify-start');
#                 messageDiv.innerHTML = `
#                     <div class="p-3 rounded-2xl max-w-sm lg:max-w-md shadow-lg bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-md">
#                         ${text}
#                     </div>
#                 `;
#             }
#             chatContainer.appendChild(messageDiv);
#         }

#         // Show a loading indicator
#         function showLoadingIndicator() {
#             const loadingDiv = document.createElement('div');
#             loadingDiv.id = 'loading-indicator';
#             loadingDiv.classList.add('flex', 'justify-start');
#             loadingDiv.innerHTML = `
#                 <div class="p-3 bg-gray-200 dark:bg-gray-700 rounded-2xl rounded-bl-md max-w-sm shadow-lg">
#                     <div class="dot-flashing"></div>
#                 </div>
#             `;
#             chatContainer.appendChild(loadingDiv);
#             scrollToBottom();
#         }

#         // Hide the loading indicator
#         function hideLoadingIndicator() {
#             const loadingDiv = document.getElementById('loading-indicator');
#             if (loadingDiv) {
#                 loadingDiv.remove();
#             }
#         }
        
#         // Scroll to the bottom of the chat container
#         function scrollToBottom() {
#             chatContainer.scrollTop = chatContainer.scrollHeight;
#         }

#         // Allow 'Enter' key to send message without adding a new line
#         input.addEventListener('keydown', (e) => {
#             if (e.key === 'Enter' && !e.shiftKey) {
#                 e.preventDefault();
#                 form.dispatchEvent(new Event('submit'));
#             }
#         });
        
#         // Initial welcome message from the server on page load
#         window.addEventListener('load', () => {
#             fetch('/chat', {
#                 method: 'POST',
#                 headers: { 'Content-Type': 'application/json' },
#                 body: JSON.stringify({ message: "salom" }) // Birinchi xabar
#             })
#             .then(response => response.json())
#             .then(data => {
#                 if (data.response) {
#                     addMessageToChat('bot', data.response);
#                     scrollToBottom();
#                 }
#             });
#         });
#     </script>
# </body>
# </html>
# """

# # Asosiy sahifa yo'nalishi
# @app.route("/")
# def index():
#     return render_template_string(HTML_TEMPLATE)

# # Chat xabarlarini qayta ishlash uchun yo'nalish
# @app.route("/chat", methods=["POST"])
# def handle_chat():
#     try:
#         # Chat obyektini sessiondan olish, agar bo'lmasa yangisini yaratish
#         if 'chat_history' not in session:
#             session['chat_history'] = []
        
#         # Foydalanuvchi xabarini olish
#         user_message = request.json["message"]

#         if not user_message.strip():
#             return jsonify({"error": "Bo'sh xabar yuborish mumkin emas."}), 400

#         # Birinchi xabar uchun maxsus javobni tekshirish
#         if not session.get("has_sent_first_message"):
#             session["has_sent_first_message"] = True
#             # Sizning birinchi xabar uchun belgilagan matningiz
#             response_text = "SALOM, men MAGISTR AI man. Sizga qanday yordam bera olaman?"
#         else:
#             # Model bilan aloqa o'rnatish
#             # Har bir so'rovda chat tarixini modelga yuborish
#             chat_history = session['chat_history']
#             chat = model.start_chat(history=chat_history)
#             response = chat.send_message(user_message)
#             response_text = response.text
            
#             # Chat tarixini yangilash
#             session['chat_history'].append({"role": "user", "parts": [{"text": user_message}]})
#             session['chat_history'].append({"role": "model", "parts": [{"text": response_text}]})
        
#         return jsonify({"response": response_text})

#     except Exception as e:
#         print(f"Xatolik yuz berdi: {e}")
#         return jsonify({"error": "Model bilan bog'lanishda xatolik yuz berdi."}), 500

# if __name__ == "__main__":
#     # Illovani ishga tushirish
#     app.run(host='0.0.0.0', port=5000, debug=False)


import os
import json
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string, session

# Flask ilovasini yaratish
app = Flask(__name__)
# Session ishlashi uchun maxfiy kalit. Bu loyihani boshqa joyda ishga tushirsangiz o'zgartiring.
app.secret_key = "super_secret_key"

# --- API kalitini sozlash ---
# API kaliti Canvas muhiti tomonidan avtomatik ta'minlanadi
GOOGLE_API_KEY = "AIzaSyDeiBvSI8aXD6YZUHSAUTgYDaDAVQ3NYA4"
genai.configure(api_key=GOOGLE_API_KEY)

# --- Modelni sozlash ---
# Siz taqdim etgan tizim yo'riqnomasi
system_instruction = """
Sen "MAGISTR AI" nomli sun'iy intellekt yordamchisan.
Sening asosiy vazifang - O'zbekistondagi abituriyentlarga va "MAGISTR" o‘quv markazi mijozlariga yordam berish.

MAGISTR o‘quv markazi haqida ma’lumot:
- Magistr o‘quv markazi turk tili, ingliz tili, tarix, matematika va boshqa fanlardan kurslar taklif etadi.
- Markaz abituriyentlarni OTM'ga tayyorlash, bojxona, ichki ishlar akademiyasi, Temurbeklar maktabiga tayyorlash bo‘yicha ham faoliyat yuritadi.
- Qo‘shimcha ravishda, 5 yillik tajribaga ega malakali ustozlar dars beradi.
- O‘quv markazi interaktiv darslar, test sinovlari va amaliy mashg‘ulotlar orqali samarali ta’lim beradi.
- Magistr o‘quv markazining juda ko‘p filiallari mavjud.

Rahbar:
- Odiljon Abduahadov

Aloqa ma’lumotlari (MAGISTR o‘quv markazi):
- Telefon: +998 99 810 34 34
- Instagram: magistr_guliston1
- Telegram: magistr_guliston

Yaratuvchi:
- Ushbu sun’iy intellektni Yusupov Muhammadyusufxon yaratgan.

Qoidalar:
- Har doim javobni oddiy matnda yoz, Markdown belgilarisiz.
- Har bir javob oxirida yangi qatorda "Instagram: magistr_guliston1" yoz.
- Foydalanuvchiga do‘stona ohangda, ammo aniq va foydali javob ber.
- Agar foydalanuvchi markaz yoki rahbar haqida so‘rasa, yuqoridagi ma’lumotlardan foydalanib tushuntir.
- Agar foydalanuvchi boshqa mavzuda savol bersa, ilmiy va aniq javob ber.
"""

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=system_instruction
)

# The HTML template for the chat interface. This is an all-in-one approach for simplicity.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magistr AI Chat</title>
    <!-- Tailwind CSS for styling -->
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
            background-color: #9880ff;
            color: #9880ff;
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
            background-color: #9880ff;
            color: #9880ff;
            animation: dotFlashing 1s infinite alternate;
            animation-delay: 0.5s;
        }
        .dot-flashing::after {
            left: 15px;
            width: 10px;
            height: 10px;
            border-radius: 5px;
            background-color: #9880ff;
            color: #9880ff;
            animation: dotFlashing 1s infinite alternate;
            animation-delay: 1s;
        }
        @keyframes dotFlashing {
            0% {
                background-color: #9880ff;
            }
            50%, 100% {
                background-color: #6944ff;
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
    </style>
</head>
<body class="flex flex-col h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 font-sans">

    <!-- Header -->
    <header class="p-4 bg-white dark:bg-gray-800 shadow-md">
        <div class="container mx-auto max-w-2xl flex justify-center items-center">
            <img src="https://ibb.co/ycyWLqhF" alt="Magistr AI logotipi" class="h-10">
        </div>
    </header>

    <!-- Chat Messages Container -->
    <main id="chat-container" class="flex-1 overflow-y-auto p-4 space-y-4 max-w-2xl mx-auto w-full">
        <!-- Messages will be dynamically added here -->
    </main>

    <!-- Chat Input Form -->
    <footer class="p-4 bg-white dark:bg-gray-800 shadow-inner">
        <div class="container mx-auto max-w-2xl">
            <form id="chat-form" class="flex items-end space-x-2">
                <textarea
                    id="user-input"
                    class="flex-1 p-3 rounded-xl bg-gray-200 dark:bg-gray-700 resize-none outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
                    placeholder="Xabar yozing..."
                    rows="1"
                    oninput='this.style.height = "";this.style.height = this.scrollHeight + "px"'
                ></textarea>
                <button
                    type="submit"
                    id="send-btn"
                    class="bg-blue-600 text-white p-3 rounded-xl font-semibold shadow-md hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-send">
                        <path d="m22 2-7 20-4-9-9-4 20-7Z"/><path d="M15 15l-4 4"/>
                    </svg>
                </button>
            </form>
        </div>
    </footer>

    <script>
        const form = document.getElementById('chat-form');
        const input = document.getElementById('user-input');
        const chatContainer = document.getElementById('chat-container');
        const sendButton = document.getElementById('send-btn');
        let isLoading = false;
        let isFirstMessage = true;
        
        // Function to handle the form submission
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const userMessageText = input.value.trim();
            if (!userMessageText || isLoading) return;

            addMessageToChat('user', userMessageText);
            input.value = '';
            input.style.height = 'auto'; // Reset textarea height
            input.focus(); // Xabar yuborilgandan so'ng darhol fokusni qaytaramiz

            showLoadingIndicator();
            isLoading = true;
            sendButton.disabled = true;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMessageText })
                });

                if (!response.ok) {
                    throw new Error('Serverdan javob olishda xatolik yuz berdi.');
                }

                const data = await response.json();
                
                hideLoadingIndicator();
                
                if (isFirstMessage) {
                    isFirstMessage = false;
                }
                
                addMessageToChat('bot', data.response);

            } catch (error) {
                console.error("Xatolik:", error);
                hideLoadingIndicator();
                addMessageToChat('bot', "Server bilan bog'lanishda xatolik yuz berdi.");
            } finally {
                isLoading = false;
                sendButton.disabled = false;
                // Har ehtimolga qarshi, javob kelgandan keyin ham fokusni qaytaramiz
                input.focus(); 
                scrollToBottom();
            }
        });

        // Add message to the chat display
        function addMessageToChat(sender, text) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('flex', 'space-x-2', 'max-w-full', 'message-fade-in');
            
            if (sender === 'user') {
                messageDiv.classList.add('justify-end');
                messageDiv.innerHTML = `
                    <div class="p-3 rounded-2xl max-w-sm lg:max-w-md shadow-lg bg-blue-500 text-white rounded-br-md">
                        ${text}
                    </div>
                `;
            } else {
                messageDiv.classList.add('justify-start');
                messageDiv.innerHTML = `
                    <div class="p-3 rounded-2xl max-w-sm lg:max-w-md shadow-lg bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-bl-md">
                        ${text}
                    </div>
                `;
            }
            chatContainer.appendChild(messageDiv);
        }

        // Show a loading indicator
        function showLoadingIndicator() {
            const loadingDiv = document.createElement('div');
            loadingDiv.id = 'loading-indicator';
            loadingDiv.classList.add('flex', 'justify-start');
            loadingDiv.innerHTML = `
                <div class="p-3 bg-gray-200 dark:bg-gray-700 rounded-2xl rounded-bl-md max-w-sm shadow-lg">
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
        
        // Initial welcome message from the server on page load
        window.addEventListener('load', () => {
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: "salom" }) // Birinchi xabar
            })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
                    addMessageToChat('bot', data.response);
                    scrollToBottom();
                }
            });
        });
    </script>
</body>
</html>
"""

# Asosiy sahifa yo'nalishi
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

# Chat xabarlarini qayta ishlash uchun yo'nalish
@app.route("/chat", methods=["POST"])
def handle_chat():
    try:
        # Chat obyektini sessiondan olish, agar bo'lmasa yangisini yaratish
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        # Foydalanuvchi xabarini olish
        user_message = request.json["message"]

        if not user_message.strip():
            return jsonify({"error": "Bo'sh xabar yuborish mumkin emas."}), 400

        # Birinchi xabar uchun maxsus javobni tekshirish
        if not session.get("has_sent_first_message"):
            session["has_sent_first_message"] = True
            # Sizning birinchi xabar uchun belgilagan matningiz
            response_text = "SALOM, men MAGISTR AI man. Sizga qanday yordam bera olaman?"
        else:
            # Model bilan aloqa o'rnatish
            # Har bir so'rovda chat tarixini modelga yuborish
            chat_history = session['chat_history']
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(user_message)
            response_text = response.text
            
            # Chat tarixini yangilash
            session['chat_history'].append({"role": "user", "parts": [{"text": user_message}]})
            session['chat_history'].append({"role": "model", "parts": [{"text": response_text}]})
        
        return jsonify({"response": response_text})

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return jsonify({"error": "Model bilan bog'lanishda xatolik yuz berdi."}), 500

if __name__ == "__main__":
    # Illovani ishga tushirish
    app.run(host='0.0.0.0', port=5000, debug=False)

