"""
ScholarMap AI Service
---------------------
Barcha Gemini AI funksiyalari shu yerda.
Thread-safe API key rotation, xatoliklarga bardosh (retry logic) mavjud.
"""
import os
import json
import logging
import threading

from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

logger = logging.getLogger(__name__)

# ─── API Key boshqaruvi (Thread-safe) ─────────────────────────────────────────
_api_keys = [
    k for k in [
        os.environ.get("GEMiNI_API"),
        os.environ.get("GEMiNI_API2"),
        os.environ.get("GEMiNI_API3"),
        os.environ.get("GEMiNI_API4"),
    ] if k  # None bo'lganlarni olib tashlaydi
]
_key_lock = threading.Lock()
_key_index = 0

MODEL_NAME = "gemini-2.0-flash"
NO_MARKDOWN = (
    "Do not use any Markdown formatting. "
    "Strictly prohibit asterisks (*), double asterisks (**), "
    "hash signs (#) for headers, or any other Markdown syntax. "
    "Return only clean plain text."
)


def _get_client():
    """Thread-safe API kalitini olish va client yaratish."""
    global _key_index
    with _key_lock:
        if not _api_keys:
            raise RuntimeError("Hech qanday Gemini API kalit topilmadi (.env faylini tekshiring).")
        key = _api_keys[_key_index]
    return genai.Client(api_key=key)


def _rotate_key():
    """Limit tuganda keyingi kalitga o'tish."""
    global _key_index
    with _key_lock:
        _key_index = (_key_index + 1) % len(_api_keys)
    logger.warning(f"API key rotated to index {_key_index}")


def _call_gemini(contents: list, max_retries: int = 4) -> str:
    """Gemini modeliga so'rov yuborish — avtomatik retry."""
    for attempt in range(max_retries):
        try:
            client = _get_client()
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini xatosi (urinish {attempt + 1}/{max_retries}): {e}")
            _rotate_key()
    return "Kechirasiz, barcha AI limitlarimiz tugadi. Keyinroq urinib ko'ring."


# ─── Asosiy funksiyalar ────────────────────────────────────────────────────────

def AI_chat(text: str) -> str:
    """Oddiy matn bilan suhbat."""
    if not text or not text.strip():
        return "Matn bo'sh bo'lmasligi kerak."
    prompt = f"{NO_MARKDOWN}\n\n{text}"
    return _call_gemini([prompt])


def AI_image_chat(text: str, file_obj) -> str:
    """Rasm + matn bilan suhbat."""
    try:
        file_obj.seek(0)
        image = Image.open(file_obj)
        image.load()
    except Exception as e:
        return f"Rasmni ochishda xato: {e}"
    prompt = f"{NO_MARKDOWN}\n\n{text or 'Ushbu rasmni tahlil qil.'}"
    return _call_gemini([prompt, image])


def AI_translate_image(text: str, file_obj, target_lang: str) -> dict:
    """Rasmdan matn ajratib tarjima qilish."""
    try:
        file_obj.seek(0)
        image = Image.open(file_obj)
        image.load()
    except Exception as e:
        return {"error": f"Rasmni ochishda xato: {e}"}

    prompt = (
        f"Extract all text from the image exactly as it appears. "
        f"DO NOT translate programming code, variable names, or code syntax. "
        f"Only translate human-readable text and comments. "
        f"Translate into: {target_lang}. "
        f"Return ONLY valid JSON with this exact format: "
        f'{{\"original_text\": \"...\", \"translated_text\": \"...\"}}'
        f"\n\n{NO_MARKDOWN}"
    )
    raw = _call_gemini([prompt, image])
    try:
        # JSON atrofidagi keraksiz narsalarni tozalash
        raw_clean = raw.strip().strip("```json").strip("```").strip()
        return json.loads(raw_clean)
    except (json.JSONDecodeError, Exception):
        return {"original_text": "", "translated_text": raw}


def AI_translate_text(text: str, target_lang: str) -> str:
    """Uzun matnni tarjima qilish (docx/pdf uchun)."""
    if not text or not text.strip():
        return "Bo'sh matn tarjima qilinmaydi."
    prompt = (
        f"Translate the following text into {target_lang}. "
        f"Preserve the exact meaning, structure, and paragraph layout. "
        f"Return ONLY the translated text — no explanations, no conversational fillers.\n\n"
        f"{NO_MARKDOWN}\n\n"
        f"Text:\n{text}"
    )
    return _call_gemini([prompt])


def AI_assistant(user_message: str, chat_history: list, universities_data: list = None) -> str:
    """
    ScholarMap AI yordamchisi:
    - Foydalanuvchi bilan suhbat olib boradi
    - Profil asosida mos universitetlarni tavsiya qiladi
    - Grantlar haqida savollarga javob beradi
    """
    system_prompt = (
        "Siz ScholarMap platformasining AI yordamchisisiz. "
        "Vazifangiz: talabalar va yoshlarga xorijiy universitetlar va grantlar haqida "
        "aniq, foydali va do'stona maslahat berish. "
        "Har doim O'zbek tilida javob bering (agar foydalanuvchi boshqa tilda so'rasa, "
        "shu tilda javob bering). "
        f"{NO_MARKDOWN}\n\n"
    )

    if universities_data:
        uni_info = "\n".join([
            f"- {u['university_name']} ({u['state']}): "
            f"Grant: {u['grant_name']}, "
            f"Miqdor: {u['grand_amount']}, "
            f"Tur: {u['grand_turi']}, "
            f"Yo'nalish: {u['directions']}, "
            f"Qabul: {u['reception_start']} - {u['reception_end']}"
            for u in universities_data[:50]  # Tezlik uchun 50 ta bilan cheklaymiz
        ])
        system_prompt += (
            f"\n\nMavjud universitetlar va grantlar ro'yxati:\n{uni_info}\n\n"
            "Foydalanuvchi so'rasa, unga mos universitetlarni ro'yxatdan tanlang va tavsiflang."
        )

    # Suhbat tarixi + yangi savol
    history_text = ""
    for msg in chat_history[-10:]:  # oxirgi 10 xabar
        role = "Foydalanuvchi" if msg.get("role") == "user" else "AI"
        history_text += f"{role}: {msg.get('content', '')}\n"

    full_prompt = (
        f"{system_prompt}\n"
        f"Suhbat tarixi:\n{history_text}\n"
        f"Foydalanuvchi: {user_message}\n"
        f"AI:"
    )
    return _call_gemini([full_prompt])


def AI_find_universities(user_profile: dict, universities_data: list) -> str:
    """
    Foydalanuvchi profiliga qarab eng mos universitetlarni topib beradi.
    user_profile: {directions, level, lang, additional_info}
    """
    if not universities_data:
        return "Hozircha tizimda universitetlar mavjud emas."

    uni_list = "\n".join([
        f"{i+1}. {u['university_name']} | {u['state']} | "
        f"Grant: {u['grant_name']} ({u['grand_amount']}) | "
        f"Tur: {u['grand_turi']} | "
        f"Yo'nalish: {u['directions']} | "
        f"Daraja: {u.get('level', 'N/A')} | "
        f"Qabul: {u['reception_start']} - {u['reception_end']}"
        for i, u in enumerate(universities_data[:100])
    ])

    profile_text = "\n".join([f"- {k}: {v}" for k, v in user_profile.items() if v])

    prompt = (
        f"Siz universitetlar bo'yicha ekspertsiz.\n"
        f"Foydalanuvchi profili:\n{profile_text}\n\n"
        f"Mavjud universitetlar:\n{uni_list}\n\n"
        f"Foydalanuvchi profiliga eng mos 5 ta universitetni tanlang. "
        f"Har bir university uchun nima uchun mos ekanini qisqacha tushuntiring. "
        f"O'zbek tilida yozing.\n"
        f"{NO_MARKDOWN}"
    )
    return _call_gemini([prompt])
