import asyncio
from googletrans import Translator
from rest_framework_simplejwt.utils import aware_utcnow


async def smart_translate(text, target_lang='uz'):
    translator = Translator()

    # Bu yerda await qo'shish shart!
    detection = await translator.detect(text)
    source_lang = detection.lang

    translation = await translator.translate(text, dest=target_lang)

    return {
        "detected_lang": source_lang,
        "translated_text": translation.text
    }



def translate_text(text, target_lang='uz'):
    translate = asyncio.run(smart_translate(text, target_lang))
    return translate

# print(translate_text("Hello, how are you?", 'uz')["translated_text"])
