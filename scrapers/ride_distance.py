import requests
import json

def get_monthly_total_distance():
    """
    请求iGPSPORT排名接口，获取本月会员总里程数据。
    """
    # 1. 设置请求URL
    url = "https://my.igpsport.com/Ranking/RankingList"
    params = {
        'type': '0'  # 对应URL中的 ?type=0
    }
    cookie=open('data/ride_cookie.txt','r').read().strip()
    # 2. 设置请求头 (Headers)
    # 注意：将您提供的Headers信息复制过来，注意格式
    headers = {
        "authority": "my.igpsport.com",
        "method": "GET",  # 这个通常由requests库自动处理，可以不放在headers里
        "path": "/Ranking/RankingList?type=0", # 这个是浏览器开发者工具中的路径，requests库会根据url和params自动生成，不需放headers
        "scheme": "https", # 同上，由库处理
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": cookie,
        "dnt": "1",
        "priority": "u=1, i",
        "referer": "https://my.igpsport.com/gather/ranking",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

    # 3. 发送GET请求
    # 注意：我们只把真正需要的headers传给requests，method由库决定，path/scheme由url决定
    # 移除 'method', 'path', 'scheme'，因为requests会自动处理
    headers_to_use = {k: v for k, v in headers.items() if k not in ['method', 'path', 'scheme']}

    try:
        response = requests.get(url, params=params, headers=headers_to_use, timeout=10)
        
        # 4. 检查响应状态
        response.raise_for_status()  # 如果状态码不是200，会抛出HTTPError
        
        # 5. 解析JSON响应
        data = response.json()
        
        # 6. 提取 TotalDistance
        # 根据您提供的路径 Data.MonthMemberRankingInfo.TotalDistance
        # 我们需要安全地访问嵌套字典
        total_distance = data.get("Data", {}).get("MonthMemberRankingInfo", {}).get("TotalDistance")
        
        if total_distance is not None:
            print(f"本月会员总里程 (TotalDistance): {total_distance}")
            return total_distance
        else:
            print("未找到 'Data.MonthMemberRankingInfo.TotalDistance' 数据。")
            print("返回的JSON数据结构可能已变更，完整数据如下:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"解析JSON响应失败: {e}")
        print(f"响应内容: {response.text}")
        return None

# --- 主程序 ---
if __name__ == "__main__":
    distance = get_monthly_total_distance()
    if distance is not None:
        print(f"成功获取数据: {distance}")
    else:
        print("获取数据失败。")