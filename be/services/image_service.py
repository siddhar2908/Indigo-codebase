import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_banner_image(prompt):
    if not GEMINI_API_KEY:
        return {
            "error": "GEMINI_API_KEY is missing in .env"
        }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash-image:generateContent?key={GEMINI_API_KEY}"
    )

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return {
            "error": "Image generation failed",
            "status_code": response.status_code,
            "details": response.text
        }

    data = response.json()

    for candidate in data.get("candidates", []):
        content = candidate.get("content", {})
        parts = content.get("parts", [])

        for part in parts:
            inline_data = part.get("inlineData") or part.get("inline_data")

            if inline_data:
                return {
                    "imageBase64": inline_data.get("data"),
                    "mimeType": inline_data.get("mimeType") or inline_data.get("mime_type")
                }

    return {
        "error": "No image returned from Gemini",
        "details": data
    }