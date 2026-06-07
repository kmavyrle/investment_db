# pip install openai

from openai import OpenAI
import base64
import mimetypes
from pathlib import Path
BOT_TOKEN = "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"

class mkAI:
    def __init__(self, api_key = BOT_TOKEN):
        self.client = OpenAI(api_key=api_key)

    # -------------------------------------------------
    # 1. GENERAL PROMPT
    # -------------------------------------------------
    def ask(self, prompt: str, model: str = "gpt-4.1-mini"):

        response = self.client.responses.create(
            model=model,
            input=prompt
        )

        return response.output_text

    # -------------------------------------------------
    # 2. GENERAL PROMPT + ATTACHMENT
    # supports images / pdf / txt
    # -------------------------------------------------
    def ask_with_attachment(
        self,
        prompt: str,
        file_path: str,
        model: str = "gpt-4.1-mini"
    ):

        file_path = Path(file_path)

        mime_type, _ = mimetypes.guess_type(file_path)

        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        # IMAGE INPUT
        if mime_type and mime_type.startswith("image"):

            response = self.client.responses.create(
                model=model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {
                                "type": "input_image",
                                "image_url": f"data:{mime_type};base64,{encoded}"
                            }
                        ]
                    }
                ]
            )

        # PDF / OTHER FILE INPUT
        else:

            response = self.client.responses.create(
                model=model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {
                                "type": "input_file",
                                "filename": file_path.name,
                                "file_data": f"data:{mime_type};base64,{encoded}"
                            }
                        ]
                    }
                ]
            )

        return response.output_text

