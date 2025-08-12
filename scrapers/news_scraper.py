import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from datetime import datetime

class NewsScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def get_news(self):
        """获取综合新闻"""
        try:
            # 这里使用新浪新闻作为示例
            url = "https://news.sina.com.cn/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_list = []
            
            # 获取新闻标题和链接
            news_items = soup.find_all('a', href=True)
            
            for item in news_items[:20]:  # 限制数量
                title = item.get_text().strip()
                link = item['href']
                
                if title and len(title) > 5 and 'http' in link:
                    news_list.append({
                        'title': title,
                        'link': link,
                        'source': '新浪新闻',
                        'timestamp': datetime.now().isoformat()
                    })
            
            return {
                'status': 'success',
                'data': news_list,
                'count': len(news_list)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'data': []
            }

# 创建实例
news_scraper = NewsScraper()

