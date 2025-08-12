#!/usr/bin/env python3
"""
天气API测试脚本
"""

import requests
import json
from scrapers.weather_scraper import weather_scraper

def test_weather_api():
    """测试天气API"""
    print("=" * 50)
    print("天气API测试")
    print("=" * 50)
    
    # 测试天气爬虫
    print("测试天气爬虫...")
    try:
        weather_data = weather_scraper.get_weather_simple()
        print(f"状态: {weather_data.get('status')}")
        print(f"消息: {weather_data.get('message')}")
        
        if weather_data.get('status') == 'success':
            data = weather_data.get('data', {})
            print(f"地点: {data.get('location')}")
            print(f"温度: {data.get('temperature')}")
            print(f"天气: {data.get('weather_desc')}")
            print(f"湿度: {data.get('humidity')}")
            print(f"风速: {data.get('wind_speed')}")
            print(f"风向: {data.get('wind_direction')}")
        else:
            print("天气数据获取失败")
            
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    test_weather_api()
