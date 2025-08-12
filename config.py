"""
配置文件
"""

import os

class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # 爬虫配置
    SCRAPER_TIMEOUT = 10
    SCRAPER_MAX_RETRIES = 3
    
    # 新闻源配置
    NEWS_SOURCES = {
        'sina': 'https://news.sina.com.cn/',
        'tech': 'https://36kr.com/',
        'finance': 'https://finance.eastmoney.com/'
    }
    
    # 缓存配置
    CACHE_TIMEOUT = 300  # 5分钟缓存

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SCRAPER_TIMEOUT = 15

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
