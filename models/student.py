from config import db
from datetime import datetime

class Student(db.Model):
    """学生模型类"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, comment='学号')
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.String(10), nullable=False, comment='性别')
    age = db.Column(db.Integer, nullable=False, comment='年龄')
    major = db.Column(db.String(100), nullable=False, comment='专业')
    grade = db.Column(db.String(20), nullable=False, comment='年级')
    phone = db.Column(db.String(20), comment='电话号码')
    email = db.Column(db.String(100), comment='邮箱')
    address = db.Column(db.Text, comment='地址')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def __init__(self, student_id, name, gender, age, major, grade, phone=None, email=None, address=None):
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
        return f'<Student {self.student_id}: {self.name}>'
    
    def to_dict(self):
        """将模型转换为字典"""
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
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    @classmethod
    def get_all(cls):
        """获取所有学生"""
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, student_id):
        """根据ID获取学生"""
        return cls.query.get(student_id)
    
    @classmethod
    def get_by_student_id(cls, student_id):
        """根据学号获取学生"""
        return cls.query.filter_by(student_id=student_id).first()
    
    def save(self):
        """保存学生信息"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """删除学生信息"""
        db.session.delete(self)
        db.session.commit()