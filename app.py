from flask import Flask
from app import create_app, db
from app.models import Student, Teacher, Admin, Class, Grade, NativePlace, ProcessStatus

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student, 'Teacher': Teacher, 'Admin': Admin, 
            'Class': Class, 'Grade': Grade, 'NativePlace': NativePlace, 
            'ProcessStatus': ProcessStatus}

@app.cli.command()
def init_db():
    """初始化数据库"""
    db.create_all()
    
    # 创建初始数据
    if not Class.query.first():
        classes = [
            Class(name='计算机科学与技术1班'),
            Class(name='计算机科学与技术2班'),
            Class(name='软件工程1班'),
            Class(name='软件工程2班'),
        ]
        for cls in classes:
            db.session.add(cls)
    
    if not Grade.query.first():
        grades = [
            Grade(name='2020级'),
            Grade(name='2021级'),
            Grade(name='2022级'),
        ]
        for grade in grades:
            db.session.add(grade)
    
    if not NativePlace.query.first():
        places = [
            NativePlace(name='北京'),
            NativePlace(name='上海'),
            NativePlace(name='广东'),
            NativePlace(name='浙江'),
            NativePlace(name='江苏'),
        ]
        for place in places:
            db.session.add(place)
    
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
    
    if not ProcessStatus.query.first():
        process = ProcessStatus()
        db.session.add(process)
    
    db.session.commit()
    print('数据库初始化完成！')

if __name__ == '__main__':
    app.run(debug=True)
