import os
from dotenv import load_dotenv
from google import genai
from PIL import Image, UnidentifiedImageError# Rasmlar bilan ishlash uchun

from celery import shared_task

import json
load_dotenv() # .env fayldagi o'zgaruvchilarni yuklaydi


api_keys = [os.environ.get("GEMiNI_API"), os.environ.get("GEMiNI_API2"),
            os.environ.get("GEMiNI_API3"), os.environ.get("GEMiNI_API4")]
index = 0
security = "Do not use any Markdown formatting. Strictly prohibit the use of asterisks (*) and double asterisks (**) for bolding, lists, or emphasis. Return only plain text"
chat_history = []


@shared_task
def generate_AI(text= None, file = None, translate_lang=None):
    contents = []
    image_obj = None
    if file is not None:
        try:
            if isinstance(file, str):
                image_obj = Image.open(file)
                contents.append(image_obj)
            else:
                image_obj = Image.open(file)  # ← shu qatorni o'zgartiring
                contents.append(image_obj)  # ← bu qatorni ham qo'shing
        except Exception as e:
            return {"error": f"Rasmni ochishda xato: {e}"}
    global index, security, chat_history
    if file and translate_lang:
        text = """
        Extract all text from the image exactly as it appears.
        DO NOT translate programming code, variable names, class names, or any code syntax.
        Only translate human-readable text and comments.
        Return ONLY as JSON: {'original_text': '...', 'translated_text': '...'}
        """
        text += security
        if translate_lang:
            text += (f" After extraction, automatically identify the source language and translate the text into "
                     f"{translate_lang}, preserving the original layout.")
        client = genai.Client(api_key=api_keys[index])
        try:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=[text, image_obj]
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Xato berdi: {e}")
            index += 1  # Keyingi keyga o'tamiz
            # Agar hamma keylar tugagan bo'lsa
            if index >= len(api_keys):
                # Keyni nolga qaytarib qo'yamiz (ertaga yana ishlashi uchun)
                index = 0
                return "Kechirasiz, barcha limitlarimiz tugadi. Keyinroq urinib ko'ring."
            return generate_AI(text, file, translate_lang)  # Xatolik yuz bersa, qayta urinib ko'rish


    else:
        if text:
            contents.append(text)
        text += security
        client = genai.Client(api_key=api_keys[index])
        if translate_lang:
            text += (f" After extraction, automatically identify the source language and translate the text into "
                     f"{translate_lang}, preserving the original layout.")

        try:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=contents
            )
            return response.text
        except Exception as e:
            xato = f"Xato berdi: {e}"
            index += 1  # Keyingi keyga o'tamiz
            if index >= len(api_keys):
                index = 0
                return "Kechirasiz, barcha limitlarimiz tugadi. Keyinroq urinib ko'ring."
            return generate_AI(text, image_obj, translate_lang)  # Xatolik yuz bersa, qayta urinib ko'rish


@shared_task
def AI_image_chat(text, file_path):
    return generate_AI(text=text, file=file_path)

@shared_task
def AI_chat(text):
    return generate_AI(text=text)

@shared_task
def AI_translate_image(text, image, target_lang):
    return generate_AI(text=text, file=image ,translate_lang=target_lang)














































# # Modellarni ko'rishning eng oddiy yo'li
# for model in client.models.list():
#     # Yangi SDKda modelning nomi model.name da bo'ladi
#     print(f"Model: {model.name}")



