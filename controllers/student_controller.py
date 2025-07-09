from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.student import Student
from app import db

# 创建蓝图
student_bp = Blueprint('student', __name__, url_prefix='/students')

@student_bp.route('/')
def index():
    """学生列表页面"""
    students = Student.get_all()
    return render_template('students/index.html', students=students)

@student_bp.route('/add', methods=['GET', 'POST'])
def add():
    """添加学生"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            student_id = request.form.get('student_id')
            name = request.form.get('name')
            gender = request.form.get('gender')
            age = int(request.form.get('age'))
            major = request.form.get('major')
            grade = request.form.get('grade')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            
            # 检查学号是否已存在
            if Student.get_by_student_id(student_id):
                flash('学号已存在！', 'error')
                return render_template('students/add.html')
            
            # 创建新学生
            student = Student(
                student_id=student_id,
                name=name,
                gender=gender,
                age=age,
                major=major,
                grade=grade,
                phone=phone,
                email=email,
                address=address
            )
            
            student.save()
            flash('学生添加成功！', 'success')
            return redirect(url_for('student.index'))
            
        except Exception as e:
            flash(f'添加失败：{str(e)}', 'error')
            return render_template('students/add.html')
    
    return render_template('students/add.html')

@student_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """编辑学生信息"""
    student = Student.get_by_id(id)
    if not student:
        flash('学生不存在！', 'error')
        return redirect(url_for('student.index'))
    
    if request.method == 'POST':
        try:
            # 更新学生信息
            student.name = request.form.get('name')
            student.gender = request.form.get('gender')
            student.age = int(request.form.get('age'))
            student.major = request.form.get('major')
            student.grade = request.form.get('grade')
            student.phone = request.form.get('phone')
            student.email = request.form.get('email')
            student.address = request.form.get('address')
            
            db.session.commit()
            flash('学生信息更新成功！', 'success')
            return redirect(url_for('student.index'))
            
        except Exception as e:
            flash(f'更新失败：{str(e)}', 'error')
    
    return render_template('students/edit.html', student=student)

@student_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """删除学生"""
    student = Student.get_by_id(id)
    if not student:
        flash('学生不存在！', 'error')
        return redirect(url_for('student.index'))
    
    try:
        student.delete()
        flash('学生删除成功！', 'success')
    except Exception as e:
        flash(f'删除失败：{str(e)}', 'error')
    
    return redirect(url_for('student.index'))

@student_bp.route('/view/<int:id>')
def view(id):
    """查看学生详情"""
    student = Student.get_by_id(id)
    if not student:
        flash('学生不存在！', 'error')
        return redirect(url_for('student.index'))
    
    return render_template('students/view.html', student=student)

@student_bp.route('/search')
def search():
    """搜索学生"""
    query = request.args.get('q', '')
    if query:
        students = Student.query.filter(
            db.or_(
                Student.name.contains(query),
                Student.student_id.contains(query),
                Student.major.contains(query)
            )
        ).all()
    else:
        students = Student.get_all()
    
    return render_template('students/index.html', students=students, search_query=query)

# API路由
@student_bp.route('/api/list')
def api_list():
    """API：获取学生列表"""
    students = Student.get_all()
    return jsonify({
        'success': True,
        'data': [student.to_dict() for student in students]
    })

@student_bp.route('/api/<int:id>')
def api_get(id):
    """API：获取单个学生信息"""
    student = Student.get_by_id(id)
    if not student:
        return jsonify({
            'success': False,
            'message': '学生不存在'
        }), 404
    
    return jsonify({
        'success': True,
        'data': student.to_dict()
    })