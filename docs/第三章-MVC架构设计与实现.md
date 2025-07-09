# 第三章：MVC架构设计与实现

## 3.1 MVC模式理论基础

### 什么是MVC？
MVC（Model-View-Controller）是一种软件架构模式，将应用程序分为三个核心组件：

- **Model（模型）**：负责数据和业务逻辑
- **View（视图）**：负责用户界面和数据展示
- **Controller（控制器）**：负责处理用户输入和协调Model与View

### MVC的优势

#### 1. 分离关注点
```
用户请求 → Controller → Model → Database
    ↑           ↓        ↓
    ←─────── View ←──────┘
```

#### 2. 代码复用性
- Model可以被多个View使用
- View可以展示不同Model的数据
- Controller逻辑可以复用

#### 3. 可维护性
- 修改界面不影响业务逻辑
- 修改数据结构不影响界面
- 各组件独立测试

#### 4. 团队协作
- 前端开发者专注View
- 后端开发者专注Model和Controller
- 并行开发提高效率

### Flask中的MVC实现

| MVC组件 | Flask实现 | 文件位置 |
|---------|-----------|----------|
| Model | SQLAlchemy模型类 | `models/` |
| View | Jinja2模板 | `templates/` |
| Controller | 路由函数和蓝图 | `controllers/` |

## 3.2 项目目录结构设计

### 标准MVC目录结构
```
student_management_system/
├── app.py                    # 应用入口文件
├── config.py                 # 配置文件
├── requirements.txt          # 依赖管理
├── README.md                 # 项目说明
├── models/                   # 模型层（Model）
│   ├── __init__.py
│   └── student.py           # 学生模型
├── controllers/              # 控制器层（Controller）
│   ├── __init__.py
│   └── student_controller.py # 学生控制器
├── templates/                # 视图层（View）
│   ├── base.html            # 基础模板
│   └── students/            # 学生相关模板
│       ├── index.html       # 列表页面
│       ├── add.html         # 添加页面
│       ├── edit.html        # 编辑页面
│       └── view.html        # 详情页面
├── static/                   # 静态资源
│   ├── css/                 # 样式文件
│   ├── js/                  # JavaScript文件
│   └── images/              # 图片资源
├── migrations/               # 数据库迁移文件
└── docs/                     # 文档目录
```

### 目录设计原则

#### 1. 按功能分层
```python
# 好的设计
models/student.py      # 学生数据模型
controllers/student_controller.py  # 学生业务逻辑
templates/students/    # 学生界面模板

# 避免的设计
student_model.py       # 文件名不清晰
student_view.py        # 混合了不同层次
student_everything.py  # 所有功能混在一起
```

#### 2. 模块化组织
```python
# 每个模块都有__init__.py
models/__init__.py
controllers/__init__.py

# 便于导入和管理
from models.student import Student
from controllers.student_controller import student_bp
```

#### 3. 资源分类
```
static/
├── css/
│   ├── bootstrap.min.css    # 第三方CSS
│   └── custom.css           # 自定义样式
├── js/
│   ├── jquery.min.js        # 第三方JS
│   └── app.js               # 应用JS
└── images/
    ├── logo.png
    └── icons/
```

## 3.3 Flask蓝图（Blueprint）详解

### 什么是蓝图？
蓝图是Flask提供的一种组织应用的方式，可以将相关的路由、模板、静态文件组织在一起。

### 蓝图的优势
- **模块化**：将大型应用分解为小模块
- **复用性**：蓝图可以在多个应用中使用
- **团队协作**：不同团队负责不同蓝图
- **URL前缀**：统一管理URL结构

### 创建学生管理蓝图

#### 1. 创建controllers目录和初始化文件
```python
# controllers/__init__.py
# 控制器模块初始化文件
```

#### 2. 创建学生控制器
```python
# controllers/student_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from config import db
from models.student import Student

# 创建蓝图
student_bp = Blueprint('students', __name__, url_prefix='/students')

# 学生列表页面
@student_bp.route('/')
def index():
    """显示学生列表"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Student.query
    
    # 搜索功能
    if search:
        query = query.filter(
            Student.name.contains(search) |
            Student.student_id.contains(search) |
            Student.major.contains(search)
        )
    
    # 分页
    students = query.paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('students/index.html', 
                         students=students, 
                         search=search)

# 添加学生页面
@student_bp.route('/add', methods=['GET', 'POST'])
def add():
    """添加学生"""
    if request.method == 'POST':
        try:
            student = Student(
                student_id=request.form['student_id'],
                name=request.form['name'],
                gender=request.form['gender'],
                age=int(request.form['age']),
                major=request.form['major'],
                grade=request.form['grade'],
                phone=request.form['phone'],
                email=request.form['email'],
                address=request.form['address']
            )
            
            db.session.add(student)
            db.session.commit()
            
            flash('学生添加成功！', 'success')
            return redirect(url_for('students.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}', 'error')
    
    return render_template('students/add.html')

# 查看学生详情
@student_bp.route('/<int:id>')
def view(id):
    """查看学生详情"""
    student = Student.query.get_or_404(id)
    return render_template('students/view.html', student=student)

# 编辑学生信息
@student_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """编辑学生信息"""
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            student.name = request.form['name']
            student.gender = request.form['gender']
            student.age = int(request.form['age'])
            student.major = request.form['major']
            student.grade = request.form['grade']
            student.phone = request.form['phone']
            student.email = request.form['email']
            student.address = request.form['address']
            
            db.session.commit()
            
            flash('学生信息更新成功！', 'success')
            return redirect(url_for('students.view', id=id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'error')
    
    return render_template('students/edit.html', student=student)

# 删除学生
@student_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """删除学生"""
    try:
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '学生删除成功！'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除失败：{str(e)}'
        }), 500
```

### 蓝图注册

在app.py中注册蓝图：
```python
# app.py
from config import app, db
from models.student import Student
from controllers.student_controller import student_bp

# 注册蓝图
app.register_blueprint(student_bp)

# 根路径重定向到学生列表
@app.route('/')
def index():
    return redirect(url_for('students.index'))

# 创建数据库表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```

## 3.4 模型层设计

### 创建Student模型

```python
# models/__init__.py
# 模型模块初始化文件
```

```python
# models/student.py
from config import db
from datetime import datetime

class Student(db.Model):
    """学生模型类"""
    
    # 表名
    __tablename__ = 'students'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    student_id = db.Column(db.String(20), unique=True, nullable=False, comment='学号')
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.String(10), nullable=False, comment='性别')
    age = db.Column(db.Integer, nullable=False, comment='年龄')
    major = db.Column(db.String(100), nullable=False, comment='专业')
    grade = db.Column(db.String(20), nullable=False, comment='年级')
    phone = db.Column(db.String(20), comment='电话号码')
    email = db.Column(db.String(100), comment='邮箱')
    address = db.Column(db.Text, comment='地址')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow, comment='更新时间')
    
    def __init__(self, student_id, name, gender, age, major, grade, 
                 phone=None, email=None, address=None):
        """构造函数"""
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.age = age
        self.major = major
        self.grade = grade
        self.phone = phone
        self.email = email
        self.address = address
    
    def __repr__(self):
        """字符串表示"""
        return f'<Student {self.student_id}: {self.name}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'major': self.major,
            'grade': self.grade,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_student_id(cls, student_id):
        """根据学号查询学生"""
        return cls.query.filter_by(student_id=student_id).first()
    
    @classmethod
    def search(cls, keyword):
        """搜索学生"""
        return cls.query.filter(
            cls.name.contains(keyword) |
            cls.student_id.contains(keyword) |
            cls.major.contains(keyword)
        ).all()
    
    def validate(self):
        """数据验证"""
        errors = []
        
        # 学号验证
        if not self.student_id or len(self.student_id) < 6:
            errors.append('学号不能少于6位')
        
        # 姓名验证
        if not self.name or len(self.name.strip()) < 2:
            errors.append('姓名不能少于2个字符')
        
        # 年龄验证
        if not isinstance(self.age, int) or self.age < 16 or self.age > 100:
            errors.append('年龄必须在16-100之间')
        
        # 邮箱验证（如果提供）
        if self.email and '@' not in self.email:
            errors.append('邮箱格式不正确')
        
        return errors
```

### 模型设计要点

#### 1. 字段类型选择
```python
# 常用字段类型
db.String(length)     # 字符串，指定最大长度
db.Text              # 长文本
db.Integer           # 整数
db.Float             # 浮点数
db.Boolean           # 布尔值
db.DateTime          # 日期时间
db.Date              # 日期
db.Time              # 时间
```

#### 2. 约束条件
```python
# 常用约束
primary_key=True     # 主键
unique=True          # 唯一约束
nullable=False       # 非空约束
default=value        # 默认值
onupdate=func        # 更新时自动调用
```

#### 3. 关系定义
```python
# 一对多关系示例（如果有班级表）
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    students = db.relationship('Student', backref='class_info', lazy=True)

class Student(db.Model):
    # ... 其他字段
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
```

## 3.5 视图层设计

### 模板继承结构

#### 1. 基础模板（base.html）
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}学生管理系统{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- 自定义CSS -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('students.index') }}">
                学生管理系统
            </a>
            
            <div class="navbar-nav">
                <a class="nav-link" href="{{ url_for('students.index') }}">学生列表</a>
                <a class="nav-link" href="{{ url_for('students.add') }}">添加学生</a>
            </div>
        </div>
    </nav>
    
    <!-- 主要内容 -->
    <div class="container mt-4">
        <!-- 消息提示 -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <!-- 页面内容 -->
        {% block content %}{% endblock %}
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- 自定义JS -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### 2. 子模板示例
```html
<!-- templates/students/index.html -->
{% extends "base.html" %}

{% block title %}学生列表 - 学生管理系统{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>学生列表</h2>
    <a href="{{ url_for('students.add') }}" class="btn btn-primary">
        <i class="fas fa-plus"></i> 添加学生
    </a>
</div>

<!-- 搜索表单 -->
<form method="GET" class="mb-4">
    <div class="row">
        <div class="col-md-6">
            <div class="input-group">
                <input type="text" class="form-control" name="search" 
                       value="{{ search }}" placeholder="搜索学号、姓名或专业...">
                <button class="btn btn-outline-secondary" type="submit">
                    <i class="fas fa-search"></i> 搜索
                </button>
            </div>
        </div>
    </div>
</form>

<!-- 学生表格 -->
{% if students.items %}
    <div class="table-responsive">
        <table class="table table-striped table-hover">
            <thead class="table-dark">
                <tr>
                    <th>学号</th>
                    <th>姓名</th>
                    <th>性别</th>
                    <th>年龄</th>
                    <th>专业</th>
                    <th>年级</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                {% for student in students.items %}
                <tr>
                    <td>{{ student.student_id }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.gender }}</td>
                    <td>{{ student.age }}</td>
                    <td>{{ student.major }}</td>
                    <td>{{ student.grade }}</td>
                    <td>
                        <a href="{{ url_for('students.view', id=student.id) }}" 
                           class="btn btn-sm btn-info">查看</a>
                        <a href="{{ url_for('students.edit', id=student.id) }}" 
                           class="btn btn-sm btn-warning">编辑</a>
                        <button class="btn btn-sm btn-danger" 
                                onclick="deleteStudent({{ student.id }}, '{{ student.name|replace("'", "\\'")|replace('"', '\\"') }}')">删除</button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    
    <!-- 分页 -->
    {% if students.pages > 1 %}
        <nav aria-label="分页导航">
            <ul class="pagination justify-content-center">
                {% if students.has_prev %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('students.index', page=students.prev_num, search=search) }}">上一页</a>
                    </li>
                {% endif %}
                
                {% for page_num in students.iter_pages() %}
                    {% if page_num %}
                        {% if page_num != students.page %}
                            <li class="page-item">
                                <a class="page-link" href="{{ url_for('students.index', page=page_num, search=search) }}">{{ page_num }}</a>
                            </li>
                        {% else %}
                            <li class="page-item active">
                                <span class="page-link">{{ page_num }}</span>
                            </li>
                        {% endif %}
                    {% else %}
                        <li class="page-item disabled">
                            <span class="page-link">…</span>
                        </li>
                    {% endif %}
                {% endfor %}
                
                {% if students.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('students.index', page=students.next_num, search=search) }}">下一页</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
    {% endif %}
{% else %}
    <div class="alert alert-info text-center">
        <h4>暂无学生数据</h4>
        <p>点击上方"添加学生"按钮开始添加学生信息。</p>
    </div>
{% endif %}
{% endblock %}

{% block extra_js %}
<script>
function deleteStudent(id, name) {
    if (confirm('确定要删除学生 "' + name + '" 吗？此操作不可恢复！')) {
        fetch('/students/' + id + '/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert('删除失败：' + data.message);
            }
        })
        .catch(error => {
            alert('删除失败：网络错误');
        });
    }
}
</script>
{% endblock %}
```

## 3.6 MVC协作流程

### 请求处理流程
```
1. 用户访问 /students/
2. Flask路由系统匹配到 student_bp.route('/')
3. 调用 controllers/student_controller.py 中的 index() 函数
4. Controller 查询 models/student.py 中的 Student 模型
5. Model 从数据库获取数据并返回给 Controller
6. Controller 将数据传递给 templates/students/index.html 模板
7. View 渲染HTML并返回给用户浏览器
```

### 数据流向图
```
User Request → Controller → Model → Database
     ↑             ↓        ↓
     ←─────── View ←────────┘
```

## 本章小结

在本章中，我们完成了：
- ✅ MVC架构理论学习
- ✅ 项目目录结构设计
- ✅ Flask蓝图的创建和使用
- ✅ 学生模型的完整设计
- ✅ 视图模板的继承结构
- ✅ MVC各层协作机制

## 下一章预告

在第四章中，我们将深入学习数据库操作，包括：
- SQLAlchemy ORM详细用法
- 数据库迁移管理
- CRUD操作的最佳实践
- 数据验证和错误处理
- 查询优化技巧

现在我们已经建立了完整的MVC架构，接下来让我们深入学习如何高效地操作数据库！