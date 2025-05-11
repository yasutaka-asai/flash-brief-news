#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""レポート生成モジュール"""

import os
import datetime
from typing import List
from news_summarizer.collectors import NewsCollector
from news_summarizer.summarizers import NewsSummarizer
from news_summarizer.utils import OUTPUT_DIR


class NewsReportGenerator:
    """ニュースレポートを生成するクラス"""
    
    def __init__(self, topics: List[str]) -> None:
        """
        初期化
        
        Args:
            topics: 収集するニューストピックのリスト
        """
        self.collector = NewsCollector()
        self.summarizer = NewsSummarizer()
        self.topics = topics
    
    def generate_daily_report(self, results_per_topic: int = 5) -> str:
        """
        日次ニュースレポートを生成
        
        Args:
            results_per_topic: トピックごとに収集する記事数
            
        Returns:
            生成されたレポート
        """
        all_news = []
        
        # 各トピックについてニュースを収集
        for topic in self.topics:
            news = self.collector.get_latest_news(topic, results_per_topic)
            all_news.extend(news)
        
        # 重複を除去（URLベース）
        unique_news = {item["link"]: item for item in all_news}.values()
        
        # ニュースを要約
        report = self.summarizer.summarize_news(list(unique_news))
        
        return report
    
    def save_report(self, report: str, output_dir: str = OUTPUT_DIR) -> str:
        """
        レポートをファイルに保存
        
        Args:
            report: 保存するレポート
            output_dir: 出力ディレクトリ
            
        Returns:
            保存したファイルのパス
        """
        # 出力ディレクトリが存在しない場合は作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # ファイル名を生成（YYYY-MM-DD.md）
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}.md"
        filepath = os.path.join(output_dir, filename)
        
        # ファイルに書き込み
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
        
        return filepath 
