import os
from openai import OpenAI  # ※独自ラッパ/別実装の可能性あり。要確認
import discord
from discord.ext import commands


def detect_language(openai_client: OpenAI, text: str) -> str:
    """
    OpenAIクライアントを使ってテキストの言語を検出し、
    2文字コード (例: en, ja) を返す関数
    """
    completion = openai_client.responses.create(
        model="gpt-4o",  # 例: ユーザーが利用できるモデル名
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
    OpenAIクライアントを使ってテキストを指定言語に翻訳する関数
    """
    completion = openai_client.responses.create(
        model="gpt-4o",
        instructions="You are a helpful translation assistant.",
        input=(f"Translate the following text to {target_lang}:\n\n{text}"),
    )
    return completion.output_text.strip()


def create_bot(openai_client: OpenAI) -> commands.Bot:
    """
    Discord Bot を生成して返す関数。
    Bot のイベント内で `openai_client` を使えるように、クロージャで参照する。
    """
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot is ready! Logged in as {bot.user}")

    @bot.event
    async def on_message(message):
        # Bot自身の投稿は無視
        if message.author.bot:
            return

        user_text = message.content.strip()
        if not user_text:
            return

        try:
            # 言語検出
            detected_lang = detect_language(openai_client, user_text)
            # 例: 英語なら日本語へ翻訳
            if detected_lang.lower() == "en":
                translated = translate_text(openai_client, user_text, target_lang="ja")
                response_text = f"翻訳結果: {translated}"
            else:
                response_text = (
                    f"言語 {detected_lang} なので、そのまま表示します: {user_text}"
                )
            await message.channel.send(response_text)

        except Exception as e:
            # ユーザーに詳細を出さない
            print(f"Error: {e}")
            await message.channel.send(
                "エラーが発生しました。しばらくしてからお試しください。"
            )

        # commands の検出（コマンド使用時に必要）
        await bot.process_commands(message)

    return bot


def main() -> None:
    """
    全体のエントリーポイント。
    環境変数からトークン・APIキーを取得し、Bot を起動する。
    """
    # ======== 環境変数からキーを読み込む ========
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not discord_bot_token or not openai_api_key:
        raise EnvironmentError("Missing DISCORD_BOT_TOKEN or OPENAI_API_KEY")

    # ======== OpenAIクライアント初期化 ========
    openai_client = OpenAI(api_key=openai_api_key)

    # ======== Discord Bot を生成し、実行 ========
    bot = create_bot(openai_client)
    bot.run(discord_bot_token)


if __name__ == "__main__":
    main()
