# 第二章：Flask基础与项目初始化

## 2.1 Flask框架介绍

### 什么是Flask？
Flask是一个用Python编写的轻量级Web应用框架。它被称为"微框架"，因为它不需要特定的工具或库，但这并不意味着功能有限。Flask的设计哲学是保持核心简单但可扩展。

### Flask的特点
- **轻量级**：核心功能简洁，易于学习
- **灵活性**：可以根据需要添加扩展
- **Pythonic**：遵循Python的设计原则
- **WSGI兼容**：符合Python Web服务器网关接口标准
- **丰富的扩展**：有大量第三方扩展可用

### Flask vs Django
| 特性 | Flask | Django |
|------|-------|--------|
| 学习曲线 | 平缓 | 陡峭 |
| 项目规模 | 小到中型 | 中到大型 |
| 灵活性 | 高 | 中等 |
| 内置功能 | 少 | 多 |
| 开发速度 | 快速原型 | 快速开发 |

## 2.2 创建Flask应用

### 最简单的Flask应用
首先，让我们创建一个最基本的Flask应用来理解其工作原理：

```python
# hello.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

运行这个应用：
```bash
python hello.py
```

访问 `http://localhost:5000`，您将看到 "Hello, World!" 消息。

### Flask应用的核心概念

#### 1. 应用实例
```python
app = Flask(__name__)
```
- `Flask(__name__)` 创建应用实例
- `__name__` 帮助Flask确定资源位置

#### 2. 路由装饰器
```python
@app.route('/')
def hello_world():
    return 'Hello, World!'
```
- `@app.route()` 定义URL路由
- 函数返回值作为HTTP响应

#### 3. 开发服务器
```python
app.run(debug=True)
```
- `debug=True` 启用调试模式
- 代码修改后自动重启
- 显示详细错误信息

## 2.3 配置文件设置

### 为什么需要配置文件？
- **分离关注点**：配置与业务逻辑分离
- **环境适配**：开发、测试、生产环境不同配置
- **安全性**：敏感信息集中管理
- **可维护性**：配置修改不需要改代码

### 创建config.py
```python
# config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# 创建Flask应用实例
app = Flask(__name__)

# 配置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "student_management.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 初始化扩展
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

### 配置项详解

#### 数据库配置
```python
# 数据库URI格式：数据库类型://用户名:密码@主机:端口/数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_management.db'

# 关闭SQLAlchemy的事件系统（提高性能）
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

#### 安全配置
```python
# 用于会话加密和CSRF保护
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

**注意**：在生产环境中，SECRET_KEY应该是一个随机的、难以猜测的字符串。

#### 其他常用配置
```python
# 调试模式
app.config['DEBUG'] = True

# 测试模式
app.config['TESTING'] = False

# JSON配置
app.config['JSON_AS_ASCII'] = False  # 支持中文JSON
```

## 2.4 数据库配置

### SQLite简介
SQLite是一个轻量级的关系型数据库，特点：
- **无服务器**：不需要单独的数据库服务器
- **零配置**：无需安装和配置
- **跨平台**：支持多种操作系统
- **ACID兼容**：支持事务

### SQLAlchemy ORM
ORM（Object-Relational Mapping）对象关系映射，优势：
- **面向对象**：用Python类操作数据库
- **数据库无关**：支持多种数据库
- **安全性**：防止SQL注入
- **维护性**：代码更易读和维护

### Flask-SQLAlchemy扩展
```python
from flask_sqlalchemy import SQLAlchemy

# 初始化数据库
db = SQLAlchemy(app)
```

### 数据库迁移
```python
from flask_migrate import Migrate

# 初始化迁移
migrate = Migrate(app, db)
```

迁移的作用：
- **版本控制**：跟踪数据库结构变化
- **自动化**：自动生成迁移脚本
- **回滚**：支持数据库结构回滚
- **团队协作**：同步数据库结构

## 2.5 项目启动测试

### 创建应用入口文件
```python
# app.py
from config import app, db

# 导入模型（稍后创建）
# from models.student import Student

# 导入控制器（稍后创建）
# from controllers.student_controller import student_bp

# 注册蓝图（稍后添加）
# app.register_blueprint(student_bp)

# 创建数据库表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```

### 测试应用启动
```bash
python app.py
```

您应该看到类似输出：
```
 * Serving Flask app 'config'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://192.168.x.x:8000
```

### 添加测试路由
为了验证应用正常工作，我们可以在config.py中添加一个测试路由：

```python
# 在config.py末尾添加
@app.route('/')
def index():
    return '''
    <h1>学生管理系统</h1>
    <p>Flask应用已成功启动！</p>
    <p>数据库配置完成。</p>
    '''

@app.route('/test')
def test():
    return {
        'message': '测试成功',
        'status': 'ok',
        'database': 'connected'
    }
```

访问 `http://localhost:8000` 和 `http://localhost:8000/test` 测试应用。

## 项目结构检查

此时您的项目结构应该是：
```
student_management_system/
├── app.py                 # ✅ 应用入口
├── config.py             # ✅ 配置文件
├── requirements.txt      # ✅ 依赖列表
├── student_management.db # ✅ 数据库文件（自动生成）
└── docs/                 # ✅ 文档目录
    ├── 教程大纲.md
    ├── 第一章-项目概述与环境准备.md
    └── 第二章-Flask基础与项目初始化.md
```

## 常见问题解决

### Q1: 端口被占用怎么办？
**A:** 修改端口号：
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # 使用8080端口
```

### Q2: 数据库文件在哪里？
**A:** SQLite数据库文件会在项目根目录自动创建，文件名为 `student_management.db`。

### Q3: 如何查看数据库内容？
**A:** 可以使用SQLite浏览器工具，如：
- DB Browser for SQLite（图形界面）
- sqlite3命令行工具
- VS Code的SQLite扩展

### Q4: 调试模式的安全性？
**A:** 调试模式仅用于开发环境，生产环境必须关闭：
```python
app.run(debug=False)  # 生产环境
```

## 最佳实践建议

1. **配置管理**：使用环境变量管理敏感配置
2. **错误处理**：添加适当的异常处理
3. **日志记录**：配置应用日志
4. **代码组织**：保持文件结构清晰
5. **版本控制**：使用Git管理代码

## 本章小结

在本章中，我们完成了：
- ✅ Flask框架基础知识学习
- ✅ 项目配置文件创建
- ✅ 数据库连接配置
- ✅ 应用启动和测试
- ✅ 基础项目结构搭建

## 下一章预告

在第三章中，我们将深入学习MVC架构设计，包括：
- MVC模式的理论基础
- 项目目录结构的详细设计
- Flask蓝图的使用方法
- 模块化开发的最佳实践

现在我们已经有了一个可以运行的Flask应用，接下来让我们按照MVC模式来组织我们的代码！