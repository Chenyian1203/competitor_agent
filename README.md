# 🌐 跨境电商 AI 智能运营系统 (Enterprise Full-Stack)

## 💡 项目简介
本项目是一个面向跨境电商行业痛点的全栈 AI 应用。通过 FastAPI 后端、SQLite 数据库、Playwright 自动化引擎与 DeepSeek 大模型，实现了“竞品数据清洗 -> 结构化入库 -> RAG 商业分析 -> ECharts 数据可视化”的完整闭环。

## 🏗️ 技术栈
- **后端**：FastAPI + Uvicorn (异步高并发、后台任务)
- **数据库**：SQLAlchemy + SQLite
- **核心引擎**：Playwright (反反爬对抗与解析) + DeepSeek (RAG 商业分析)
- **前端**：HTML/JS + ECharts 数据可视化大屏 + Markdown 实时渲染

## 🌟 核心工程亮点
1. **高可用数据容灾设计**：考虑到电商平台严苛的反爬风控，系统设计了双轨数据接入方案。演示环境采用高保真实时快照，代码内置了完整的代理池与 Playwright 接入逻辑，在生产环境中无缝切换至真实抓取。
2. **大模型深度商业赋能**：通过定制化 Prompt，DeepSeek 不仅能做数据总结，更能输出包含“价格带红海/蓝海分析”、“痛点诊断”、“定价与视觉打法”的运营总监级商业报告。
3. **全栈闭环**：从前端点击，到后台异步处理，再到 SQL 入库与图表渲染，完美打通全栈链路。

## 🚀 快速运行
1. `pip install -r requirements.txt`
2. `cd backend`
3. `uvicorn main:app --reload`
4. 访问 `http://127.0.0.1:8000/`
