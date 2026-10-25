import subprocess
import time
from openai import OpenAI

client = OpenAI(
    api_key="sk-e220f79fc9e7465983c34cb893df1c07", 
    base_url="https://api.deepseek.com"
)

bsk_path = r"C:\Users\13360\.local\bin\bsk.exe"
session_name = "mytest"

print("⏳ 1. 启动后台...")
subprocess.Popen([bsk_path, "daemon", "start", "--port", "52899"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

print("🌐 2. 创建会话...")
subprocess.run([bsk_path, "session", "start", "--session", session_name], capture_output=True, text=True, encoding='utf-8', errors='ignore')
time.sleep(1)

print("🛒 3. 打开京东并搜索...")
subprocess.run([bsk_path, "navigate", "--session", session_name, "https://search.jd.com/Search?keyword=便携榨汁杯"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
time.sleep(3)

print("📸 4. 抓取页面数据...")
observe_result = subprocess.run([bsk_path, "observe", "--session", session_name], capture_output=True, text=True, encoding='utf-8', errors='ignore')

print("🧠 5. 呼叫 DeepSeek 写报告...")
prompt = f"""
你是一个资深的跨境电商运营专家。
以下是抓取到的京东页面代码：
{observe_result.stdout[:5000]} 

请帮我提取出前 3 款榨汁杯的名称，并写一份简短的《竞品分析及差异化营销建议》。
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}]
)

# 直接打印在终端里！
print("\n" + "="*50)
print("🎉 惊天大战报！DeepSeek 写的报告如下：\n")
print(response.choices[0].message.content)
print("="*50 + "\n")