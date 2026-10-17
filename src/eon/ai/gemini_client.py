
from dotenv import load_dotenv
from google import genai


class GeminiClient:

    def __init__(self):
        load_dotenv()

        self.client = genai.Client()
        self.model = "gemini-flash-latest"

    def generate_response(self, message: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=message,
        )

        answer = response.text
        if not answer:
            raise RuntimeError("Gemini returned an empty response.")

        return answer.strip()
