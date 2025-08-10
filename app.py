import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "super_secret_key"

# --- API kalitini sozlash ---
GOOGLE_API_KEY = "AIzaSyDeiBvSI8aXD6YZUHSAUTgYDaDAVQ3NYA4"
genai.configure(api_key=GOOGLE_API_KEY)

# --- Modelni sozlash ---
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
    model_name='gemini-2.0-flash',
    system_instruction=system_instruction
)
chat = model.start_chat(history=[])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def handle_chat():
    try:
        user_message = request.json["message"]

        if not user_message.strip():
            return jsonify({"error": "Bo'sh xabar yuborish mumkin emas."}), 400

        if not session.get("has_sent_first_message"):
            session["has_sent_first_message"] = True
            return jsonify({"response": "SALOM, men MAGISTR AI man. Sizga qanday yordam bera olaman?"})

        response = chat.send_message(user_message)
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return jsonify({"error": "Model bilan bog'lanishda xatolik yuz berdi."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
