# mi_cookie_refresher.py
import os
import time
import json
import threading
import requests
from datetime import datetime, timedelta

# ================== 配置区域 ==================
COOKIE_FILE = "data/mi_cookie.txt"
REFRESH_INTERVAL = 300  # 5分钟刷新一次
COOKIE_FILE_MAX_AGE = 310  # 文件超过310秒未更新就触发刷新

# 小米 API 地址（用于刷新 serviceToken）
REFRESH_URL = "https://i.mi.com/status/lite/setting"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://i.mi.com/mobile/find",
    "Origin": "https://i.mi.com",
    "Accept": "application/json",
}

# 初始化会话
session = requests.Session()
session.headers.update(HEADERS)

# 线程控制
refresh_thread = None
stop_event = threading.Event()


def load_cookies():
    """从文件加载 Cookie"""
    if not os.path.exists(COOKIE_FILE):
        print(f"❌ Cookie 文件不存在: {COOKIE_FILE}")
        return None
    
    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        print(f"✅ 成功加载 Cookie: {list(cookies.keys())}")
        return cookies
    except Exception as e:
        print(f"❌ 加载 Cookie 失败: {e}")
        return None

def save_cookies(cookies):
    """保存 Cookie 到文件"""
    try:
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
        print(f"💾 已保存 Cookie 到 {COOKIE_FILE}")
    except Exception as e:
        print(f"❌ 保存 Cookie 失败: {e}")

def is_cookie_expired():
    """检查 Cookie 文件是否过期（超过5分钟未更新）"""
    if not os.path.exists(COOKIE_FILE):
        return True
    
    mtime = os.path.getmtime(COOKIE_FILE)
    elapsed = time.time() - mtime
    return elapsed > COOKIE_FILE_MAX_AGE

def refresh_service_token():
    """向小米服务器发起请求，刷新 serviceToken"""
    print(f"🔄 开始刷新 serviceToken... {datetime.now().strftime('%H:%M:%S')}")

    # 加载当前 Cookie
    cookies = load_cookies()
    if not cookies:
        print("⚠️ 无 Cookie，跳过刷新")
        return False

    # 更新 session 的 cookies
    session.cookies.clear()
    session.cookies.update(cookies)

    # 构造查询参数
    params = {
        "ts": int(time.time() * 1000),
        "type": "AutoRenewal",
        "inactiveTime": "10"
    }

    try:
        r = session.get(REFRESH_URL, params=params, timeout=10)
        
        if r.status_code == 200:
            # ✅ 检查是否返回了新的 Set-Cookie
            if 'serviceToken' in r.cookies:
                print("🔑 检测到新的 serviceToken")
            else:
                print("⚠️ 未收到新的 serviceToken（可能已是最新的）")

            # 更新本地 Cookie
            new_cookies = {k: v for k, v in session.cookies.items()}
            save_cookies(new_cookies)
            return True
        else:
            print(f"❌ 请求失败: {r.status_code} - {r.text[:100]}")
            return False

    except Exception as e:
        print(f"❌ 请求异常: {type(e).__name__}: {e}")
        return False
    

def refresh_loop():
    """后台刷新循环"""
    print("🧵 Cookie 刷新线程已启动")
    while not stop_event.is_set():
        if is_cookie_expired():
            refresh_service_token()
        else:
            print(f"⏳ Cookie 有效，跳过刷新（文件更新于 {int(time.time() - os.path.getmtime(COOKIE_FILE))} 秒前）")
        
        # 等待，但支持提前停止
        for _ in range(10):
            if stop_event.is_set():
                break
            time.sleep(1)  # 分段 sleep，支持快速退出

    print("🧵 Cookie 刷新线程已停止")
    
def start_refresher():
    """启动后台刷新线程"""
    global refresh_thread
    if refresh_thread and refresh_thread.is_alive():
        print("🔄 刷新线程已在运行")
        return

    stop_event.clear()
    refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
    refresh_thread.start()
    print("🚀 已启动 Cookie 自动刷新守护线程")

def stop_refresher():
    """停止刷新线程"""
    stop_event.set()
    if refresh_thread:
        refresh_thread.join(timeout=2)
    print("🛑 已停止 Cookie 刷新线程")

def get_latest_cookies():
    """供主程序调用：获取最新的 Cookie"""
    cookies = load_cookies()
    if cookies:
        print(f"🟢 获取最新 Cookie: powerLevel 查询可用")
    else:
        print("🔴 获取 Cookie 失败")
    return cookies
# ================== 使用示例 ==================
if __name__ == "__main__":
    # 1. 启动后台刷新
    start_refresher()

    # 2. 主程序可以继续做其他事（比如查询设备）
    try:
        while True:
            time.sleep(10)
            # 示例：每 30 秒尝试读取一次 Cookie
            if time.time() % 30 < 1:
                cookies = get_latest_cookies()
                if cookies:
                    print(f"🔋 当前 serviceToken 长度: {len(cookies.get('serviceToken', ''))}")
    except KeyboardInterrupt:
        print("\n👋 正在退出...")
        stop_refresher()