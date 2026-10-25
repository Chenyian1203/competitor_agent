# -*- coding: utf-8 -*-
import json
import re
from core.logger import get_logger

logger = get_logger("DataProcessor")

class DataProcessor:
    @staticmethod
    def parse_amazon_text(raw_text: str) -> list:
        """将 Playwright 抓取的原始文本，清洗成标准的 JSON 结构"""
        logger.info("开始进行数据清洗与结构化...")
        items = []
        lines = raw_text.split('\n')
        
        for line in lines:
            # 匹配格式: 竞品商品: xxx | 价格: $xxx
            if "竞品商品:" in line and "价格:" in line:
                try:
                    parts = line.split(" | ")
                    title = parts[0].replace("竞品商品: ", "").strip()
                    price_str = parts[1].replace("价格: ", "").strip()
                    
                    # 提取数字
                    price_match = re.search(r'[\d\.]+', price_str)
                    price = float(price_match.group()) if price_match else 0.0
                    
                    items.append({
                        "title": title,
                        "price_usd": price,
                        "raw_price": price_str
                    })
                except Exception as e:
                    logger.warning(f"单行解析失败: {line} | {e}")
                    
        logger.info(f"数据清洗完成，成功提取 {len(items)} 个有效竞品")
        return items

    @staticmethod
    def save_to_json(data: list, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"结构化数据已持久化保存至: {filepath}")