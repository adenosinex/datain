import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from datetime import datetime

class FinanceScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def get_finance_news(self):
        """获取财经新闻"""
        try:
            # 使用东方财富网作为财经新闻源
            url = "https://finance.eastmoney.com/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            finance_list = []
            
            # 获取财经新闻标题和链接
            news_items = soup.find_all('a', href=True)
            
            for item in news_items[:15]:  # 限制数量
                title = item.get_text().strip()
                link = item['href']
                
                if title and len(title) > 5 and 'http' in link:
                    finance_list.append({
                        'title': title,
                        'link': link,
                        'source': '东方财富',
                        'category': '财经',
                        'timestamp': datetime.now().isoformat()
                    })
            
            return {
                'status': 'success',
                'data': finance_list,
                'count': len(finance_list)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'data': []
            }

# 创建实例
finance_scraper = FinanceScraper()

