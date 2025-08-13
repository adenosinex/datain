
import os
import re


def temp_esp():
    p=r'\\Synology\home\sync od\tempdata\esp'
    files=os.listdir(p)
    files.sort()
    recent_file=files[-1]
    with open(os.path.join(p,recent_file),'r') as f:
        lines=f.readlines()
        for i in lines[::-1]:
            r=re.search(r'(\d{2}\.\d{2})C', i)
            if r:
                rs=r.group(1)
                return rs
        return None
    
import requests
import json
def temp_mi():
        
    # 配置
    HA_URL = "http://192.168.31.82:8123"  # 例如 http://192.168.1.100:8123
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2MGM0MzNhOWQ5NDM0ZmRiOGQ3YTJkMjhhYjZiOGMxNyIsImlhdCI6MTc1NTA5MDM4NCwiZXhwIjoyMDcwNDUwMzg0fQ.iPgWj9Jx3PNIoUKg5KrVOKorz4QH-JNAyoMErvrlWnU"  # 替换为你的实际令牌
    ENTITY_ID = "sensor.miaomiaoc_cn_blt_3_1hc155qh0kc00_t2_temperature_p_2_1"  # 替换为你的温度计实体ID

    # API 端点：获取特定实体的状态
    url = f"{HA_URL}/api/states/{ENTITY_ID}"
    # url = f"{HA_URL}/api/states"

    # 设置请求头
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        data = response.json()
        temperature = data.get('state')  # 获取状态值（即温度）
        unit = data.get('attributes', {}).get('unit_of_measurement')  # 获取单位（通常是 °C）

        if temperature != 'unavailable' and temperature != 'unknown':
            # print(f"温度: {temperature} {unit}")
            return temperature
        else:
            print("无法获取温度数据，状态为:", temperature)

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 解码错误: {e}")

def get_home_temp():
    tmi=temp_mi()
    esp=temp_esp()
    return f'esp传感器： {esp}  米家温度计： {tmi}'
