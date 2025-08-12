#!/usr/bin/env python3
"""
测试脚本 - 验证项目功能
"""

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://localhost:5000"
    
    print("=" * 50)
    print("测试API端点")
    print("=" * 50)
    
    # 测试时间API
    try:
        response = requests.get(f"{base_url}/api/time")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 时间API正常: {data['time']}")
        else:
            print(f"❌ 时间API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 时间API错误: {e}")
    
    # 测试新闻API
    try:
        response = requests.get(f"{base_url}/api/news")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 新闻API正常: 获取到 {data.get('count', 0)} 条新闻")
        else:
            print(f"❌ 新闻API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 新闻API错误: {e}")
    
    # 测试科技API
    try:
        response = requests.get(f"{base_url}/api/tech")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 科技API正常: 获取到 {data.get('count', 0)} 条新闻")
        else:
            print(f"❌ 科技API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 科技API错误: {e}")
    
    # 测试财经API
    try:
        response = requests.get(f"{base_url}/api/finance")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 财经API正常: 获取到 {data.get('count', 0)} 条新闻")
        else:
            print(f"❌ 财经API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 财经API错误: {e}")
    
    # 测试天气API
    try:
        response = requests.get(f"{base_url}/api/weather")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 天气API正常: {data.get('status', 'error')}")
            if data.get('status') == 'success':
                weather_info = data.get('data', {})
                print(f"   地点: {weather_info.get('location', 'N/A')}")
                print(f"   温度: {weather_info.get('temperature', 'N/A')}°C")
        else:
            print(f"❌ 天气API失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 天气API错误: {e}")

def test_scrapers():
    """测试爬虫模块"""
    print("\n" + "=" * 50)
    print("测试爬虫模块")
    print("=" * 50)
    
    try:
        from scrapers.news_scraper import news_scraper
        from scrapers.tech_scraper import tech_scraper
        from scrapers.finance_scraper import finance_scraper
        from scrapers.weather_scraper import weather_scraper
        
        # 测试新闻爬虫
        news_data = news_scraper.get_news()
        print(f"✅ 新闻爬虫: {news_data.get('count', 0)} 条数据")
        
        # 测试科技爬虫
        tech_data = tech_scraper.get_tech_news()
        print(f"✅ 科技爬虫: {tech_data.get('count', 0)} 条数据")
        
        # 测试财经爬虫
        finance_data = finance_scraper.get_finance_news()
        print(f"✅ 财经爬虫: {finance_data.get('count', 0)} 条数据")
        
        # 测试天气爬虫
        weather_data = weather_scraper.get_weather_simple()
        print(f"✅ 天气爬虫: {weather_data.get('status', 'error')}")
        if weather_data.get('status') == 'success':
            print(f"   地点: {weather_data.get('data', {}).get('location', 'N/A')}")
            print(f"   温度: {weather_data.get('data', {}).get('temperature', 'N/A')}°C")
        
    except Exception as e:
        print(f"❌ 爬虫测试失败: {e}")

if __name__ == "__main__":
    print("个人信息源主页 - 功能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试爬虫模块
    test_scrapers()
    
    # 测试API端点（需要先启动服务器）
    print("\n注意: 要测试API端点，请先运行 'python run.py' 启动服务器")
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)
