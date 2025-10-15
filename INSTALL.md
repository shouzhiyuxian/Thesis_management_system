# 安装和运行指南

## 快速开始

### 1. 环境要求
- Python 3.8+
- MySQL 5.7+
- pip

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置数据库
1. 创建MySQL数据库：
```sql
CREATE DATABASE thesis_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改数据库配置（在 `config.py` 中）：
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@localhost/thesis_management'
```

### 4. 初始化数据库
```bash
python init_database.py
```

### 5. 启动系统
```bash
python run.py
```

或者：
```bash
python app.py
```

### 6. 访问系统
打开浏览器访问：http://localhost:5000

## 默认账号

系统初始化后会创建以下默认账号：

| 角色 | 用户名/编号 | 密码 | 说明 |
|------|-------------|------|------|
| 管理员 | admin001 | admin123 | 系统管理员 |
| 教师 | T001 | teacher123 | 示例教师 |
| 学生 | 2020001001 | student123 | 示例学生 |

## 功能测试

运行测试脚本验证系统功能：
```bash
python test_system.py
```

## 常见问题

### 1. 数据库连接失败
- 检查MySQL服务是否启动
- 确认数据库用户名和密码正确
- 确认数据库已创建

### 2. 端口被占用
- 修改 `app.py` 或 `run.py` 中的端口号
- 或者停止占用5000端口的其他程序

### 3. 文件上传失败
- 确认 `static/uploads` 目录存在且有写权限
- 检查文件大小是否超过限制

### 4. 模板文件找不到
- 确认 `templates` 目录结构正确
- 检查模板文件名是否匹配

## 开发模式

启用开发模式（自动重载）：
```bash
export FLASK_ENV=development
python app.py
```

## 生产部署

### 使用Gunicorn（推荐）
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用uWSGI
```bash
pip install uwsgi
uwsgi --http :5000 --module app:app --processes 4 --threads 2
```

## 备份和恢复

### 备份数据库
```bash
mysqldump -u用户名 -p密码 thesis_management > backup.sql
```

### 恢复数据库
```bash
mysql -u用户名 -p密码 thesis_management < backup.sql
```

## 日志配置

在生产环境中，建议配置日志记录：

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/thesis_system.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Thesis Management System startup')
```
