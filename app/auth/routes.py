from flask import render_template, redirect, url_for, flash, request, session
from functools import wraps
from app import db
from app.models import Student, Teacher, Admin, ProcessStatus
from app.auth import bp

def login_required(f):
    """登录检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('请先登录', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        if not username or not password or not user_type:
            flash('请填写完整信息', 'error')
            return render_template('auth/login.html')
        
        user = None
        if user_type == 'admin':
            user = Admin.query.filter_by(admin_no=username).first()
        elif user_type == 'teacher':
            user = Teacher.query.filter_by(teacher_no=username).first()
        elif user_type == 'student':
            user = Student.query.filter_by(student_no=username).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            session['user_type'] = user_type
            session['username'] = user.username
            if hasattr(user, 'student_no'):
                session['user_no'] = user.student_no
            elif hasattr(user, 'teacher_no'):
                session['user_no'] = user.teacher_no
            elif hasattr(user, 'admin_no'):
                session['user_no'] = user.admin_no
            
            # 获取流程状态
            process_status = ProcessStatus.query.first()
            if not process_status:
                process_status = ProcessStatus()
                db.session.add(process_status)
                db.session.commit()
            
            flash(f'欢迎回来，{user.username}！', 'success')
            
            if user_type == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user_type == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            elif user_type == 'student':
                return redirect(url_for('student.dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('您已成功退出登录', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not old_password or not new_password or not confirm_password:
            flash('请填写完整信息', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('新密码确认不一致', 'error')
            return render_template('auth/change_password.html')
        
        user_type = session.get('user_type')
        user_id = session.get('user_id')
        
        user = None
        if user_type == 'admin':
            user = Admin.query.get(user_id)
        elif user_type == 'teacher':
            user = Teacher.query.get(user_id)
        elif user_type == 'student':
            user = Student.query.get(user_id)
        
        if user and user.password == old_password:
            user.password = new_password
            db.session.commit()
            flash('密码修改成功', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('原密码错误', 'error')
    
    return render_template('auth/change_password.html')
