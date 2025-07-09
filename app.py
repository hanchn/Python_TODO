from config import app, db

# 导入模型和路由
from models.student import Student
from controllers.student_controller import student_bp

# 注册蓝图
app.register_blueprint(student_bp)

# 创建数据库表
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)