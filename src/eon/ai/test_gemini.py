
from eon.ai.gemini_client import GeminiClient


def main():
    try:
        gemini = GeminiClient()
        answer = gemini.generate_response(
            "Reply with exactly: EON Gemini connection successful."
        )
        print("\nGemini response:")
        print(answer)

    except Exception as error:
        print(f"\nGemini test failed: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
