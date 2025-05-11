#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""設定関連のユーティリティモジュール"""

import os
from typing import List
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# デフォルトのトピックリスト
DEFAULT_TOPICS: List[str] = [
    "政治",
    "経済",
    "IT",
    "AI",
    "EdTech",
    "プログラミング",
]

# 環境変数から設定を取得
AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "")

GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")

# 出力ディレクトリ
OUTPUT_DIR: str = "reports" 
