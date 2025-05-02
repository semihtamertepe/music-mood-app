import os
from googletrans import Translator
from typing import Optional

translator = Translator()

async def translate_text(text: str) -> str:
    """
    Translate Turkish text to English using Google Translate
    """
    try:
        # Detect if the text is already in English
        detected_lang = translator.detect(text).lang
        if detected_lang == 'en':
            return text

        # Translate from Turkish to English
        translation = translator.translate(text, src='tr', dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        # If translation fails, return the original text
        return text 