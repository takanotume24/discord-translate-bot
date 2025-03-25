import os
from openai import (
    OpenAI,
)

from create_bot import create_bot


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
