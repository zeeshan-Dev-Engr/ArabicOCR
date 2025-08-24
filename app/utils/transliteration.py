import os
from typing import Optional


def transliterate_text(text: str) -> str:
    """Transliterate Arabic text to Latin script"""
    if not text:
        return ""
    
    try:
        # Use the arabic_reshaper and python-bidi libraries for proper handling of Arabic text
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        # Reshape the Arabic text
        reshaped_text = arabic_reshaper.reshape(text)
        
        # Handle bidirectional text
        bidi_text = get_display(reshaped_text)
        
        # For actual transliteration, we would use a dedicated library
        # This is a simplified implementation for demonstration purposes
        # In a real application, you might use a more sophisticated transliteration library
        
        # Arabic to Latin character mapping (simplified)
        arabic_to_latin = {
            'ا': 'a', 'أ': 'a', 'إ': 'i', 'آ': 'aa',
            'ب': 'b', 'ت': 't', 'ث': 'th',
            'ج': 'j', 'ح': 'h', 'خ': 'kh',
            'د': 'd', 'ذ': 'dh', 'ر': 'r',
            'ز': 'z', 'س': 's', 'ش': 'sh',
            'ص': 's', 'ض': 'd', 'ط': 't',
            'ظ': 'z', 'ع': '`', 'غ': 'gh',
            'ف': 'f', 'ق': 'q', 'ك': 'k',
            'ل': 'l', 'م': 'm', 'ن': 'n',
            'ه': 'h', 'و': 'w', 'ي': 'y',
            'ة': 'h', 'ى': 'a', 'ء': '\'',
            'ؤ': 'w', 'ئ': 'y',
            # Vowels and diacritics
            'َ': 'a', 'ُ': 'u', 'ِ': 'i',
            'ّ': '', 'ْ': '', 'ٌ': 'un',
            'ٍ': 'in', 'ً': 'an', 'ـ': '',
            # Numbers
            '٠': '0', '١': '1', '٢': '2',
            '٣': '3', '٤': '4', '٥': '5',
            '٦': '6', '٧': '7', '٨': '8',
            '٩': '9',
            # Punctuation and spaces
            ' ': ' ', '،': ',', '؛': ';',
            '؟': '?', '.': '.', '!': '!',
            '(': '(', ')': ')', '\n': '\n',
        }
        
        # Perform character-by-character transliteration
        transliterated = ''
        for char in text:
            transliterated += arabic_to_latin.get(char, char)
        
        return transliterated
    
    except Exception as e:
        error_message = f"Transliteration error: {str(e)}"
        print(error_message)
        return error_message