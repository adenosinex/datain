# 快速启动指南

## 🚀 立即开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 测试功能
```bash
# 运行演示脚本
python demo.py

# 运行测试脚本
python test_app.py
```

### 3. 启动Web应用
```bash
python run.py
```

### 4. 访问应用
打开浏览器访问：http://localhost:5000

## 📋 功能特性

- ✅ 实时时间显示（精确到秒）
- ✅ 综合新闻聚合
- ✅ 科技新闻聚合  
- ✅ 财经新闻聚合
- ✅ 响应式设计
- ✅ 自动数据刷新
- ✅ 现代化UI界面

## 🔧 项目结构

```
datain/
├── app.py                 # Flask主应用
├── run.py                 # 启动脚本
├── demo.py                # 演示脚本
├── test_app.py            # 测试脚本
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── scrapers/             # 爬虫模块
│   ├── news_scraper.py   # 综合新闻爬虫
│   ├── tech_scraper.py   # 科技新闻爬虫
│   └── finance_scraper.py # 财经新闻爬虫
└── templates/            # 前端模板
    └── index.html        # 主页面
```

## 🎯 API接口

- `GET /api/time` - 获取实时时间
- `GET /api/news` - 获取综合新闻
- `GET /api/tech` - 获取科技新闻
- `GET /api/finance` - 获取财经新闻

## 🛠️ 开发说明

### 添加新的新闻源
1. 在 `scrapers/` 目录下创建新的爬虫文件
2. 实现爬虫类和方法
3. 在 `app.py` 中添加对应的API路由
4. 在前端模板中添加新的标签页

### 自定义样式
修改 `templates/index.html` 中的CSS样式部分

## 📱 移动端支持

项目完全支持移动端访问，响应式设计确保在各种设备上都有良好的显示效果。

## 🔍 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **端口被占用**
   ```bash
   # 修改 run.py 中的端口号
   app.run(host='0.0.0.0', port=5001)
   ```

3. **爬虫数据为空**
   - 检查网络连接
   - 确认目标网站可访问
   - 查看控制台错误信息

## 📞 支持

如有问题，请查看：
- `readme.md` - 详细文档
- `test_app.py` - 功能测试
- `demo.py` - 功能演示

---

**享受你的个人信息源主页！** 🎉

