# 第四章：数据库操作与ORM实践

## 4.1 SQLAlchemy ORM深入理解

### ORM概念回顾
ORM（Object-Relational Mapping）对象关系映射是一种编程技术，用于在不兼容的类型系统间转换数据。在Python中，SQLAlchemy是最流行的ORM框架。

### SQLAlchemy架构
```
Application Code
       ↓
SQLAlchemy ORM
       ↓
SQLAlchemy Core
       ↓
Database API (DBAPI)
       ↓
Database
```

### 核心组件

#### 1. 声明式基类
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 所有模型都继承自 db.Model
class Student(db.Model):
    pass
```

#### 2. 会话管理
```python
# Flask-SQLAlchemy 自动管理会话
db.session.add(student)     # 添加到会话
db.session.commit()         # 提交事务
db.session.rollback()       # 回滚事务
db.session.delete(student)  # 删除对象
```

#### 3. 查询接口
```python
# 基本查询
Student.query.all()                    # 查询所有
Student.query.get(1)                   # 根据主键查询
Student.query.filter_by(name='张三')    # 简单条件查询
Student.query.filter(Student.age > 18) # 复杂条件查询
```

## 4.2 数据库迁移管理

### Flask-Migrate简介
Flask-Migrate是基于Alembic的Flask扩展，用于处理SQLAlchemy数据库迁移。

### 迁移的重要性
- **版本控制**：跟踪数据库结构变化
- **团队协作**：同步数据库结构
- **部署安全**：渐进式数据库更新
- **回滚能力**：支持数据库结构回滚

### 迁移命令详解

#### 1. 初始化迁移仓库
```bash
# 首次使用时执行
flask db init
```

这会创建 `migrations/` 目录：
```
migrations/
├── alembic.ini          # Alembic配置文件
├── env.py              # 迁移环境配置
├── script.py.mako      # 迁移脚本模板
└── versions/           # 迁移版本文件夹
```

#### 2. 生成迁移脚本
```bash
# 检测模型变化并生成迁移脚本
flask db migrate -m "Initial migration"
```

#### 3. 应用迁移
```bash
# 将迁移应用到数据库
flask db upgrade
```

#### 4. 回滚迁移
```bash
# 回滚到上一个版本
flask db downgrade

# 回滚到指定版本
flask db downgrade <revision_id>
```

#### 5. 查看迁移历史
```bash
# 查看当前版本
flask db current

# 查看迁移历史
flask db history
```

### 配置Flask-Migrate

在项目中添加迁移支持：
```python
# config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "student_management.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 初始化扩展
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

### 迁移最佳实践

#### 1. 迁移脚本审查
```python
# 生成的迁移脚本示例
"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # 升级操作
    op.create_table('students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        # ... 其他字段
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id')
    )

def downgrade():
    # 降级操作
    op.drop_table('students')
```

#### 2. 数据迁移
```python
# 包含数据操作的迁移
def upgrade():
    # 结构变更
    op.add_column('students', sa.Column('status', sa.String(20), nullable=True))
    
    # 数据迁移
    connection = op.get_bind()
    connection.execute(
        "UPDATE students SET status = 'active' WHERE status IS NULL"
    )
    
    # 设置非空约束
    op.alter_column('students', 'status', nullable=False)
```

## 4.3 CRUD操作详解

### Create（创建）操作

#### 1. 基本创建
```python
# 方式一：构造函数创建
student = Student(
    student_id='2024001',
    name='张三',
    gender='男',
    age=20,
    major='计算机科学',
    grade='2024级'
)

db.session.add(student)
db.session.commit()
```

#### 2. 批量创建
```python
# 批量添加学生
students = [
    Student(student_id='2024001', name='张三', gender='男', age=20, major='计算机科学', grade='2024级'),
    Student(student_id='2024002', name='李四', gender='女', age=19, major='软件工程', grade='2024级'),
    Student(student_id='2024003', name='王五', gender='男', age=21, major='数据科学', grade='2023级')
]

db.session.add_all(students)
db.session.commit()
```

#### 3. 创建时的错误处理
```python
def create_student(student_data):
    """安全创建学生记录"""
    try:
        # 检查学号是否已存在
        existing = Student.query.filter_by(student_id=student_data['student_id']).first()
        if existing:
            return {'success': False, 'message': '学号已存在'}
        
        # 创建新学生
        student = Student(**student_data)
        
        # 数据验证
        errors = student.validate()
        if errors:
            return {'success': False, 'message': '; '.join(errors)}
        
        db.session.add(student)
        db.session.commit()
        
        return {'success': True, 'student': student, 'message': '学生创建成功'}
        
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'创建失败：{str(e)}'}
```

### Read（读取）操作

#### 1. 基本查询
```python
# 查询所有学生
all_students = Student.query.all()

# 根据主键查询
student = Student.query.get(1)
student = Student.query.get_or_404(1)  # 找不到时返回404

# 查询第一个匹配的记录
first_student = Student.query.first()

# 根据条件查询第一个
student = Student.query.filter_by(student_id='2024001').first()
```

#### 2. 条件查询
```python
# 简单条件查询
male_students = Student.query.filter_by(gender='男').all()

# 复杂条件查询
from sqlalchemy import and_, or_

# 年龄大于18的男学生
adult_male = Student.query.filter(
    and_(Student.age > 18, Student.gender == '男')
).all()

# 计算机或软件工程专业
cs_students = Student.query.filter(
    or_(Student.major == '计算机科学', Student.major == '软件工程')
).all()

# 模糊查询
name_like = Student.query.filter(Student.name.like('%张%')).all()
name_contains = Student.query.filter(Student.name.contains('张')).all()

# 范围查询
age_range = Student.query.filter(Student.age.between(18, 25)).all()

# 列表查询
majors = ['计算机科学', '软件工程', '数据科学']
cs_majors = Student.query.filter(Student.major.in_(majors)).all()
```

#### 3. 排序和分页
```python
# 排序
students_by_age = Student.query.order_by(Student.age.desc()).all()
students_by_name = Student.query.order_by(Student.name.asc()).all()

# 多字段排序
students_sorted = Student.query.order_by(
    Student.grade.desc(), 
    Student.age.asc()
).all()

# 分页
page = 1
per_page = 10
students_page = Student.query.paginate(
    page=page, 
    per_page=per_page, 
    error_out=False
)

# 分页对象属性
print(f"总记录数：{students_page.total}")
print(f"总页数：{students_page.pages}")
print(f"当前页：{students_page.page}")
print(f"是否有下一页：{students_page.has_next}")
print(f"是否有上一页：{students_page.has_prev}")
```

#### 4. 聚合查询
```python
from sqlalchemy import func

# 统计总数
total_count = Student.query.count()

# 按专业统计人数
major_counts = db.session.query(
    Student.major, 
    func.count(Student.id).label('count')
).group_by(Student.major).all()

# 平均年龄
average_age = db.session.query(func.avg(Student.age)).scalar()

# 最大最小年龄
max_age = db.session.query(func.max(Student.age)).scalar()
min_age = db.session.query(func.min(Student.age)).scalar()
```

### Update（更新）操作

#### 1. 单记录更新
```python
# 查询并更新
student = Student.query.get(1)
if student:
    student.age = 21
    student.phone = '13800138000'
    db.session.commit()
```

#### 2. 批量更新
```python
# 批量更新年级
Student.query.filter_by(grade='2023级').update({
    'grade': '2024级'
})
db.session.commit()

# 条件批量更新
Student.query.filter(Student.age < 18).update({
    'age': 18
})
db.session.commit()
```

#### 3. 安全更新函数
```python
def update_student(student_id, update_data):
    """安全更新学生信息"""
    try:
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return {'success': False, 'message': '学生不存在'}
        
        # 更新字段
        for key, value in update_data.items():
            if hasattr(student, key) and key != 'id' and key != 'student_id':
                setattr(student, key, value)
        
        # 数据验证
        errors = student.validate()
        if errors:
            return {'success': False, 'message': '; '.join(errors)}
        
        db.session.commit()
        return {'success': True, 'student': student, 'message': '更新成功'}
        
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'更新失败：{str(e)}'}
```

### Delete（删除）操作

#### 1. 单记录删除
```python
# 查询并删除
student = Student.query.get(1)
if student:
    db.session.delete(student)
    db.session.commit()
```

#### 2. 批量删除
```python
# 删除所有2020级学生
Student.query.filter_by(grade='2020级').delete()
db.session.commit()

# 条件删除
Student.query.filter(Student.age > 30).delete()
db.session.commit()
```

#### 3. 软删除实现
```python
# 在模型中添加软删除字段
class Student(db.Model):
    # ... 其他字段
    is_deleted = db.Column(db.Boolean, default=False, comment='是否删除')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def soft_delete(self):
        """软删除"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        db.session.commit()
    
    @classmethod
    def active_query(cls):
        """只查询未删除的记录"""
        return cls.query.filter_by(is_deleted=False)
```

## 4.4 数据验证与错误处理

### 模型级验证

#### 1. 字段验证
```python
class Student(db.Model):
    # ... 字段定义
    
    def validate(self):
        """数据验证"""
        errors = []
        
        # 学号验证
        if not self.student_id:
            errors.append('学号不能为空')
        elif len(self.student_id) < 6:
            errors.append('学号不能少于6位')
        elif not self.student_id.isalnum():
            errors.append('学号只能包含字母和数字')
        
        # 姓名验证
        if not self.name or not self.name.strip():
            errors.append('姓名不能为空')
        elif len(self.name.strip()) < 2:
            errors.append('姓名不能少于2个字符')
        elif len(self.name.strip()) > 50:
            errors.append('姓名不能超过50个字符')
        
        # 性别验证
        if self.gender not in ['男', '女', '其他']:
            errors.append('性别必须是：男、女、其他')
        
        # 年龄验证
        if not isinstance(self.age, int):
            errors.append('年龄必须是整数')
        elif self.age < 16 or self.age > 100:
            errors.append('年龄必须在16-100之间')
        
        # 邮箱验证
        if self.email:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                errors.append('邮箱格式不正确')
        
        # 电话验证
        if self.phone:
            phone_pattern = r'^1[3-9]\d{9}$'
            if not re.match(phone_pattern, self.phone):
                errors.append('手机号格式不正确')
        
        return errors
    
    def validate_unique(self):
        """唯一性验证"""
        errors = []
        
        # 检查学号唯一性
        existing = Student.query.filter(
            Student.student_id == self.student_id,
            Student.id != self.id  # 排除自己
        ).first()
        
        if existing:
            errors.append('学号已存在')
        
        return errors
```

#### 2. 业务逻辑验证
```python
class Student(db.Model):
    # ... 其他方法
    
    def validate_business_rules(self):
        """业务规则验证"""
        errors = []
        
        # 年级与年龄的合理性检查
        current_year = datetime.now().year
        grade_year = int(self.grade.replace('级', ''))
        expected_age_min = current_year - grade_year + 17
        expected_age_max = current_year - grade_year + 25
        
        if not (expected_age_min <= self.age <= expected_age_max):
            errors.append(f'年龄与年级不匹配，{self.grade}学生年龄应在{expected_age_min}-{expected_age_max}岁之间')
        
        # 专业与年级的匹配检查
        valid_majors = {
            '2024级': ['计算机科学', '软件工程', '数据科学', '人工智能'],
            '2023级': ['计算机科学', '软件工程', '数据科学'],
            '2022级': ['计算机科学', '软件工程'],
            '2021级': ['计算机科学', '软件工程']
        }
        
        if self.grade in valid_majors and self.major not in valid_majors[self.grade]:
            errors.append(f'{self.grade}不支持{self.major}专业')
        
        return errors
```

### 控制器级验证

```python
# controllers/student_controller.py
from flask import request, flash, jsonify

def validate_student_form(form_data):
    """表单数据验证"""
    errors = []
    
    # 必填字段检查
    required_fields = ['student_id', 'name', 'gender', 'age', 'major', 'grade']
    for field in required_fields:
        if not form_data.get(field, '').strip():
            errors.append(f'{field}不能为空')
    
    # 数据类型检查
    try:
        age = int(form_data.get('age', 0))
        if age <= 0:
            errors.append('年龄必须是正整数')
    except ValueError:
        errors.append('年龄必须是数字')
    
    return errors

@student_bp.route('/add', methods=['GET', 'POST'])
def add():
    """添加学生"""
    if request.method == 'POST':
        # 表单验证
        form_errors = validate_student_form(request.form)
        if form_errors:
            for error in form_errors:
                flash(error, 'error')
            return render_template('students/add.html')
        
        try:
            # 创建学生对象
            student = Student(
                student_id=request.form['student_id'].strip(),
                name=request.form['name'].strip(),
                gender=request.form['gender'],
                age=int(request.form['age']),
                major=request.form['major'].strip(),
                grade=request.form['grade'].strip(),
                phone=request.form.get('phone', '').strip() or None,
                email=request.form.get('email', '').strip() or None,
                address=request.form.get('address', '').strip() or None
            )
            
            # 模型验证
            validation_errors = student.validate()
            unique_errors = student.validate_unique()
            business_errors = student.validate_business_rules()
            
            all_errors = validation_errors + unique_errors + business_errors
            
            if all_errors:
                for error in all_errors:
                    flash(error, 'error')
                return render_template('students/add.html')
            
            # 保存到数据库
            db.session.add(student)
            db.session.commit()
            
            flash('学生添加成功！', 'success')
            return redirect(url_for('students.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'添加失败：{str(e)}', 'error')
            return render_template('students/add.html')
    
    return render_template('students/add.html')
```

### 异常处理最佳实践

#### 1. 数据库异常处理
```python
from sqlalchemy.exc import IntegrityError, DataError

def safe_database_operation(operation_func, *args, **kwargs):
    """安全的数据库操作包装器"""
    try:
        result = operation_func(*args, **kwargs)
        db.session.commit()
        return {'success': True, 'data': result}
        
    except IntegrityError as e:
        db.session.rollback()
        if 'UNIQUE constraint failed' in str(e):
            return {'success': False, 'message': '数据已存在，请检查唯一字段'}
        else:
            return {'success': False, 'message': '数据完整性错误'}
            
    except DataError as e:
        db.session.rollback()
        return {'success': False, 'message': '数据格式错误'}
        
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'操作失败：{str(e)}'}
```

#### 2. API错误响应
```python
@student_bp.errorhandler(404)
def not_found(error):
    """404错误处理"""
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'message': '资源不存在',
            'error_code': 404
        }), 404
    else:
        return render_template('errors/404.html'), 404

@student_bp.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({
            'success': False,
            'message': '服务器内部错误',
            'error_code': 500
        }), 500
    else:
        return render_template('errors/500.html'), 500
```

## 4.5 查询优化技巧

### 1. 索引优化
```python
class Student(db.Model):
    # ... 字段定义
    
    # 添加索引
    __table_args__ = (
        db.Index('idx_student_id', 'student_id'),
        db.Index('idx_name', 'name'),
        db.Index('idx_major_grade', 'major', 'grade'),
    )
```

### 2. 查询优化
```python
# 避免N+1查询问题
# 不好的做法
students = Student.query.all()
for student in students:
    print(student.class_info.name)  # 每次都查询数据库

# 好的做法
from sqlalchemy.orm import joinedload
students = Student.query.options(joinedload(Student.class_info)).all()
for student in students:
    print(student.class_info.name)  # 一次查询获取所有数据
```

### 3. 分页优化
```python
def get_students_page(page=1, per_page=10, search=None):
    """优化的分页查询"""
    query = Student.query
    
    # 搜索条件
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Student.name.like(search_filter),
                Student.student_id.like(search_filter),
                Student.major.like(search_filter)
            )
        )
    
    # 排序（使用索引字段）
    query = query.order_by(Student.student_id.desc())
    
    # 分页
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return pagination
```

## 本章小结

在本章中，我们深入学习了：
- ✅ SQLAlchemy ORM的核心概念和架构
- ✅ 数据库迁移的管理和最佳实践
- ✅ 完整的CRUD操作实现
- ✅ 多层次的数据验证机制
- ✅ 异常处理和错误管理
- ✅ 查询优化技巧

## 下一章预告

在第五章中，我们将学习前端界面开发，包括：
- Bootstrap框架的深入使用
- 响应式设计原理和实践
- JavaScript交互功能实现
- 表单验证和用户体验优化
- 现代Web UI设计模式

现在我们已经掌握了强大的数据库操作能力，接下来让我们创建美观易用的用户界面！