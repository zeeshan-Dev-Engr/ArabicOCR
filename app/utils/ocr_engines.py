import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def process_with_qari(image_path: str) -> str:
    """Process an image with Qari-OCR
    
    Note: This is a placeholder implementation. In a real application,
    you would need to install and import the Qari-OCR library.
    """
    try:
        # This is a placeholder. In a real implementation, you would use the Qari-OCR library
        # For example:
        # from qari_ocr import QariOCR
        # ocr = QariOCR()
        # result = ocr.process_image(image_path)
        # return result.text
        
        # For now, we'll return a placeholder message
        return "[Qari-OCR placeholder: This would contain the actual OCR result from Qari-OCR]\n\nلقد تم استخراج هذا النص باستخدام تقنية التعرف الضوئي على الحروف العربية."
    except Exception as e:
        print(f"Error processing with Qari-OCR: {str(e)}")
        return f"Error processing with Qari-OCR: {str(e)}"


def process_with_mistral(image_path: str) -> str:
    """Process an image with Mistral OCR API"""
    if not MISTRAL_API_KEY:
        return "Error: Mistral API key not found. Please set the MISTRAL_API_KEY environment variable."
    
    try:
        # Read the image file
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        # Prepare the API request
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Convert image to base64 for API request
        import base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        
        # Prepare the payload
        payload = {
            "model": "mistral-large-latest",  # Use appropriate model
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract all Arabic text from this image. Return only the extracted text without any additional comments or explanations."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ]
        }
        
        # Make the API request
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        # Process the response
        if response.status_code == 200:
            result = response.json()
            extracted_text = result["choices"][0]["message"]["content"]
            return extracted_text
        else:
            error_message = f"Mistral API error: {response.status_code} - {response.text}"
            print(error_message)
            return error_message
    
    except Exception as e:
        error_message = f"Error processing with Mistral OCR: {str(e)}"
        print(error_message)
        return error_message