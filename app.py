import base64
import os
import sqlite3
import threading
import time
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
from scrapers.mipad import run_getpercrnt
from utils.spider import  StealthBrowser
from utils.bookmark_manager import bookmark_manager
from utils.daily_stats import add_record, get_stats,delete_record
from utils.wc_img import factory_wc
from utils.spider import run_spider2
app = Flask(__name__)
CORS(app)

from utils.memorydb import InMemoryURLDB

db_url=InMemoryURLDB(r'utils\urlcontent.db')
wc=factory_wc()
 
# 模拟耗时任务
def long_running_task(task_id):
    print(f"任务 {task_id} 开始执行...")
    # global spider
    # spider = StealthBrowser(headless=True)
    print(f"任务 {task_id} 执行完成")
 
def start_task():
    # 获取任务ID或其他参数
    task_id = 123

    # 🔥 开启新线程执行耗时任务
    thread = threading.Thread(target=long_running_task, args=(task_id,))
    thread.daemon = True  # 主程序退出时，线程也自动退出
    thread.start()
start_task()
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
@app.route('/api/mi')
def get_mi():
    """获取天气数据"""
    try:
        gps_data = {'msg':run_getpercrnt()}
         
        
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

def get_text(  url):
        db_url.delete_url(url)
        db_url.set_url(url)

        now=time.time()
        while time.time()-now<5:
            html=db_url.get_content(url)
            if html:
                return html
            time.sleep(0.5)


@app.route('/api/fetch_html', methods=['POST'])
def fetch_html():
    """根据URL获取HTML源码"""
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': '缺少URL参数'}), 400
        html=run_spider2(url)
        return jsonify({'status': 'success', 'html': html})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
@app.route('/daily_stats')
def daily_stats_page():
    return render_template('daily_stats.html')

@app.route('/api/daily_stats', methods=['GET', 'POST'])
def api_daily_stats():
    if request.method == 'POST':
        data = request.get_json()
        # 后端自动生成北京时间
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.datetime.now(tz)
        time_str = now.strftime('%Y-%m-%d %H:%M:%S')
        add_record(
            data['project'], 
            time_str,
            data.get('remark', ''),
            data.get('count', None)
        )
        return jsonify({'status': 'ok'})
    return jsonify(get_stats())

@app.route('/api/daily_stats/<int:record_id>', methods=['DELETE'])
def delete_daily_record(record_id):
    success = delete_record(record_id)
    return jsonify({'status': 'ok'})

@app.route('/wordcloud')
def wordcloud_page():
    return render_template('wordcloud.html')

@app.route('/api/wordcloud', methods=['POST'])
def api_wordcloud():
    data = request.get_json()
    text = data.get('text', '')
    if not text.strip():
        return jsonify({'error': '内容不能为空'}), 400
    if len(text)<200 and 'http' in text and '.' in text:
        text=run_spider2(text)

    exclude = data.get('exclude', '')
    if not text.strip():
        return jsonify({'error': '内容不能为空'}), 400
    exclude_words = [w.strip() for w in exclude.split(' ') if w.strip()]
  

    file_path,word_count = wc(text,exclude_words)
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return jsonify({'img': encoded_string, 'word_count': word_count})

def main():
    """主函数"""
    print("=" * 50)
    print("个人信息源主页")
    print("=" * 50)
    print("正在启动服务器...")
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = 'development'
    
    # 启动Flask应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )



def back_run():
    # from scrapers.mi_keeplogin import start_refresher
    # start_refresher()
 
    # from utils.spider import start_spider
    # start_spider()
    from utils.auto_request import run_auto_request
    run_auto_request()
    
if __name__ == '__main__':
    back_run()
    main()

