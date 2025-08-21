import json
import os
import time
from scrapers.ride_distance import get_monthly_total_distance as get_current_mileage
 
DATA_FILE = "data/mileage_data.json"

# 读取持久化数据
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"last_mileage": None, "total_mileage": 0}

# 保存持久化数据
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

import time
from datetime import datetime

def is_within_3_minutes(data,last=180):
    update_time_str = data.get('update_time', '')
    if not update_time_str:
        return False  # 无时间字符串，直接返回False
    
    try:
        # 解析时间字符串为时间元组，再转为datetime对象
        time_tuple = time.strptime(update_time_str, "%Y-%m-%d %H:%M:%S")
        update_time = datetime(*time_tuple[:6])  # 提取年月日时分秒
        
        # 获取当前时间
        current_time = datetime.now()
        
        # 计算时间差（秒）
        time_diff = (current_time - update_time).total_seconds()
        
        # 判断是否在3分钟内（包含3分钟）
        return abs(time_diff) <= last  # 绝对值处理避免时间字符串晚于当前时间的情况
    
    except ValueError:
        # 时间格式解析失败（如字符串不符合"%Y-%m-%d %H:%M:%S"）
        return False

 

# 创建追踪器
def get_mile():
    data = load_data()

    if is_within_3_minutes(data):  
        # 如果今天没有更新过，重置数据
        return data["total_mileage"]
    def tracker():
        nonlocal data
         
        current = get_current_mileage()
        if not current:
        
            return data["total_mileage"]   
        
        if data["last_mileage"] is None:
            data["last_mileage"] = current
            save_data(data)
            return data["total_mileage"]

        if current < data["last_mileage"]:
            # 新统计周期
            data["total_mileage"] += current
        elif current == data["last_mileage"]:
            data["total_mileage"]  = current
        else:
            # 正常累加
            data["total_mileage"] += (current - data["last_mileage"])

        data["last_mileage"] = current
        data['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        save_data(data)
        return data["total_mileage"]

    return tracker()

def check_login():
    r=get_current_mileage()
    if not r:
        return False
    return True
def msg():
    start_distance_km = 153
    psi_start = 50
    psi_after_a = 41
    psi_after_b = 39
    total_ride_distance_km = 220

    mileage_km = get_mile() 
    last_ride_km = mileage_km - start_distance_km
    ride_completion_pct = (last_ride_km / total_ride_distance_km) * 100
    predicted_psi = psi_start - (psi_start - psi_after_b) / total_ride_distance_km * last_ride_km
    a=f'准备维护' if ride_completion_pct > 80 else '放心骑行'
    login=f'在线' if check_login()  else '掉线 last:'+load_data().get('update_time', '未知时间')
    result = (
         f"{a}<br>"
        f"本阶段骑行距离: {last_ride_km:.1f} km\n"
        f"骑行完成百分比: {ride_completion_pct:.1f}%\n"
        f"预测胎压: {predicted_psi:.1f} psi"
        f"<br>累计里程: {mileage_km:.1f} km\n"
        f"登录状态:{login}  \n"
    )

    return result
