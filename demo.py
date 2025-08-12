#!/usr/bin/env python3
"""
演示脚本 - 展示个人信息源主页功能
"""

import time
from datetime import datetime
from scrapers.news_scraper import news_scraper
from scrapers.tech_scraper import tech_scraper
from scrapers.finance_scraper import finance_scraper
from scrapers.weather_scraper import weather_scraper

def demo_scrapers():
    """演示爬虫功能"""
    print("=" * 60)
    print("个人信息源主页 - 功能演示")
    print("=" * 60)
    
    # 显示当前时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"🕐 当前时间: {current_time}")
    print()
    
    # 演示新闻爬虫
    print("📰 综合新闻:")
    print("-" * 40)
    news_data = news_scraper.get_news()
    if news_data['status'] == 'success' and news_data['data']:
        for i, item in enumerate(news_data['data'][:3], 1):
            print(f"{i}. {item['title']}")
            print(f"   来源: {item['source']} | 链接: {item['link']}")
            print()
    else:
        print("暂无数据")
    print()
    
    # 演示科技新闻爬虫
    print("🔬 科技新闻:")
    print("-" * 40)
    tech_data = tech_scraper.get_tech_news()
    if tech_data['status'] == 'success' and tech_data['data']:
        for i, item in enumerate(tech_data['data'][:3], 1):
            print(f"{i}. {item['title']}")
            print(f"   来源: {item['source']} | 链接: {item['link']}")
            print()
    else:
        print("暂无数据")
    print()
    
    # 演示财经新闻爬虫
    print("💰 财经新闻:")
    print("-" * 40)
    finance_data = finance_scraper.get_finance_news()
    if finance_data['status'] == 'success' and finance_data['data']:
        for i, item in enumerate(finance_data['data'][:3], 1):
            print(f"{i}. {item['title']}")
            print(f"   来源: {item['source']} | 链接: {item['link']}")
            print()
    else:
        print("暂无数据")
    print()
    
    # 演示天气爬虫
    print("🌤️ 天气信息:")
    print("-" * 40)
    weather_data = weather_scraper.get_weather_simple()
    if weather_data['status'] == 'success':
        data = weather_data['data']
        print(f"地点: {data.get('location', 'N/A')}")
        print(f"温度: {data.get('temperature', 'N/A')}°C")
        print(f"天气: {data.get('weather_desc', 'N/A')}")
        print(f"湿度: {data.get('humidity', 'N/A')}%")
        print(f"风速: {data.get('wind_speed', 'N/A')}m/s")
        print(f"风向: {data.get('wind_direction', 'N/A')}")
        print(f"消息: {data.get('message', 'N/A')}")
    else:
        print("暂无数据")
    print()
    
    print("=" * 60)
    print("演示完成！")
    print("要启动完整的Web应用，请运行: python run.py")
    print("然后在浏览器中访问: http://localhost:5000")
    print("=" * 60)

if __name__ == "__main__":
    demo_scrapers()

