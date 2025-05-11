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
            各トピックについて、英語と日本語の概要を貼り付けてください。そして、ニュースの内容を要約してください。
            英語の単語は、TOEIC700点以上の水準の場合、単語の説明を日本語で説明してください。
            ニュースの背景や文脈を簡単にまとめてください。なぜ今、これが起こっているのか、という背景情報を知りたいです。
            そのニュースが今後、どのような影響を与えるのか、推察をして考察をしてください。こちらは、500文字くらいで、それなりに充実した内容だと助かります。関連するニュース記事のタイトルとリンクをMarkdown形式で付記してください。
            
            ニュース記事:
            {news_data}
            
            出力形式:
            # 本日のニュース要約（YYYY-MM-DD）
            
            ## トピック1
            ### [記事タイトル1](記事リンク1)
            #### 英語の概要
            #### 日本語の概要
            #### ニュースの内容・背景・影響
            #### 考察
                
            ### [記事タイトル2](記事リンク2)
            #### 英語の概要
            #### 日本語の概要
            #### ニュースの内容・背景・影響
            #### 考察
            
            ## トピック2
            ### [記事タイトル3](記事リンク3)
            #### 英語の概要
            #### 日本語の概要
            #### ニュースの内容・背景・影響
            #### 考察


            ### [記事タイトル4](記事リンク4)
            #### 英語の概要
            #### 日本語の概要
            #### ニュースの内容・背景・影響
            #### 考察
            
            ## その他の注目ニュース
            ### [記事タイトル5](記事リンク5)
            #### 英語の概要
            #### 日本語の概要
            #### ニュースの内容・背景・影響
            #### 考察
            
            ### [記事タイトル6](記事リンク6)
            #### 英語の概要
            #### 日本語の概要
            #### ニュースの内容・背景・影響
            #### 考察
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
        # 各記事のタイトルとリンクをLLMが利用しやすい形式で渡す
        formatted_news = "\n\n".join([
            f"タイトル: {item.get('title', 'タイトルなし')}\n"
            f"リンク: {item.get('link', 'リンクなし')}\n"
            f"スニペット: {item.get('snippet', '内容なし')}"
            for item in news_data
        ])
        
        # 要約を生成
        summary = self.summary_chain.invoke({"news_data": formatted_news})
        return summary["text"] 
