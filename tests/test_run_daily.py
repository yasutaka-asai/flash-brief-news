#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""run_daily.pyのテスト"""

import unittest
from unittest.mock import patch, MagicMock

from src.run_daily import job, run_scheduler


class TestRunDaily(unittest.TestCase):
    """run_dailyモジュールのテストクラス"""

    @patch('src.run_daily.generate_news_report')
    @patch('builtins.print')
    def test_job(self, mock_print, mock_generate_report):
        """jobが正しく実行されることをテスト"""
        # 関数を実行
        job()

        # アサーション
        mock_generate_report.assert_called_once()
        mock_print.assert_any_call("ニュースレポート生成を開始します...")
        mock_print.assert_any_call("ニュースレポート生成が完了しました")

    @patch('src.run_daily.schedule')
    @patch('src.run_daily.job')
    @patch('src.run_daily.time.sleep', side_effect=InterruptedError)  # 無限ループを回避
    @patch('builtins.print')
    def test_run_scheduler(self, mock_print, mock_sleep, mock_job, mock_schedule):
        """run_schedulerが正しく実行されることをテスト"""
        # モックの設定
        mock_schedule_every = MagicMock()
        mock_schedule_every.day = MagicMock()
        mock_schedule_every.day.at = MagicMock()
        mock_schedule_every.day.at.return_value.do = MagicMock()
        
        mock_schedule.every.return_value = mock_schedule_every
        
        # 関数を実行（InterruptedErrorが発生するが、これはテストの一部）
        with self.assertRaises(InterruptedError):
            run_scheduler()

        # アサーション
        mock_schedule.every.assert_called_once()
        mock_schedule_every.day.at.assert_called_once_with("07:00")
        mock_schedule_every.day.at.return_value.do.assert_called_once_with(mock_job)
        mock_job.assert_called_once()  # 起動時に一度実行されたことを確認
        mock_print.assert_called_with("ニュースレポート生成スケジューラを開始しました")


if __name__ == '__main__':
    unittest.main() 
