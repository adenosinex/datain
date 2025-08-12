import requests
import json
import re
from datetime import datetime
from fake_useragent import UserAgent

class WeatherScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'https://www.weather.com.cn/',
        }

    def send_weather(self, url):
        # 构建天气API URL
        

        response = requests.get(url, headers=self.headers, timeout=10)
        response.encoding = 'utf-8'

        # 解析JSONP响应
        content = response.text
        return content

    def get_weather(self, lat=31.093228072338526, lon=109.91479684164297):
        """获取天气信息"""
        try:
            timestamp = int(datetime.now().timestamp() * 1000)
            url_less = f"https://mpf.weather.com.cn/mpf_v3/webgis/minute?lat={lat}&lon={lon}&callback=fc5m&_={timestamp}"
            content_less = self.send_weather(url_less)
            # 移除JSONP回调函数包装
            json_str2 = re.search(r'fc5m\((.*)\)', content_less)
            
            url_more = f"https://forecast.weather.com.cn/town/api/v1/sk?lat={lat}&lng={lon}&callback=getDataSK&_={timestamp}"
            content = self.send_weather(url_more)
            # 移除JSONP回调函数包装
            json_str = re.search(r'getDataSK\((.*)\)', content)
            
            if json_str:
                weather_data = json.loads(json_str.group(1))
                weather_data_less = json.loads(json_str2.group(1))
                
                # 提取天气信息
                weather_info = {
                    'status': 'success',
                    'data': {
                        'temperature': weather_data.get('temp', {}),
                        'humidity': weather_data.get('humidity', {}),
                        'wind': weather_data.get('Wind', {}),
                        'weather': weather_data.get('weather', {}),
                        'forecast': weather_data_less.get('msg', {}),
                        'timestamp': datetime.now().isoformat()
                    },
                    'message': weather_data.get('msg', '获取天气信息成功')
                }
                
                return weather_info
            else:
                return {
                    'status': 'error',
                    'message': '无法解析天气数据',
                    'data': {}
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'获取天气信息失败: {str(e)}',
                'data': {}
            }
    
    def get_weather_simple(self, lat=31.093228072338526, lon=109.91479684164297):
        """获取简化的天气信息"""
        try:
            weather_data = self.get_weather(lat, lon)
            
            if weather_data['status'] == 'success':
                data = weather_data['data']
                return {
                    'status': 'success',
                    'data': {
                        'location': data.get('location', {}).get('name', '未知地点'),
                        'temperature': data.get('temperature', {}).get('value', 'N/A'),
                        'weather_desc': data.get('weather', {}).get('desc', '未知'),
                        'humidity': data.get('humidity', {}).get('value', 'N/A'),
                        'wind_speed': data.get('wind', {}).get('speed', 'N/A'),
                        'wind_direction': data.get('wind', {}).get('direction', 'N/A'),
                        'message': weather_data.get('message', ''),
                        'timestamp': datetime.now().isoformat()
                    }
                }
            else:
                return weather_data
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'获取天气信息失败: {str(e)}',
                'data': {}
            }

# 创建实例
weather_scraper = WeatherScraper()
