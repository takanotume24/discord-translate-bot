from openai import (
    OpenAI,
)


def translate_text(openai_client: OpenAI, text: str, target_lang: str) -> str:
    """
    Uses the OpenAI client to translate the given text into the specified language.
    """
    completion = openai_client.responses.create(
        model="gpt-4o",
        instructions="You are a helpful translation assistant.",
        input=(f"Translate the following text to {target_lang}:\n\n{text}"),
    )
    return completion.output_text.strip()
