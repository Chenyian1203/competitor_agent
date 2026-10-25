# -*- coding: utf-8 -*-
import json
import uuid
import sys
import os
from urllib.parse import quote
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, Product, Report
from core.browser_agent import BrowserAgent
from core.llm_engine import LLMEngine
from core.logger import get_logger

logger = get_logger("API_Server")

SQLALCHEMY_DATABASE_URL = "sqlite:///./competitor.db" 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine) 

app = FastAPI(title="跨境电商 AI 运营系统 API")

@app.get("/")
def read_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

class TaskRequest(BaseModel):
    keyword: str

def run_agent_pipeline(trace_id: str, keyword: str):
    logger.info(f"[{trace_id}] 🚀 后台任务启动: 真实抓取 eBay 关键词 '{keyword}'")
    db = SessionLocal()
    agent = BrowserAgent()
    llm = LLMEngine()
    
    try:
        agent.start()
        
        # 🚨 使用 eBay 的搜索链接（国内可直接访问）
                # 🚨 拼装京东移动端真实搜索链接
                # 🚨 拼装闲鱼的真实搜索 API 链接
                # 🚨 拼装 eBay 的真实 PC 搜索链接
        safe_keyword = quote(keyword)
        url = f"https://thor.weidian.com/?keyword={keyword}"
        raw_text = agent.fetch_page_text(url)
        
        try:
            items = json.loads(raw_text)
        except:
            items = []

        # 🚨 纯真实抓取，抓不到绝不造假
        if not items or len(items) == 0:
            logger.error(f"[{trace_id}] ❌ 抓取失败：eBay 返回了空数据。")
            return

        logger.info(f"[{trace_id}] 💾 正在保存 {len(items)} 条真实数据入库...")
        for item in items:
            db.add(Product(
                title=item.get('title'),
                price=item.get('price', 0.0),
                img_url="", 
                brand=item.get('brand', 'eBay'),
                rating=float(item.get('rating', 0)) if item.get('rating') else 0.0,
                platform="eBay",
                trace_id=trace_id
            ))
            
        logger.info(f"[{trace_id}] 🧠 正在呼叫 DeepSeek 生成商业战略报告...")
        report_text = llm.generate_report(items, "eBay")
        db.add(Report(trace_id=trace_id, content=report_text))
        
        db.commit()
        logger.info(f"[{trace_id}] ✅ 完美！真实业务全流程闭环完成！")

    except Exception as e:
        logger.error(f"[{trace_id}] ❌ 崩溃: {e}")
        db.rollback()
    finally:
        agent.stop()
        db.close()

@app.post("/api/scrape")
def trigger_scrape(request: TaskRequest, background_tasks: BackgroundTasks):
    trace_id = str(uuid.uuid4())[:8]
    background_tasks.add_task(run_agent_pipeline, trace_id, request.keyword)
    return {"status": "success", "trace_id": trace_id, "message": "任务已下发"}

@app.get("/api/products")
def get_products():
    db = SessionLocal()
    try:
        data = db.query(Product).all()
        return {"count": len(data), "data": data}
    finally:
        db.close()

@app.get("/api/reports")
def get_reports():
    db = SessionLocal()
    try:
        data = db.query(Report).all()
        return {"count": len(data), "data": data}
    finally:
        db.close()