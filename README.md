# Discord Bot with OpenAI

This repository contains a Discord Bot that automatically detects the language of incoming messages and translates English text to Japanese using the OpenAI API.

## Features

- **Language Detection**  
  Utilizes an OpenAI client to detect the language of each message.
- **Auto-Translation**  
  If the detected language is English (`en`), it automatically translates the text into Japanese.
- **Other Languages**  
  If any other language is detected, the message is simply echoed back.

## Requirements

- **OpenAI API Key**  
  Obtain an API key by creating an [OpenAI account](https://platform.openai.com/) (adjust the URL as necessary).
- **Discord Bot Token**  
  Register an application in the [Discord Developer Portal](https://discord.com/developers/applications), create a bot, and retrieve its token.

## File Structure

```
.
├── Dockerfile          # Docker configuration for building the image
├── mise.toml           # Specifies the Python version
├── requirements.txt    # Lists pinned Python dependencies
└── src
    └── main.py         # Main Discord Bot implementation
```

## Environment Variables

- **`DISCORD_BOT_TOKEN`**  
  The Discord Bot token (required).
- **`OPENAI_API_KEY`**  
  The OpenAI API key (required).

## Usage with Docker

1. **Build the Image**  

   ```bash
   docker build -t discord-bot:latest .
   ```

2. **Run the Container**  

   ```bash
   docker run -it --rm \
     -e DISCORD_BOT_TOKEN="your_discord_bot_token" \
     -e OPENAI_API_KEY="your_openai_api_key" \
     discord-bot:latest
   ```

   - This sets the environment variables for the container.
   - Once started, the bot will connect to Discord.

## Local Usage (Without Docker)

1. **Install Python 3.12**  
   Match the version specified in `mise.toml`.
2. **Install Dependencies**  

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

3. **Set Environment Variables**  

   ```bash
   export DISCORD_BOT_TOKEN="your_discord_bot_token"
   export OPENAI_API_KEY="your_openai_api_key"
   ```

4. **Run the Bot**  

   ```bash
   python src/main.py
   ```

   The bot will attempt to connect to Discord.

## How It Works

- Whenever a user sends a message in a text channel, the bot detects the language.
- If the detected language is English, it translates the message into Japanese and replies with `Translation: ...`.
- If the language is anything else, it replies by echoing the original message along with the detected language code.
- The command prefix is set to `!`, though no specific commands are defined in this sample.
