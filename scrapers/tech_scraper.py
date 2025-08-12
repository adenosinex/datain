import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from datetime import datetime

class TechScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def get_tech_news(self):
        """获取科技新闻"""
        try:
            # 使用36氪作为科技新闻源
            url = "https://36kr.com/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tech_list = []
            
            # 获取科技新闻标题和链接
            news_items = soup.find_all('a', href=True)
            
            for item in news_items[:15]:  # 限制数量
                title = item.get_text().strip()
                link = item['href']
                
                if title and len(title) > 5 and 'http' in link:
                    tech_list.append({
                        'title': title,
                        'link': link,
                        'source': '36氪',
                        'category': '科技',
                        'timestamp': datetime.now().isoformat()
                    })
            
            return {
                'status': 'success',
                'data': tech_list,
                'count': len(tech_list)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'data': []
            }

# 创建实例
tech_scraper = TechScraper()

