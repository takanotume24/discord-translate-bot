# ベースイメージ (軽量)
FROM python:3.12-slim

# 作業ディレクトリ作成
WORKDIR /app

# 必要なら OS パッケージを導入 (例として ca-certificates 等)
# 余計なパッケージは追加しないこと
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージのインストール (バージョン固定されたrequirements.txt)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 非rootユーザを追加 (UID 1000, GID 1000は一例)
RUN useradd -u 1000 discordbot

# ソースコードをコピー
COPY src/main.py /app/

# 所有権を変更
RUN chown -R discordbot:discordbot /app

# 実行ユーザ切り替え (最小権限)
USER discordbot

# 起動時コマンド
CMD ["python", "main.py"]
