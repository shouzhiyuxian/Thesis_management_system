#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
毕业论文管理系统启动脚本
"""

import os
from app import create_app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    # 设置环境变量
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    print("=" * 50)
    print("毕业论文管理系统")
    print("=" * 50)
    print("默认管理员账号：admin001")
    print("默认管理员密码：admin123")
    print("=" * 50)
    print("系统启动中...")
    print("访问地址：http://localhost:5000")
    print("=" * 50)
    
    # 启动应用
    app.run(debug=True, host='0.0.0.0', port=5000)
