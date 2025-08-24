import os
import requests
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_TRANSLATE_API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")

# Translation service to use (openai or google)
TRANSLATION_SERVICE = os.getenv("TRANSLATION_SERVICE", "openai")


def translate_text(text: str, target_language: str = "en") -> str:
    """Translate Arabic text to the target language"""
    if not text:
        return ""
    
    # Choose translation service based on configuration
    if TRANSLATION_SERVICE.lower() == "openai":
        return translate_with_openai(text, target_language)
    else:
        return translate_with_google(text, target_language)


def translate_with_openai(text: str, target_language: str = "en") -> str:
    """Translate text using OpenAI GPT-4o API"""
    if not OPENAI_API_KEY:
        return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    
    try:
        import openai
        
        # Configure OpenAI client
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Get language name from code
        language_names = {
            "en": "English",
            "fr": "French",
            "es": "Spanish",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            # Add more languages as needed
        }
        
        language_name = language_names.get(target_language, "English")
        
        # Create the prompt
        prompt = f"Translate the following Arabic text to {language_name}. Provide only the translation without any additional text or explanations:\n\n{text}"
        
        # Make the API request
        response = client.chat.completions.create(
            model="gpt-4o",  # Use GPT-4o for best translation quality
            messages=[
                {"role": "system", "content": "You are a professional translator specializing in Arabic to other languages."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent translations
            max_tokens=4000
        )
        
        # Extract the translation from the response
        translation = response.choices[0].message.content.strip()
        return translation
    
    except Exception as e:
        error_message = f"OpenAI translation error: {str(e)}"
        print(error_message)
        return error_message


def translate_with_google(text: str, target_language: str = "en") -> str:
    """Translate text using Google Translate API via translators library"""
    try:
        # Using the translators library which doesn't require an API key for basic usage
        import translators as ts
        
        # Map language codes if needed
        language_map = {
            "zh": "zh-CN",  # Chinese (Simplified)
            "zh-TW": "zh-TW",  # Chinese (Traditional)
            # Add more mappings as needed
        }
        
        # Get the mapped language code or use the original
        target_lang = language_map.get(target_language, target_language)
        
        # Translate using Google Translate
        translation = ts.google(text, from_language='ar', to_language=target_lang)
        
        return translation
    
    except Exception as e:
        error_message = f"Google translation error: {str(e)}"
        print(error_message)
        return error_message