#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""report_generator.pyのテスト"""

import unittest
import os
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime

from src.news_summarizer.generators.report_generator import NewsReportGenerator


class TestNewsReportGenerator(unittest.TestCase):
    """NewsReportGeneratorクラスのテストクラス"""

    @patch('src.news_summarizer.generators.report_generator.NewsCollector')
    @patch('src.news_summarizer.generators.report_generator.NewsSummarizer')
    def setUp(self, mock_summarizer_class, mock_collector_class):
        """テスト環境のセットアップ"""
        self.mock_collector_class = mock_collector_class
        self.mock_summarizer_class = mock_summarizer_class
        
        self.mock_collector = MagicMock()
        self.mock_summarizer = MagicMock()
        
        mock_collector_class.return_value = self.mock_collector
        mock_summarizer_class.return_value = self.mock_summarizer
        
        self.topics = ["テストトピック1", "テストトピック2"]
        self.generator = NewsReportGenerator(self.topics)

    def test_init(self):
        """初期化が正しく行われることをテスト"""
        self.mock_collector_class.assert_called_once()
        self.mock_summarizer_class.assert_called_once()
        self.assertEqual(self.generator.topics, self.topics)
        self.assertEqual(self.generator.collector, self.mock_collector)
        self.assertEqual(self.generator.summarizer, self.mock_summarizer)

    def test_generate_daily_report(self):
        """generate_daily_reportメソッドが正しく動作することをテスト"""
        # モックの設定
        self.mock_collector.get_latest_news.side_effect = [
            [
                {"title": "ニュース1", "link": "http://example.com/1", "snippet": "スニペット1"},
                {"title": "ニュース2", "link": "http://example.com/2", "snippet": "スニペット2"},
            ],
            [
                {"title": "ニュース3", "link": "http://example.com/3", "snippet": "スニペット3"},
                {"title": "ニュース4", "link": "http://example.com/4", "snippet": "スニペット4"},
                {"title": "ニュース重複", "link": "http://example.com/1", "snippet": "スニペット重複"},
            ],
        ]
        
        self.mock_summarizer.summarize_news.return_value = "要約されたレポート"
        
        # メソッドを実行
        result = self.generator.generate_daily_report(results_per_topic=2)
        
        # アサーション
        # 各トピックでニュース収集メソッドが呼ばれたか確認
        self.assertEqual(self.mock_collector.get_latest_news.call_count, 2)
        self.mock_collector.get_latest_news.assert_any_call("テストトピック1", 2)
        self.mock_collector.get_latest_news.assert_any_call("テストトピック2", 2)
        
        # 要約メソッドが正しい引数で呼ばれたか確認
        self.mock_summarizer.summarize_news.assert_called_once()
        # 重複が除去されていることを確認（URLベース）
        news_arg = self.mock_summarizer.summarize_news.call_args[0][0]
        self.assertEqual(len(news_arg), 4)  # 重複を除いた4件
        
        # 結果の確認
        self.assertEqual(result, "要約されたレポート")

    @patch('src.news_summarizer.generators.report_generator.os.path.exists')
    @patch('src.news_summarizer.generators.report_generator.os.makedirs')
    @patch('src.news_summarizer.generators.report_generator.open', new_callable=mock_open)
    @patch('src.news_summarizer.generators.report_generator.datetime')
    def test_save_report(self, mock_datetime, mock_file_open, mock_makedirs, mock_path_exists):
        """save_reportメソッドが正しく動作することをテスト"""
        # モックの設定
        mock_path_exists.return_value = False
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-05-01"
        mock_datetime.datetime.now.return_value = mock_now
        
        report = "テストレポート内容"
        output_dir = "test_output"
        
        # メソッドを実行
        filepath = self.generator.save_report(report, output_dir)
        
        # アサーション
        mock_path_exists.assert_called_once_with(output_dir)
        mock_makedirs.assert_called_once_with(output_dir)
        mock_datetime.datetime.now.assert_called_once()
        mock_now.strftime.assert_called_once_with("%Y-%m-%d")
        
        expected_filepath = os.path.join(output_dir, "2023-05-01.md")
        self.assertEqual(filepath, expected_filepath)
        
        mock_file_open.assert_called_once_with(expected_filepath, "w", encoding="utf-8")
        mock_file_open().write.assert_called_once_with(report)

    @patch('src.news_summarizer.generators.report_generator.os.path.exists')
    @patch('src.news_summarizer.generators.report_generator.open', new_callable=mock_open)
    @patch('src.news_summarizer.generators.report_generator.datetime')
    def test_save_report_existing_dir(self, mock_datetime, mock_file_open, mock_path_exists):
        """既存ディレクトリにsave_reportメソッドが正しく動作することをテスト"""
        # モックの設定
        mock_path_exists.return_value = True  # ディレクトリが既に存在する場合
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-05-01"
        mock_datetime.datetime.now.return_value = mock_now
        
        report = "テストレポート内容"
        
        # メソッドを実行
        filepath = self.generator.save_report(report)
        
        # アサーション
        mock_path_exists.assert_called_once()
        
        expected_filepath = os.path.join("reports", "2023-05-01.md")
        self.assertEqual(filepath, expected_filepath)
        
        mock_file_open.assert_called_once_with(expected_filepath, "w", encoding="utf-8")
        mock_file_open().write.assert_called_once_with(report)


if __name__ == '__main__':
    unittest.main() 
