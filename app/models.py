from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

class Student(db.Model):
    """学生信息表"""
    __tablename__ = 't_student'
    
    id = db.Column(db.Integer, primary_key=True)
    student_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    sex = db.Column(db.String(2))
    native_place_id = db.Column(db.Integer, db.ForeignKey('t_nativeplace.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('t_class.id'))
    grade_id = db.Column(db.Integer, db.ForeignKey('t_grade.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('t_teacher.id'))
    birth = db.Column(db.String(20))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    native_place = db.relationship('NativePlace', backref='students')
    class_info = db.relationship('Class', backref='students')
    grade = db.relationship('Grade', backref='students')
    teacher = db.relationship('Teacher', backref='students')
    papers = db.relationship('Paper', backref='student', lazy='dynamic')
    comments = db.relationship('Comment', backref='student', lazy='dynamic')

class Teacher(db.Model):
    """教师信息表"""
    __tablename__ = 't_teacher'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    teacher_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    sex = db.Column(db.String(2))
    native_place_id = db.Column(db.Integer, db.ForeignKey('t_nativeplace.id'))
    birth = db.Column(db.String(20))
    descs = db.Column(db.String(2000))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    native_place = db.relationship('NativePlace', backref='teachers')
    guides = db.relationship('Guide', backref='teacher', lazy='dynamic')
    papers = db.relationship('Paper', backref='teacher', lazy='dynamic')
    comments = db.relationship('Comment', backref='teacher', lazy='dynamic')

class Admin(db.Model):
    """管理员信息表"""
    __tablename__ = 't_admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    admin_no = db.Column(db.String(20), unique=True, nullable=False, index=True)
    sex = db.Column(db.String(2))
    native_place_id = db.Column(db.Integer, db.ForeignKey('t_nativeplace.id'))
    birth = db.Column(db.String(20))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    native_place = db.relationship('NativePlace', backref='admins')
    notices = db.relationship('Notice', backref='admin', lazy='dynamic')

class Class(db.Model):
    """班级信息表"""
    __tablename__ = 't_class'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class Grade(db.Model):
    """年级信息表"""
    __tablename__ = 't_grade'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class NativePlace(db.Model):
    """籍贯信息表"""
    __tablename__ = 't_nativeplace'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class Notice(db.Model):
    """通知信息表"""
    __tablename__ = 't_notice'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    lead_foot = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('t_admin.id'))

class Guide(db.Model):
    """指导资料信息表"""
    __tablename__ = 't_guide'
    
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(200), nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    teacher_no = db.Column(db.String(20), db.ForeignKey('t_teacher.teacher_no'))
    download_time = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

class PaperRequire(db.Model):
    """论文需求资料信息表"""
    __tablename__ = 't_paperrequire'
    
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

class Paper(db.Model):
    """论文信息表"""
    __tablename__ = 't_paper'
    
    id = db.Column(db.Integer, primary_key=True)
    paper_name = db.Column(db.String(200), nullable=False)
    student_no = db.Column(db.String(20), db.ForeignKey('t_student.student_no'))
    teacher_no = db.Column(db.String(20), db.ForeignKey('t_teacher.teacher_no'))
    save_path = db.Column(db.String(200), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    comments = db.relationship('Comment', backref='paper', lazy='dynamic')

class ProcessStatus(db.Model):
    """流程信息表"""
    __tablename__ = 't_processstatus'
    
    id = db.Column(db.Integer, primary_key=True)
    releasing_notices = db.Column(db.String(5), default='0')
    complete_personal_data = db.Column(db.String(5), default='0')
    upload_paper_guide = db.Column(db.String(5), default='0')
    upload_end_evaluate = db.Column(db.String(5), default='0')

class Comment(db.Model):
    """教师批阅信息表"""
    __tablename__ = 't_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('t_paper.id'))
    teacher_no = db.Column(db.String(20), db.ForeignKey('t_teacher.teacher_no'))
    student_no = db.Column(db.String(20), db.ForeignKey('t_student.student_no'))
    content = db.Column(db.String(1000), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)




