# -*- coding: utf-8 -*-
import os
import argparse
from datetime import datetime
from urllib.parse import quote

from config.settings import PLATFORMS, REPORT_DIR, DATA_DIR
from core.agent_factory import AgentFactory  # 🚨 引入工厂
from core.llm_engine import LLMEngine
from core.data_processor import DataProcessor
from core.logger import get_logger

logger = get_logger("MainPipeline")

def run_pipeline(keyword: str, platform_key: str, engine_type: str):
    logger.info(f"🚀 启动 Agent | 引擎: {engine_type} | 平台: {platform_key} | 关键词: {keyword}")
    
    if platform_key not in PLATFORMS:
        logger.error("不支持的平台！")
        return

    platform_info = PLATFORMS[platform_key]
    target_url = f"{platform_info['url']}{quote(keyword)}"
    
    # 🚨 通过工厂获取引擎
    try:
        agent = AgentFactory.get_agent(engine_type)
    except Exception as e:
        logger.critical(f"双引擎均无法启动: {e}")
        return

    llm = LLMEngine()
    
    try:
        raw_text = agent.fetch_page_text(target_url)
        
        if not raw_text or len(raw_text) < 100:
            logger.error("❌ 抓取失败，页面文本为空。")
            return
            
        # 数据清洗
        structured_data = DataProcessor.parse_amazon_text(raw_text)
        if not structured_data:
            logger.error("未能解析出有效商品，请检查页面结构。")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(DATA_DIR, f"data_{platform_key}_{timestamp}.json")
        DataProcessor.save_to_json(structured_data, json_path)
        
        # AI 分析
        report_md = llm.generate_report(structured_data, platform_info['name'])
        
        # 保存
        file_path = os.path.join(REPORT_DIR, f"report_{platform_key}_{timestamp}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_md)
            
        logger.info(f"✅ 业务全流程闭环完成！报告已保存: {file_path}")
        
    except Exception as e:
        logger.critical(f"Pipeline 崩溃: {e}")
    finally:
        agent.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="跨境电商竞品监控 Agent")
    parser.add_argument("--keyword", type=str, default="portable blender", help="搜索关键词")
    parser.add_argument("--platform", type=str, default="amazon", help="目标平台")
    # 🚨 新增引擎参数
    parser.add_argument("--engine", type=str, default="auto", choices=["auto", "bsk", "playwright"], help="选择驱动引擎")
    args = parser.parse_args()
    
    run_pipeline(args.keyword, args.platform, args.engine)