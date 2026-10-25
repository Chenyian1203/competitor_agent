# -*- coding: utf-8 -*-
from core.browser_agent import BrowserAgent

def main():
    agent = BrowserAgent()
    # 注意：如果百度有反爬（抓不到结构），就换回 JD
    # agent.auto_search("https://www.baidu.com", "期中大作业")
    agent.auto_search("https://www.baidu.com", "期中大作业")
    print("[完成] 请看屏幕！")

if __name__ == "__main__":
    main()