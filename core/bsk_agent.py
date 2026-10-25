# -*- coding: utf-8 -*-
import subprocess
import time
import uuid
import os

class BskAgent:
    def __init__(self):
        self.bsk = "bsk"
        self.session_id = f"agent_{uuid.uuid4().hex[:6]}"
        self.browser_id = ""
        
        # 🚨 核心修复1：让 Python 在后台静默拉起 daemon，绕过终端 Job Object 限制
        self._ensure_daemon()
        
        self.browser_id = self._detect_browser()
        self._init_session()

    def _ensure_daemon(self):
        """确保后台守护进程存活，如果已死锁，先杀后启"""
        print("[BskAgent] 正在检查并强制唤醒底层 Daemon...")
        try:
            # 清理可能死锁的旧进程
            subprocess.run(["taskkill", "/F", "/IM", "bsk.exe"], capture_output=True, text=True)
            subprocess.run(["taskkill", "/F", "/IM", "bsk-daemon.exe"], capture_output=True, text=True)
            time.sleep(1)
            
            # 使用 Popen 在独立进程中启动，不阻塞主程序
            # 设置 creationflags 确保它脱离当前终端的 Job Object
            subprocess.Popen(
                [self.bsk, "daemon", "start"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            print("[BskAgent] Daemon 启动指令已下发，等待 3 秒...")
            time.sleep(3)
        except Exception as e:
            print(f"[BskAgent] ⚠️ 唤醒 Daemon 异常: {e}")

    def _detect_browser(self) -> str:
        print("[BskAgent] 正在侦测可用浏览器...")
        # 侦测时稍微多给一点超时时间
        res = self._run_bsk(["browsers"], ignore_session=True, timeout=20)
        for line in res.strip().split('\n'):
            if "edge" in line.lower() or "chrome" in line.lower():
                parts = line.split()
                if parts:
                    print(f"[BskAgent] ✅ 锁定浏览器 ID: {parts[0]}")
                    return parts[0]
        return "default"

    def _init_session(self):
        print(f"[BskAgent] 正在申请新会话: {self.session_id}")
        res = self._run_bsk(["session", "start", f"--name={self.session_id}", f"--browser={self.browser_id}"], ignore_session=True)
        if "error" in res.lower():
            print(f"[BskAgent] ❌ 会话创建失败: {res[:100]}")
        else:
            print(f"[BskAgent] ✅ 会话建立成功！")

    def _run_bsk(self, args: list, timeout: int = 15, ignore_session=False) -> str:
        if not ignore_session and "--session" not in args:
            args.extend(["--session", self.session_id])
        cmd = [self.bsk] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return "[BskAgent Error] 执行超时"
        except Exception as e:
            return f"[BskAgent Error] {e}"

    def start(self):
        pass

    def fetch_page_text(self, url: str) -> str:
        print(f"[BskAgent] 尝试导航至: {url}")
        
        # 1. 先尝试官方标准导航
        res = self._run_bsk(["navigate", url])
        print(f"[BskAgent] 官方导航结果: {res[:80]}")
        
        # 2. 如果标准导航被拦截，用 JS 直接改地址（极其管用）
        if "error" in res.lower() or "requested resource" in res.lower():
            print("[BskAgent] ⚠️ 标准导航失败，启用底层 JS 强制跳转...")
            js_nav = f"window.location.href = '{url}';"
            self._run_bsk(["evaluate", js_nav])
            
        print("[BskAgent] 强制等待 4 秒让页面渲染...")
        time.sleep(4)
        
        # 3. 抓取无障碍树快照
        print("[BskAgent] 正在获取页面无障碍树快照...")
        snapshot_data = self._run_bsk(["snapshot"], timeout=20)
        
        if not snapshot_data or len(snapshot_data) < 50:
            print(f"[BskAgent] ❌ 快照获取失败。")
            return ""
            
        return snapshot_data
    
    def stop(self):
        print("[BskAgent] 释放 bsk 资源...")