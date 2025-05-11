#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""news_summarizer.pyのテスト"""

import unittest
from unittest.mock import patch, MagicMock

from src.news_summarizer.summarizers.news_summarizer import NewsSummarizer
# import src.news_summarizer.utils as utils # 不要になる


class TestNewsSummarizer(unittest.TestCase):
    """NewsSummarizerクラスのテストクラス"""

    @patch('src.news_summarizer.summarizers.news_summarizer.LLMChain')
    @patch('src.news_summarizer.summarizers.news_summarizer.PromptTemplate')
    @patch('src.news_summarizer.summarizers.news_summarizer.AzureChatOpenAI')
    def setUp(self, mock_azure_openai_class, mock_prompt_template_class, mock_llm_chain_class):
        """テスト環境のセットアップ"""
        self.mock_azure_openai_class = mock_azure_openai_class
        self.mock_prompt_template_class = mock_prompt_template_class
        self.mock_llm_chain_class = mock_llm_chain_class
        
        self.mock_llm_instance = MagicMock()
        self.mock_azure_openai_class.return_value = self.mock_llm_instance
        
        self.mock_prompt_instance = MagicMock()
        self.mock_prompt_template_class.return_value = self.mock_prompt_instance
        
        self.mock_chain_instance = MagicMock()
        self.mock_llm_chain_class.return_value = self.mock_chain_instance

        # NewsSummarizerモジュール内の定数を直接パッチ
        self.azure_api_key_patch = patch('src.news_summarizer.summarizers.news_summarizer.AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_API_KEY')
        self.azure_endpoint_patch = patch('src.news_summarizer.summarizers.news_summarizer.AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_ENDPOINT')
        self.azure_deployment_patch = patch('src.news_summarizer.summarizers.news_summarizer.AZURE_OPENAI_DEPLOYMENT_NAME', 'AZURE_OPENAI_DEPLOYMENT_NAME')
        
        self.azure_api_key_patch.start()
        self.azure_endpoint_patch.start()
        self.azure_deployment_patch.start()
        self.addCleanup(self.azure_api_key_patch.stop)
        self.addCleanup(self.azure_endpoint_patch.stop)
        self.addCleanup(self.azure_deployment_patch.stop)

        self.summarizer = NewsSummarizer()

    def test_init(self):
        """初期化が正しく行われることをテスト"""
        self.mock_azure_openai_class.assert_called_once_with(
            api_key="AZURE_OPENAI_API_KEY",
            azure_endpoint="AZURE_OPENAI_ENDPOINT",
            azure_deployment="AZURE_OPENAI_DEPLOYMENT_NAME",
            temperature=0.3
        )
        
        self.mock_prompt_template_class.assert_called_once()
        self.assertEqual(
            self.mock_prompt_template_class.call_args[1]["input_variables"], 
            ["news_data"]
        )
        
        self.mock_llm_chain_class.assert_called_once_with(
            llm=self.mock_llm_instance,
            prompt=self.mock_prompt_instance
        )

    def test_summarize_news(self):
        """summarize_newsメソッドが正しく動作することをテスト"""
        # テストデータ
        news_data = [
            {"title": "テストニュース1", "link": "http://example.com/1", "snippet": "スニペット1"},
            {"title": "テストニュース2", "link": "http://example.com/2", "snippet": "スニペット2"},
        ]
        
        # モックの戻り値を設定
        self.mock_chain_instance.invoke.return_value = {"text": "要約されたテキスト"}
        
        # メソッドを実行
        result = self.summarizer.summarize_news(news_data)
        
        # アサーション
        expected_formatted_news = (
            "タイトル: テストニュース1\n"
            "リンク: http://example.com/1\n"
            "スニペット: スニペット1\n\n"
            "タイトル: テストニュース2\n"
            "リンク: http://example.com/2\n"
            "スニペット: スニペット2"
        )
        
        self.mock_chain_instance.invoke.assert_called_once()
        self.assertEqual(
            self.mock_chain_instance.invoke.call_args[0][0]["news_data"],
            expected_formatted_news
        )
        self.assertEqual(result, "要約されたテキスト")


if __name__ == '__main__':
    unittest.main() 
