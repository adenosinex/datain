
3. 前端依赖:# 个人信息源主页

使用 Flask + Vue 构建的个人信息源主页项目

## 项目描述

- 标题为实时时间，确保十分准确，对齐时间服务器
- 导航栏收藏各类新闻文章链接，分类展示
- 滑动栏显示每个信息集合，由单独py文件提供爬取的信息

## 项目结构

```
datain/
├── app.py                 # Flask主应用
├── run.py                 # 启动脚本
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── readme.md             # 项目说明
├── scrapers/             # 爬虫模块
│   ├── __init__.py
│   ├── news_scraper.py   # 综合新闻爬虫
│   ├── tech_scraper.py   # 科技新闻爬虫
│   └── finance_scraper.py # 财经新闻爬虫
└── templates/            # 前端模板
    └── index.html        # 主页面
```

## 功能特性

- 🕐 **实时时间显示** - 精确到秒的实时时间显示
- 🌤️ **实时天气信息** - 显示当前地点天气状况
- 📰 **多源新闻聚合** - 综合新闻、科技新闻、财经新闻、体育新闻、娱乐新闻
- 🔖 **书签管理** - 快速访问常用网站
- 🎨 **现代化UI** - 响应式设计，支持移动端
- 🔄 **自动刷新** - 定时自动更新数据
- 📱 **移动端适配** - 完美支持手机和平板设备
- 🚀 **可扩展架构** - 轻松添加新的信息源

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行项目

```bash
# 方式1：直接运行
python run.py

# 方式2：使用Flask命令
python app.py
```

### 3. 访问应用

打开浏览器访问：http://localhost:5000

## API接口

- `GET /api/time` - 获取实时时间
- `GET /api/news` - 获取综合新闻
- `GET /api/tech` - 获取科技新闻
- `GET /api/finance` - 获取财经新闻
- `GET /api/sports` - 获取体育新闻
- `GET /api/entertainment` - 获取娱乐新闻
- `GET /api/weather` - 获取天气信息
- `GET /api/weather/<lat>/<lon>` - 根据经纬度获取天气信息

## 技术栈

### 后端
- **Flask** - Web框架
- **Flask-CORS** - 跨域支持
- **requests** - HTTP请求库
- **BeautifulSoup4** - HTML解析
- **fake-useragent** - 随机User-Agent

### 前端
- **Vue.js 3** - 前端框架
- **Axios** - HTTP客户端
- **CSS3** - 现代化样式
- **响应式设计** - 移动端适配

## 开发说明

### 添加新的新闻源

1. 在 `scrapers/` 目录下创建新的爬虫文件
2. 实现爬虫类和方法
3. 在 `app.py` 中添加对应的API路由
4. 在前端模板中添加新的标签页

### 自定义样式

修改 `templates/index.html` 中的CSS样式部分

## 注意事项

- 请遵守网站的robots.txt规则
- 建议添加适当的请求延迟
- 生产环境请修改SECRET_KEY
- 建议使用代理池避免IP被封

## 许可证

MIT License