from openai import (
    OpenAI,
)
import discord
from discord.ext import commands
from translate_text import translate_text
from detect_language import detect_language


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
