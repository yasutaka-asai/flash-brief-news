#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ニュース要約モジュール"""

from typing import List, Dict, Any
from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from news_summarizer.utils import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT_NAME,
    AZURE_OPENAI_API_VERSION
)


class NewsSummarizer:
    """Azure OpenAIを使用してニュースを要約するクラス"""
    
    def __init__(self) -> None:
        """Azure OpenAI LLMの初期化"""
        self.llm = AzureChatOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=AZURE_OPENAI_API_VERSION,
            temperature=0.3
        )
        
        # 要約用のプロンプトテンプレート
        self.summary_prompt = PromptTemplate(
            input_variables=["news_data"],
            template="""
            以下のニュース記事のリストを分析し、主要なトピックごとに整理して要約してください。
            各トピックについて、重要なポイント、影響、関連する事実を含めてください。
            
            ニュース記事:
            {news_data}
            
            出力形式:
            # 本日のニュース要約（YYYY-MM-DD）
            
            ## トピック1
            - 要点1
            - 要点2
            
            ## トピック2
            - 要点1
            - 要点2
            
            ## その他の注目ニュース
            - ニュース1
            - ニュース2
            """
        )
        
        self.summary_chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)
    
    def summarize_news(self, news_data: List[Dict[str, Any]]) -> str:
        """
        ニュースデータを要約
        
        Args:
            news_data: ニュース記事のリスト
            
        Returns:
            要約されたテキスト
        """
        # ニュースデータを整形
        formatted_news = "\n\n".join([
            f"タイトル: {item.get('title', 'タイトルなし')}\n"
            f"リンク: {item.get('link', 'リンクなし')}\n"
            f"スニペット: {item.get('snippet', '内容なし')}"
            for item in news_data
        ])
        
        # 要約を生成
        summary = self.summary_chain.invoke({"news_data": formatted_news})
        return summary["text"] 
