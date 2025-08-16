from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import datetime
import pytz
from scrapers.news_scraper import news_scraper
from scrapers.tech_scraper import tech_scraper
from scrapers.finance_scraper import finance_scraper
from scrapers.weather_scraper import weather_scraper
from scrapers.local_temp import get_home_temp
from utils.ride import msg
 
from utils.bookmark_manager import bookmark_manager
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
        weather_data_local = get_home_temp()
        weather_data['data']['local_temp'] = weather_data_local
        
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/gps')
def get_gps():
    """获取天气数据"""
    try:
        gps_data = {'msg':msg()}
         
        
        return jsonify({'data':gps_data})
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

# 书签相关API
@app.route('/api/bookmarks')
def get_bookmarks():
    """获取所有书签分类"""
    try:
        categories = bookmark_manager.get_all_categories()
        return jsonify({
            'status': 'success',
            'data': categories
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookmarks/all')
def get_all_bookmarks():
    """获取所有书签（扁平化）"""
    try:
        bookmarks = bookmark_manager.get_all_bookmarks()
        return jsonify({
            'status': 'success',
            'data': bookmarks
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookmarks/search')
def search_bookmarks():
    """搜索书签"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': '搜索关键词不能为空'}), 400
        
        results = bookmark_manager.search_bookmarks(query)
        return jsonify({
            'status': 'success',
            'data': results,
            'query': query
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookmarks/category/<category_id>')
def get_bookmarks_by_category(category_id):
    """根据分类获取书签"""
    try:
        category = bookmark_manager.get_category_by_id(category_id)
        if not category:
            return jsonify({'error': '分类不存在'}), 404
        
        return jsonify({
            'status': 'success',
            'data': category
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookmarks/add', methods=['POST'])
def add_bookmark():
    """添加书签"""
    try:
        data = request.get_json()
        category_id = data.get('category_id')
        bookmark = data.get('bookmark')
        
        if not category_id or not bookmark:
            return jsonify({'error': '缺少必要参数'}), 400
        
        success = bookmark_manager.add_bookmark(category_id, bookmark)
        if success:
            return jsonify({
                'status': 'success',
                'message': '书签添加成功'
            })
        else:
            return jsonify({'error': '添加书签失败'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookmarks/remove', methods=['POST'])
def remove_bookmark():
    """删除书签"""
    try:
        data = request.get_json()
        category_id = data.get('category_id')
        bookmark_title = data.get('bookmark_title')
        
        if not category_id or not bookmark_title:
            return jsonify({'error': '缺少必要参数'}), 400
        
        success = bookmark_manager.remove_bookmark(category_id, bookmark_title)
        if success:
            return jsonify({
                'status': 'success',
                'message': '书签删除成功'
            })
        else:
            return jsonify({'error': '删除书签失败'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
