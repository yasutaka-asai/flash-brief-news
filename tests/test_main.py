#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main.pyのテスト"""

import unittest
from unittest.mock import patch, MagicMock

from src.main import main


class TestMain(unittest.TestCase):
    """mainモジュールのテストクラス"""

    @patch('src.main.NewsReportGenerator')
    def test_main_function(self, mock_generator_class):
        """main関数が正しく実行されることをテスト"""
        # モックの設定
        mock_generator = MagicMock()
        mock_generator_class.return_value = mock_generator
        mock_generator.generate_daily_report.return_value = "テストレポート"
        mock_generator.save_report.return_value = "/path/to/report.md"

        # 関数を実行
        with patch('builtins.print') as mock_print:
            main()

        # アサーション
        mock_generator_class.assert_called_once()
        mock_generator.generate_daily_report.assert_called_once()
        mock_generator.save_report.assert_called_once_with("テストレポート")
        
        # printが正しく呼ばれたことを確認
        mock_print.assert_any_call("ニュースレポートを生成しました: /path/to/report.md")
        mock_print.assert_any_call("レポート内容:")
        mock_print.assert_any_call("テストレポート")


if __name__ == '__main__':
    unittest.main() 
