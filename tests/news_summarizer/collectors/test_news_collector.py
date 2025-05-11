#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""news_collector.pyのテスト"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.news_summarizer.collectors.news_collector import NewsCollector
# import src.news_summarizer.utils as utils # 不要になる


class TestNewsCollector(unittest.TestCase):
    """NewsCollectorクラスのテストクラス"""

    @patch('src.news_summarizer.collectors.news_collector.GoogleSearchAPIWrapper')
    def setUp(self, mock_google_search_class):
        """テスト環境のセットアップ"""
        self.mock_google_search_class = mock_google_search_class
        self.mock_search_instance = MagicMock()
        self.mock_google_search_class.return_value = self.mock_search_instance

        # NewsCollectorモジュール内の定数を直接パッチ
        self.google_api_key_patch = patch('src.news_summarizer.collectors.news_collector.GOOGLE_API_KEY', 'GOOGLE_API_KEY')
        self.google_cse_id_patch = patch('src.news_summarizer.collectors.news_collector.GOOGLE_CSE_ID', 'GOOGLE_CSE_ID')
        
        self.google_api_key_patch.start()
        self.google_cse_id_patch.start()
        self.addCleanup(self.google_api_key_patch.stop)
        self.addCleanup(self.google_cse_id_patch.stop)

        self.collector = NewsCollector()

    def test_init(self):
        """初期化が正しく行われることをテスト"""
        self.mock_google_search_class.assert_called_once_with(
            google_api_key="GOOGLE_API_KEY",
            google_cse_id="GOOGLE_CSE_ID"
        )

    @patch('src.news_summarizer.collectors.news_collector.datetime')
    def test_get_latest_news(self, mock_datetime):
        """get_latest_newsメソッドが正しく動作することをテスト"""
        # モックの設定
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-05-01"
        mock_datetime.datetime.now.return_value = mock_now
        
        expected_results = [
            {"title": "テストニュース1", "link": "http://example.com/1", "snippet": "スニペット1"},
            {"title": "テストニュース2", "link": "http://example.com/2", "snippet": "スニペット2"},
        ]
        self.mock_search_instance.results.return_value = expected_results
        
        # メソッドを実行
        results = self.collector.get_latest_news("テストクエリ", 2)
        
        # アサーション
        mock_datetime.datetime.now.assert_called_once()
        mock_now.strftime.assert_called_once_with("%Y-%m-%d")
        self.mock_search_instance.results.assert_called_once_with("テストクエリ 2023-05-01 ニュース", 2)
        self.assertEqual(results, expected_results)


if __name__ == '__main__':
    unittest.main() 
