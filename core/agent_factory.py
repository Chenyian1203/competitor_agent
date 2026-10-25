# -*- coding: utf-8 -*-
"""
Agent 工厂：负责双引擎的初始化与自动降级切换
"""
from core.bsk_agent import BskAgent
from core.browser_agent import BrowserAgent
from core.logger import get_logger

logger = get_logger("AgentFactory")

class AgentFactory:
    @staticmethod
    def get_agent(engine_type="auto"):
        """
        获取引擎实例
        :param engine_type: "bsk" (腾讯), "playwright" (微软), "auto" (自动降级)
        """
        if engine_type == "bsk":
            logger.info("启动指定引擎: 腾讯 BrowserSkill")
            return BskAgent()
        elif engine_type == "playwright":
            logger.info("启动指定引擎: Playwright")
            agent = BrowserAgent()
            agent.start()
            return agent
        else:
            # auto 模式：先尝试 bsk，如果挂了自动切 Playwright
            logger.info("Auto 模式：正在探测腾讯 BrowserSkill...")
            try:
                bsk = BskAgent()
                # 试运行一次看是否会报错 (这里只是简单探测)
                # 如果 bsk 会话建立失败，这里会捕获
                if "error" in bsk._run_bsk(["status"]).lower():
                    raise Exception("bsk daemon not running")
                logger.info("✅ 腾讯引擎准备就绪！")
                return bsk
            except Exception as e:
                logger.warning(f"⚠️ 腾讯引擎不可用 ({e})，正在无缝降级至 Playwright 高可用引擎...")
                agent = BrowserAgent()
                agent.start()
                return agent