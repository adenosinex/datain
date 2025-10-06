


import json
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

import requests
 

# 初始化定时任务调度器
scheduler = BackgroundScheduler()
# 添加定时任务，每天8点14分执行


def send_daily_stats():
    url = "http://localhost:5000/api/daily_stats"
    
    # 请求头
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Microsoft Edge\";v=\"140\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "referrer": "http://localhost:5000/daily_stats"
    }
    
    # 请求体数据
    payload = {
        "project": "downm",
       
        "remark": "auto"
    }
    
    try:
        # 发送POST请求
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),  # 将字典转换为JSON字符串
            timeout=10  # 设置超时时间
        )
        
        # 打印响应信息
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    
def run_auto_request():
    
    scheduler.add_job(
        func=send_daily_stats,
        trigger='cron',
        hour=8,
        minute=15,
        second=0
    )
    # scheduler.add_job(
    #     func=send_daily_stats,
    #     trigger='cron',
    #     hour=9,
    #     minute=42,
    #     second=0
    # )
    print("定时任务已添加，每天8点14分执行 send_daily_stats 函数。")
    # 启动调度器
    scheduler.start()

    # 当应用退出时，关闭调度器
    atexit.register(lambda: scheduler.shutdown())