#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ニュース要約システムのエントリーポイント"""

from news_summarizer.generators import NewsReportGenerator
from news_summarizer.utils import DEFAULT_TOPICS


def main() -> None:
    """メイン関数"""
    # レポート生成器を初期化
    generator = NewsReportGenerator(DEFAULT_TOPICS)
    
    # 日次レポートを生成
    report = generator.generate_daily_report()
    
    # レポートを保存
    filepath = generator.save_report(report)
    
    print(f"ニュースレポートを生成しました: {filepath}")
    print("レポート内容:")
    print(report)


if __name__ == "__main__":
    main()
