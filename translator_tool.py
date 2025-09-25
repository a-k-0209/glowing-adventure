from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from typing import Literal

class TranslatorInput(BaseModel):
    text: str = Field(..., description="input text to be translated")
    target_language: Literal["German", "French", "Spanish"] = Field(..., description="Language to be translated to")

class TranslatorTool(StructuredTool):
    name: str = "translator" 
    description: str = "Translates text from English to the target language."
    args_schema: type[TranslatorInput] = TranslatorInput

    def _run(self, text: str, target_language: str):
        translations = {
            "Good Morning": {"German": "Guten Morgen", "French": "Bonjour", "Spanish": "Buenos días"},
            "Have a nice day": {"German": "Einen schönen Tag", "French": "Bonne journée", "Spanish": "Que tengas un buen día"},
            "Sunshine": {"German": "Sonnenschein", "French": "Rayon de soleil", "Spanish": "Luz del sol"}
        }

        if text in translations and target_language in translations[text]:
            return translations[text][target_language]
        else:
            return f"Translation not found"
