from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from googletrans import Translator, LANGUAGES

class TranslatorInput(BaseModel):
    text: str = Field(..., description="input text to be translated")
    target_language: str = Field(..., description="Language to be translated to")

class TranslatorTool(StructuredTool):
    name: str = "translator" 
    description: str = "Translates text from English to the target language."
    args_schema: type[TranslatorInput] = TranslatorInput

    def _run(self, text: str, target_language: str):
        # translations = {
        #     "Good Morning": {"German": "Guten Morgen", "French": "Bonjour", "Spanish": "Buenos días"},
        #     "Have a nice day": {"German": "Einen schönen Tag", "French": "Bonne journée", "Spanish": "Que tengas un buen día"},
        #     "Sunshine": {"German": "Sonnenschein", "French": "Rayon de soleil", "Spanish": "Luz del sol"}
        # }
        dest_code = (code for code, name in LANGUAGES.items() if name == target_language.lower())
        # detected_language = Translator.detect(text)
        translator = Translator()
        translation = translator.translate(text, dest="ja")

        return translation
