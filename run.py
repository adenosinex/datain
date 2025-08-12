#!/usr/bin/env python3
"""
个人信息源主页启动脚本
"""

import os
import sys
from app import app

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

if __name__ == '__main__':
    main()
