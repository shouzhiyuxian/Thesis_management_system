from flask import render_template, redirect, url_for, flash, request, session, send_from_directory
from werkzeug.utils import secure_filename
from app import db
from app.models import Admin, Teacher, Student, Notice, ProcessStatus, Class, Grade, NativePlace, Paper, Comment, Guide
from app.admin import bp
import os
from datetime import datetime

def admin_required(f):
    """管理员权限装饰器"""
    def decorated_function(*args, **kwargs):
        if session.get('user_type') != 'admin':
            flash('需要管理员权限', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/dashboard')
@admin_required
def dashboard():
    # 统计数据
    student_count = Student.query.count()
    teacher_count = Teacher.query.count()
    notice_count = Notice.query.count()
    paper_count = Paper.query.count()
    
    # 最新通知
    recent_notices = Notice.query.order_by(Notice.create_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         student_count=student_count,
                         teacher_count=teacher_count,
                         notice_count=notice_count,
                         paper_count=paper_count,
                         recent_notices=recent_notices)

@bp.route('/users')
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    user_type = request.args.get('type', 'all')
    
    if user_type == 'student':
        users = Student.query.paginate(page=page, per_page=10, error_out=False)
    elif user_type == 'teacher':
        users = Teacher.query.paginate(page=page, per_page=10, error_out=False)
    else:
        # 显示所有用户，这里简化处理，只显示学生和教师
        users = Student.query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('admin/users.html', users=users, user_type=user_type)

@bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        username = request.form.get('username')
        password = request.form.get('password')
        sex = request.form.get('sex')
        birth = request.form.get('birth')
        native_place_id = request.form.get('native_place_id', type=int)
        
        if user_type == 'student':
            student_no = request.form.get('student_no')
            class_id = request.form.get('class_id', type=int)
            grade_id = request.form.get('grade_id', type=int)
            teacher_id = request.form.get('teacher_id', type=int)
            
            if Student.query.filter_by(student_no=student_no).first():
                flash('学号已存在', 'error')
                return render_template('admin/add_user.html')
            
            student = Student(
                student_no=student_no,
                username=username,
                password=password,
                sex=sex,
                birth=birth,
                native_place_id=native_place_id,
                class_id=class_id,
                grade_id=grade_id,
                teacher_id=teacher_id
            )
            db.session.add(student)
            
        elif user_type == 'teacher':
            teacher_no = request.form.get('teacher_no')
            descs = request.form.get('descs', '')
            
            if Teacher.query.filter_by(teacher_no=teacher_no).first():
                flash('教师编号已存在', 'error')
                return render_template('admin/add_user.html')
            
            teacher = Teacher(
                teacher_no=teacher_no,
                username=username,
                password=password,
                sex=sex,
                birth=birth,
                native_place_id=native_place_id,
                descs=descs
            )
            db.session.add(teacher)
        
        db.session.commit()
        flash('用户添加成功', 'success')
        return redirect(url_for('admin.users'))
    
    # 获取选项数据
    classes = Class.query.all()
    grades = Grade.query.all()
    teachers = Teacher.query.all()
    native_places = NativePlace.query.all()
    
    return render_template('admin/add_user.html', 
                         classes=classes, 
                         grades=grades, 
                         teachers=teachers,
                         native_places=native_places)

@bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user_type = request.args.get('type', 'student')
    
    if user_type == 'student':
        user = Student.query.get_or_404(user_id)
    elif user_type == 'teacher':
        user = Teacher.query.get_or_404(user_id)
    else:
        flash('无效的用户类型', 'error')
        return redirect(url_for('admin.users'))
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.password = request.form.get('password')
        user.sex = request.form.get('sex')
        user.birth = request.form.get('birth')
        user.native_place_id = request.form.get('native_place_id', type=int)
        
        if user_type == 'student':
            user.class_id = request.form.get('class_id', type=int)
            user.grade_id = request.form.get('grade_id', type=int)
            user.teacher_id = request.form.get('teacher_id', type=int)
        elif user_type == 'teacher':
            user.descs = request.form.get('descs', '')
        
        db.session.commit()
        flash('用户信息更新成功', 'success')
        return redirect(url_for('admin.users'))
    
    # 获取选项数据
    classes = Class.query.all()
    grades = Grade.query.all()
    teachers = Teacher.query.all()
    native_places = NativePlace.query.all()
    
    return render_template('admin/edit_user.html', 
                         user=user, 
                         user_type=user_type,
                         classes=classes, 
                         grades=grades, 
                         teachers=teachers,
                         native_places=native_places)

@bp.route('/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    user_type = request.args.get('type', 'student')
    
    if user_type == 'student':
        user = Student.query.get_or_404(user_id)
    elif user_type == 'teacher':
        user = Teacher.query.get_or_404(user_id)
    else:
        flash('无效的用户类型', 'error')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/notices')
@admin_required
def notices():
    page = request.args.get('page', 1, type=int)
    notices = Notice.query.order_by(Notice.create_date.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/notices.html', notices=notices)

@bp.route('/add_notice', methods=['GET', 'POST'])
@admin_required
def add_notice():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        lead_foot = request.form.get('lead_foot', '')
        
        if not title or not content:
            flash('请填写标题和内容', 'error')
            return render_template('admin/add_notice.html')
        
        notice = Notice(
            title=title,
            content=content,
            lead_foot=lead_foot,
            admin_id=session.get('user_id')
        )
        db.session.add(notice)
        db.session.commit()
        flash('通知发布成功', 'success')
        return redirect(url_for('admin.notices'))
    
    return render_template('admin/add_notice.html')

@bp.route('/edit_notice/<int:notice_id>', methods=['GET', 'POST'])
@admin_required
def edit_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    
    if request.method == 'POST':
        notice.title = request.form.get('title')
        notice.content = request.form.get('content')
        notice.lead_foot = request.form.get('lead_foot', '')
        
        db.session.commit()
        flash('通知更新成功', 'success')
        return redirect(url_for('admin.notices'))
    
    return render_template('admin/edit_notice.html', notice=notice)

@bp.route('/delete_notice/<int:notice_id>')
@admin_required
def delete_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    flash('通知删除成功', 'success')
    return redirect(url_for('admin.notices'))

@bp.route('/process_control', methods=['GET', 'POST'])
@admin_required
def process_control():
    process_status = ProcessStatus.query.first()
    if not process_status:
        process_status = ProcessStatus()
        db.session.add(process_status)
        db.session.commit()
    
    if request.method == 'POST':
        process_status.releasing_notices = '1' if request.form.get('releasing_notices') else '0'
        process_status.complete_personal_data = '1' if request.form.get('complete_personal_data') else '0'
        process_status.upload_paper_guide = '1' if request.form.get('upload_paper_guide') else '0'
        process_status.upload_end_evaluate = '1' if request.form.get('upload_end_evaluate') else '0'
        
        db.session.commit()
        flash('进程状态更新成功', 'success')
        return redirect(url_for('admin.process_control'))
    
    return render_template('admin/process_control.html', process_status=process_status)

@bp.route('/papers')
@admin_required
def papers():
    page = request.args.get('page', 1, type=int)
    papers = Paper.query.order_by(Paper.upload_time.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/papers.html', papers=papers)

@bp.route('/comments')
@admin_required
def comments():
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.order_by(Comment.create_time.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/comments.html', comments=comments)
