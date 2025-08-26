import time
import requests
import json

def run_getpercrnt():
        
    # === 配置 ===
    # 小米查找设备的接口
    url = "https://i.mi.com/find/device/full/status"

    # 请求参数（ts 是时间戳，可以更新）
    params = {
        "ts": str(int(time.time() * 1000))  # 可以用当前时间戳替代，如 str(int(time.time() * 1000))
    }

    # 请求头（Headers）
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "priority": "u=1, i",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referrer": "https://i.mi.com/mobile/find",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
    }

    # === 注意：必须保持登录状态 ===
    # cookies 从浏览器中获取（关键！）
    COOKIE_FILE="data/mi_cookie.txt"
    with open(COOKIE_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    headers["cookie"] = "; ".join([f"{key}={value}" for key, value in cookies.items()])
    # === 发送请求 ===
    session = requests.Session()
    session.headers.update(headers)
    

    try:
        response = session.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        # === 解析数据 ===
        if "data" in data and "devices" in data["data"] and len(data["data"]["devices"]) > 0:
            device = data["data"]["devices"][0]
            last_location = device.get("lastLocationReceipt", {})

            power_level = last_location.get("powerLevel", "未知")
            latitude = last_location.get("latitude", "未知")
            longitude = last_location.get("longitude", "未知")
            timestamp = last_location.get("timestamp", "未知")

            print("✅ 获取成功！")
            print(f"设备名称: {device.get('name', '未知')}")
            key='放心存放' if power_level>30 else '请及时充电'
            s=f"{key} 6spro 电量: {power_level}%"
            print(s)
            print(f"位置: 纬度={latitude}, 经度={longitude}")
            print(f"定位时间: {timestamp}")
            return s
        else:
            print("❌ 未找到设备数据")
            print("返回数据:", json.dumps(data, indent=2, ensure_ascii=False))

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误: {e}")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
    except Exception as e:
        print(f"❌ 解析错误: {e}")
    return "获取失败 mi cookie失效"
 

if __name__ == "__main__":
    run_getpercrnt()