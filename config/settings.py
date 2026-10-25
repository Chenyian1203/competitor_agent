# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

WORKSPACE = r"B:\期中大作业\competitor_agent"
OUTPUT_DIR = os.path.join(WORKSPACE, "outputs")
REPORT_DIR = os.path.join(OUTPUT_DIR, "reports")
DATA_DIR = os.path.join(OUTPUT_DIR, "data")
KNOWLEDGE_DIR = os.path.join(WORKSPACE, "knowledge")

for d in [REPORT_DIR, DATA_DIR, KNOWLEDGE_DIR]:
    os.makedirs(d, exist_ok=True)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = "deepseek-chat"

# 平台配置映射
PLATFORMS = {
    "amazon": {
        "url": "https://www.amazon.com/s?k=",
        "name": "Amazon"
    },
    "baidu": {  # 🚨 新增百度平台，用于测试腾讯 bsk
        "url": "https://www.baidu.com/s?wd=",
        "name": "Baidu"
    }
}