from openai import (
    OpenAI,
)


def detect_language(openai_client: OpenAI, text: str) -> str:
    """
    Uses the OpenAI client to detect the language of the given text,
    and returns a two-letter code (e.g., en, ja).
    """
    completion = openai_client.responses.create(
        model="gpt-4o",
        instructions="You are a language detection assistant.",
        input=(
            "Detect the language of the following text and "
            "respond ONLY with a two-letter code:\n\n"
            f"{text}"
        ),
    )
    return completion.output_text.strip()
