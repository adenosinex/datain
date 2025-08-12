from flask import Flask, render_template, jsonify
from flask_cors import CORS
import datetime
import pytz
from scrapers.news_scraper import news_scraper
from scrapers.tech_scraper import tech_scraper
from scrapers.finance_scraper import finance_scraper
from scrapers.weather_scraper import weather_scraper

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/time')
def get_time():
    """获取实时时间"""
    tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.datetime.now(tz)
    return jsonify({
        'time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'timestamp': current_time.timestamp()
    })

@app.route('/api/news')
def get_news():
    """获取新闻数据"""
    try:
        news_data = news_scraper.get_news()
        return jsonify(news_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tech')
def get_tech():
    """获取科技新闻数据"""
    try:
        tech_data = tech_scraper.get_tech_news()
        return jsonify(tech_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/finance')
def get_finance():
    """获取财经数据"""
    try:
        finance_data = finance_scraper.get_finance_news()
        return jsonify(finance_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather')
def get_weather():
    """获取天气数据"""
    try:
        weather_data = weather_scraper.get_weather_simple()
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/<lat>/<lon>')
def get_weather_by_location(lat, lon):
    """根据经纬度获取天气数据"""
    try:
        weather_data = weather_scraper.get_weather_simple(float(lat), float(lon))
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
