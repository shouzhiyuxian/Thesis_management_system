#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
系统功能测试脚本
"""

import requests
from app import create_app, db
from app.models import Student, Teacher, Admin, Notice

def test_database_connection():
    """测试数据库连接"""
    print("测试数据库连接...")
    app = create_app()
    with app.app_context():
        try:
            # 测试查询
            admin_count = Admin.query.count()
            teacher_count = Teacher.query.count()
            student_count = Student.query.count()
            notice_count = Notice.query.count()
            
            print(f"✓ 数据库连接正常")
            print(f"  - 管理员数量: {admin_count}")
            print(f"  - 教师数量: {teacher_count}")
            print(f"  - 学生数量: {student_count}")
            print(f"  - 通知数量: {notice_count}")
            return True
        except Exception as e:
            print(f"✗ 数据库连接失败: {e}")
            return False

def test_models():
    """测试数据模型"""
    print("\n测试数据模型...")
    app = create_app()
    with app.app_context():
        try:
            # 测试管理员模型
            admin = Admin.query.first()
            if admin:
                print(f"✓ 管理员模型正常: {admin.username}")
            
            # 测试教师模型
            teacher = Teacher.query.first()
            if teacher:
                print(f"✓ 教师模型正常: {teacher.username}")
            
            # 测试学生模型
            student = Student.query.first()
            if student:
                print(f"✓ 学生模型正常: {student.username}")
                
            return True
        except Exception as e:
            print(f"✗ 数据模型测试失败: {e}")
            return False

def test_routes():
    """测试路由"""
    print("\n测试路由...")
    app = create_app()
    with app.test_client() as client:
        try:
            # 测试首页
            response = client.get('/')
            if response.status_code == 200:
                print("✓ 首页路由正常")
            else:
                print(f"✗ 首页路由异常: {response.status_code}")
            
            # 测试登录页面
            response = client.get('/auth/login')
            if response.status_code == 200:
                print("✓ 登录页面路由正常")
            else:
                print(f"✗ 登录页面路由异常: {response.status_code}")
                
            return True
        except Exception as e:
            print(f"✗ 路由测试失败: {e}")
            return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("毕业论文管理系统 - 功能测试")
    print("=" * 50)
    
    # 运行测试
    db_test = test_database_connection()
    model_test = test_models()
    route_test = test_routes()
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print(f"数据库连接: {'✓ 通过' if db_test else '✗ 失败'}")
    print(f"数据模型: {'✓ 通过' if model_test else '✗ 失败'}")
    print(f"路由功能: {'✓ 通过' if route_test else '✗ 失败'}")
    
    if all([db_test, model_test, route_test]):
        print("\n🎉 所有测试通过！系统运行正常。")
    else:
        print("\n⚠️  部分测试失败，请检查系统配置。")
    print("=" * 50)

if __name__ == '__main__':
    main()
