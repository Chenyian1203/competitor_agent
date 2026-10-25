# -*- coding: utf-8 -*-
import json
import os

class BrowserAgent:
    def __init__(self):
        pass

    def start(self):
        print("[Browser] 启动真实业务数据快照解析引擎...")

    def fetch_page_text(self, url: str) -> str:
        print(f"[Browser] 正在加载真实业务数据快照...")
        try:
            # 🚨 直接写死绝对路径，绕过所有环境变量和当前工作目录的限制
            file_path = r"B:\期中大作业\competitor_agent\backend\snapshot_data.json"
            
            if not os.path.exists(file_path):
                print(f"[Browser] ❌ 找不到文件: {file_path}")
                return "[]"
                
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
            print(f"[Browser] ✅ 真实数据快照加载成功！")
            return data
        except Exception as e:
            print(f"[Browser] ❌ 读取快照异常: {e}")
            return "[]"

    def stop(self):
        print("[Browser] 解析引擎关闭。")