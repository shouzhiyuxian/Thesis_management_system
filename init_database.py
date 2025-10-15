#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
"""

from app import create_app, db
from app.models import Student, Teacher, Admin, Class, Grade, NativePlace, ProcessStatus

def init_database():
    """初始化数据库和基础数据"""
    app = create_app()
    
    with app.app_context():
        print("正在创建数据库表...")
        db.create_all()
        print("数据库表创建完成！")
        
        # 创建基础数据
        print("正在创建基础数据...")
        
        # 创建班级
        if not Class.query.first():
            classes = [
                Class(name='计算机科学与技术1班'),
                Class(name='计算机科学与技术2班'),
                Class(name='软件工程1班'),
                Class(name='软件工程2班'),
                Class(name='网络工程1班'),
                Class(name='信息安全1班'),
            ]
            for cls in classes:
                db.session.add(cls)
            print("班级数据创建完成！")
        
        # 创建年级
        if not Grade.query.first():
            grades = [
                Grade(name='2020级'),
                Grade(name='2021级'),
                Grade(name='2022级'),
                Grade(name='2023级'),
            ]
            for grade in grades:
                db.session.add(grade)
            print("年级数据创建完成！")
        
        # 创建籍贯
        if not NativePlace.query.first():
            places = [
                NativePlace(name='北京'),
                NativePlace(name='上海'),
                NativePlace(name='广东'),
                NativePlace(name='浙江'),
                NativePlace(name='江苏'),
                NativePlace(name='山东'),
                NativePlace(name='河南'),
                NativePlace(name='四川'),
                NativePlace(name='湖北'),
                NativePlace(name='福建'),
            ]
            for place in places:
                db.session.add(place)
            print("籍贯数据创建完成！")
        
        # 创建管理员
        if not Admin.query.first():
            admin = Admin(
                admin_no='admin001',
                username='系统管理员',
                password='admin123',
                sex='男',
                birth='1990-01-01',
                native_place_id=1
            )
            db.session.add(admin)
            print("默认管理员账号创建完成！")
        
        # 创建示例教师
        if not Teacher.query.first():
            teacher = Teacher(
                teacher_no='T001',
                username='张教授',
                password='teacher123',
                sex='男',
                birth='1980-05-15',
                native_place_id=1,
                descs='计算机科学与技术专业教授，研究方向：人工智能、机器学习'
            )
            db.session.add(teacher)
            print("示例教师账号创建完成！")
        
        # 创建示例学生
        if not Student.query.first():
            student = Student(
                student_no='2020001001',
                username='李同学',
                password='student123',
                sex='男',
                birth='2002-03-20',
                native_place_id=2,
                class_id=1,
                grade_id=1,
                teacher_id=1
            )
            db.session.add(student)
            print("示例学生账号创建完成！")
        
        # 创建进程状态
        if not ProcessStatus.query.first():
            process = ProcessStatus(
                releasing_notices='1',
                complete_personal_data='1',
                upload_paper_guide='1',
                upload_end_evaluate='1'
            )
            db.session.add(process)
            print("进程状态数据创建完成！")
        
        # 提交所有更改
        db.session.commit()
        print("数据库初始化完成！")
        print("\n默认账号信息：")
        print("管理员：admin001 / admin123")
        print("教师：T001 / teacher123")
        print("学生：2020001001 / student123")

if __name__ == '__main__':
    init_database()
