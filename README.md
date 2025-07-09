# 学生管理系统

基于Flask框架开发的学生管理系统，采用MVC架构模式，使用SQLAlchemy ORM和SQLite本地数据库。

## 功能特性

- ✅ 学生信息的增删改查（CRUD）
- ✅ 学生信息搜索功能
- ✅ 响应式Web界面
- ✅ 数据表单验证
- ✅ 本地SQLite数据库持久化
- ✅ MVC架构设计
- ✅ ORM数据库操作
- ✅ Bootstrap美观界面

## 技术栈

- **后端框架**: Flask 2.3.3
- **数据库ORM**: SQLAlchemy
- **数据库**: SQLite
- **模板引擎**: Jinja2
- **前端框架**: Bootstrap 5
- **图标库**: Bootstrap Icons

## 项目结构

```
Python_TODO/
├── app.py                 # 应用入口文件
├── requirements.txt       # 项目依赖
├── README.md             # 项目说明
├── models/               # 数据模型层
│   ├── __init__.py
│   └── student.py        # 学生模型
├── controllers/          # 控制器层
│   ├── __init__.py
│   └── student_controller.py  # 学生控制器
└── templates/            # 视图模板层
    ├── base.html         # 基础模板
    └── students/         # 学生相关模板
        ├── index.html    # 学生列表
        ├── add.html      # 添加学生
        ├── edit.html     # 编辑学生
        └── view.html     # 学生详情
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问系统

打开浏览器访问：http://localhost:5000/students

## 功能说明

### 学生管理功能

1. **学生列表**: 查看所有学生信息，支持搜索
2. **添加学生**: 添加新的学生信息
3. **编辑学生**: 修改现有学生信息
4. **查看详情**: 查看学生的详细信息
5. **删除学生**: 删除学生记录（需确认）

### 数据字段

- 学号（必填，唯一）
- 姓名（必填）
- 性别（必填）
- 年龄（必填）
- 专业（必填）
- 年级（必填）
- 电话号码（可选）
- 邮箱（可选）
- 地址（可选）

## API接口

系统还提供了RESTful API接口：

- `GET /students/api/list` - 获取所有学生列表
- `GET /students/api/<id>` - 获取指定学生信息

## 数据库

系统使用SQLite数据库，数据库文件为 `student_management.db`，会在首次运行时自动创建。

## 开发说明

### MVC架构

- **Model（模型）**: `models/student.py` - 定义数据结构和数据库操作
- **View（视图）**: `templates/` - 定义用户界面模板
- **Controller（控制器）**: `controllers/student_controller.py` - 处理业务逻辑和路由

### 扩展功能

如需添加新功能，可以：

1. 在 `models/` 中添加新的数据模型
2. 在 `controllers/` 中添加新的控制器
3. 在 `templates/` 中添加新的视图模板
4. 在 `app.py` 中注册新的蓝图

## 注意事项

- 确保Python版本 >= 3.7
- 首次运行会自动创建数据库表
- 学号必须唯一，不可重复
- 删除操作不可撤销，请谨慎操作

## 许可证

本项目仅供学习和参考使用。