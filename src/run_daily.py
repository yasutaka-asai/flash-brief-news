#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ニュース要約システムのスケジューラ"""

import schedule
import time
from src.main import main as generate_news_report


def job() -> None:
    """毎日実行するジョブ"""
    print("ニュースレポート生成を開始します...")
    generate_news_report()
    print("ニュースレポート生成が完了しました")


def run_scheduler() -> None:
    """スケジューラを実行"""
    # 毎日午前7時に実行するようにスケジュール
    schedule.every().day.at("07:00").do(job)
    
    print("ニュースレポート生成スケジューラを開始しました")
    
    # 起動時に一度実行
    job()
    
    # スケジュールに従って実行
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    run_scheduler() 
