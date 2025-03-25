import os
from openai import (
    OpenAI,
)
import discord
from discord.ext import commands


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


def create_bot(openai_client: OpenAI) -> commands.Bot:
    """
    Creates and returns a Discord Bot.
    Uses a closure so `openai_client` can be referenced within the bot's events.
    """
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot is ready! Logged in as {bot.user}")

    @bot.event
    async def on_message(message):
        # Ignore messages from the bot itself
        if message.author.bot:
            return

        user_text = message.content.strip()
        if not user_text:
            return

        try:
            # Detect language
            detected_lang = detect_language(openai_client, user_text)
            # Example: if it's English, translate to Japanese
            if detected_lang.lower() == "en":
                translated = translate_text(openai_client, user_text, target_lang="ja")
                response_text = f"Translation result: {translated}"
            else:
                response_text = f"The detected language is {detected_lang}, displaying as is: {user_text}"
            await message.channel.send(response_text)

        except Exception as e:
            # Do not expose detailed info to the user
            print(f"Error: {e}")
            await message.channel.send("An error occurred. Please try again later.")

        # Needed to detect commands (when using commands)
        await bot.process_commands(message)

    return bot


def main() -> None:
    """
    Entry point of the application.
    Retrieves the token and API key from environment variables and starts the bot.
    """
    # ======== Retrieve keys from environment variables ========
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not discord_bot_token or not openai_api_key:
        raise EnvironmentError("Missing DISCORD_BOT_TOKEN or OPENAI_API_KEY")

    # ======== Initialize the OpenAI client ========
    openai_client = OpenAI(api_key=openai_api_key)

    # ======== Create and run the Discord Bot ========
    bot = create_bot(openai_client)
    bot.run(discord_bot_token)


if __name__ == "__main__":
    main()
