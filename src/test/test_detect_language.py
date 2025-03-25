import unittest
from unittest.mock import Mock
# from openai import OpenAI  # 公式 openai パッケージに "OpenAI" クラスは実在しないため、使用しないかコメントアウト

from detect_language import detect_language


class TestDetectLanguage(unittest.TestCase):
    def setUp(self):
        # ここでは spec を付けずに Mock() を生成し、自由に属性を生やせるようにする
        self.mock_openai_client = Mock()

        # responses 属性を生やし、その下に create メソッドを用意
        self.mock_openai_client.responses = Mock()
        self.mock_openai_client.responses.create.return_value.output_text = ""

    def test_detect_language_english(self):
        # モックの戻り値を 'en' に設定
        self.mock_openai_client.responses.create.return_value.output_text = "en"
        result = detect_language(self.mock_openai_client, "Hello, how are you?")
        self.assertEqual(result, "en")

    def test_detect_language_french(self):
        self.mock_openai_client.responses.create.return_value.output_text = "fr"
        result = detect_language(self.mock_openai_client, "Bonjour, comment ça va?")
        self.assertEqual(result, "fr")

    def test_detect_language_japanese(self):
        self.mock_openai_client.responses.create.return_value.output_text = "ja"
        result = detect_language(self.mock_openai_client, "こんにちは、お元気ですか？")
        self.assertEqual(result, "ja")

    def test_detect_language_spanish(self):
        self.mock_openai_client.responses.create.return_value.output_text = "es"
        result = detect_language(self.mock_openai_client, "Hola, ¿cómo estás?")
        self.assertEqual(result, "es")

    def test_detect_language_german(self):
        self.mock_openai_client.responses.create.return_value.output_text = "de"
        result = detect_language(self.mock_openai_client, "Hallo, wie geht es dir?")
        self.assertEqual(result, "de")

    def test_detect_language_chinese(self):
        self.mock_openai_client.responses.create.return_value.output_text = "zh"
        result = detect_language(self.mock_openai_client, "你好，你怎么样？")
        self.assertEqual(result, "zh")

    def test_detect_language_korean(self):
        self.mock_openai_client.responses.create.return_value.output_text = "ko"
        result = detect_language(
            self.mock_openai_client, "안녕하세요, 어떻게 지내세요?"
        )
        self.assertEqual(result, "ko")

    def test_detect_language_arabic(self):
        self.mock_openai_client.responses.create.return_value.output_text = "ar"
        result = detect_language(self.mock_openai_client, "مرحباً، كيف حالك؟")
        self.assertEqual(result, "ar")

    def test_detect_language_russian(self):
        self.mock_openai_client.responses.create.return_value.output_text = "ru"
        result = detect_language(self.mock_openai_client, "Привет, как дела?")
        self.assertEqual(result, "ru")

    def test_detect_language_portuguese(self):
        self.mock_openai_client.responses.create.return_value.output_text = "pt"
        result = detect_language(self.mock_openai_client, "Olá, como você está?")
        self.assertEqual(result, "pt")

    def test_detect_language_hindi(self):
        self.mock_openai_client.responses.create.return_value.output_text = "hi"
        result = detect_language(self.mock_openai_client, "नमस्ते, आप कैसे हैं?")
        self.assertEqual(result, "hi")

    def test_detect_language_bengali(self):
        self.mock_openai_client.responses.create.return_value.output_text = "bn"
        result = detect_language(self.mock_openai_client, "হ্যালো, আপনি কেমন আছেন?")
        self.assertEqual(result, "bn")

    def test_detect_language_unknown_code(self):
        # 2文字以外の返り値や想定外の言語コードの場合を想定
        self.mock_openai_client.responses.create.return_value.output_text = "xx"
        result = detect_language(self.mock_openai_client, "Some unknown language text")
        self.assertEqual(result, "xx")

    def test_detect_language_empty_text(self):
        # 返り値を "xx" としているが、どのように処理されるかをテスト
        self.mock_openai_client.responses.create.return_value.output_text = "xx"
        result = detect_language(self.mock_openai_client, "")
        self.assertEqual(result, "xx")

    def test_detect_language_whitespace_text(self):
        # スペースや改行のみの場合を想定
        self.mock_openai_client.responses.create.return_value.output_text = "xx"
        result = detect_language(self.mock_openai_client, "   \n   ")
        self.assertEqual(result, "xx")

    def test_detect_language_special_characters(self):
        # 絵文字や特殊文字だけの場合を想定
        self.mock_openai_client.responses.create.return_value.output_text = "xx"
        text = "😀❤️✨"
        result = detect_language(self.mock_openai_client, text)
        self.assertEqual(result, "xx")

    def test_detect_language_long_text(self):
        # 大量のテキストの場合を想定
        self.mock_openai_client.responses.create.return_value.output_text = "en"
        long_text = "Hello " * 1000  # 非常に長い英語テキスト
        result = detect_language(self.mock_openai_client, long_text)
        self.assertEqual(result, "en")

    def test_detect_language_strips_output(self):
        # 戻り値に空白や改行が含まれている場合でも `.strip()` されることを検証
        self.mock_openai_client.responses.create.return_value.output_text = "  en  \n"
        result = detect_language(self.mock_openai_client, "Hello, how are you?")
        self.assertEqual(result, "en")

    def test_api_call_arguments(self):
        """
        実際に responses.create が正しい引数を用いて呼ばれているかを確認するテスト。
        """
        test_text = "Testing argument passing"
        _ = detect_language(self.mock_openai_client, test_text)
        self.mock_openai_client.responses.create.assert_called_once()

        # 呼び出し時に使われた引数を取り出して検証
        _, kwargs = self.mock_openai_client.responses.create.call_args
        self.assertEqual(kwargs["model"], "gpt-4o")
        self.assertIn("You are a language detection assistant.", kwargs["instructions"])
        self.assertIn("Detect the language of the following text", kwargs["input"])
        self.assertIn(test_text, kwargs["input"])


if __name__ == "__main__":
    unittest.main()
