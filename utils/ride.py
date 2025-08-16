import json
import os
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

# 创建追踪器
def get_mile():
    data = load_data()

    def tracker():
        nonlocal data
        current = get_current_mileage()

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
        save_data(data)
        return data["total_mileage"]

    return tracker()

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
    result = (
         f"{a}\n"
        f"累计里程: {mileage_km:.1f} km\n"
        f"本阶段骑行距离: {last_ride_km:.1f} km\n"
        f"骑行完成百分比: {ride_completion_pct:.1f}%\n"
        f"预测胎压: {predicted_psi:.1f} psi"
    )

    return result
