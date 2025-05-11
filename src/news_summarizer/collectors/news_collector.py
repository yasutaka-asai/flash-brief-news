#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ニュース収集モジュール"""

import datetime
from typing import List, Dict, Any
from langchain_community.utilities import GoogleSearchAPIWrapper
from news_summarizer.utils import GOOGLE_API_KEY, GOOGLE_CSE_ID


class NewsCollector:
    """Google Search APIを使用してニュースを収集するクラス"""
    
    def __init__(self) -> None:
        """Google Search API Wrapperの初期化"""
        self.search = GoogleSearchAPIWrapper(
            google_api_key=GOOGLE_API_KEY,
            google_cse_id=GOOGLE_CSE_ID
        )
    
    def get_latest_news(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        指定されたクエリで最新ニュースを検索
        
        Args:
            query: 検索クエリ
            num_results: 取得する結果の数
            
        Returns:
            検索結果のリスト
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        search_query = f"{query} {today} ニュース"
        
        results = self.search.results(search_query, num_results)
        return results 
