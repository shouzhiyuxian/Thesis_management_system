# 毕业论文管理系统

一个基于Flask的毕业论文管理系统，为毕业生和指导教师提供便捷的论文管理平台。

## 功能特性

### 用户角色
- **管理员**：系统管理、用户管理、通知发布、进程控制
- **教师**：发布通知、上传指导资料、批阅学生论文
- **学生**：查看通知、下载资料、上传论文、查看批阅

### 主要功能
1. **用户管理**：支持管理员、教师、学生三种角色的信息管理
2. **通知发布**：管理员和教师可以发布论文相关通知
3. **资料管理**：教师可以上传指导资料，学生可以下载
4. **论文管理**：学生可以上传论文，教师可以批阅
5. **流程控制**：管理员可以控制整个论文流程的进度

## 技术栈

- **后端框架**：Flask 2.0.2
- **数据库**：MySQL
- **ORM**：SQLAlchemy 1.4.25
- **前端框架**：Bootstrap 5
- **Python版本**：3.8

## 安装和运行

### 1. 克隆项目
```bash
git clone <repository-url>
cd Thesis_Management_System
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置数据库
1. 创建MySQL数据库：
```sql
CREATE DATABASE thesis_management;
```

2. 修改 `config.py` 中的数据库连接配置：
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/thesis_management'
```

### 4. 初始化数据库
```bash
flask init-db
```

### 5. 运行应用
```bash
python app.py
```

应用将在 http://localhost:5000 启动

## 默认账号

- **管理员账号**：admin001
- **管理员密码**：admin123

## 项目结构

```
Thesis_Management_System/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用工厂
│   ├── models.py          # 数据库模型
│   ├── auth/              # 认证模块
│   ├── admin/             # 管理员模块
│   ├── teacher/           # 教师模块
│   ├── student/           # 学生模块
│   └── main/              # 主模块
├── templates/             # 模板文件
├── static/                # 静态文件
├── uploads/               # 上传文件目录
├── config.py              # 配置文件
├── app.py                 # 应用入口
└── requirements.txt       # 依赖包列表
```

## 数据库设计

系统包含以下主要数据表：

- `t_student` - 学生信息表
- `t_teacher` - 教师信息表
- `t_admin` - 管理员信息表
- `t_notice` - 通知信息表
- `t_guide` - 指导资料表
- `t_paper` - 论文信息表
- `t_comments` - 批阅信息表
- `t_processstatus` - 流程状态表
- `t_class` - 班级信息表
- `t_grade` - 年级信息表
- `t_nativeplace` - 籍贯信息表

## 使用说明

### 管理员操作
1. 登录系统后进入管理面板
2. 在"用户管理"中添加学生和教师账号
3. 在"通知管理"中发布系统通知
4. 在"进程控制"中管理论文流程进度

### 教师操作
1. 登录系统后进入教师面板
2. 在"通知公告"中发布通知
3. 在"指导资料"中上传相关文档
4. 在"论文批阅"中查看和批阅学生论文

### 学生操作
1. 登录系统后进入学生面板
2. 在"通知公告"中查看最新通知
3. 在"下载资料"中获取指导材料
4. 在"论文管理"中上传论文
5. 在"批阅记录"中查看教师反馈

## 开发说明

### 添加新功能
1. 在对应的模块目录下添加路由
2. 创建相应的模板文件
3. 更新数据库模型（如需要）
4. 运行数据库迁移

### 自定义配置
修改 `config.py` 文件中的配置项：
- 数据库连接
- 文件上传限制
- 分页设置
- 会话配置

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

如有问题，请通过以下方式联系：
- 提交 Issue
- 发送邮件至：[your-email@example.com]
