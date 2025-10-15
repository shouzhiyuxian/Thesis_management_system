from flask import render_template, redirect, url_for, flash, request, session, send_from_directory
from werkzeug.utils import secure_filename
from app import db
from app.models import Teacher, Student, Notice, Guide, Paper, Comment, ProcessStatus
from app.teacher import bp
import os
from datetime import datetime

def teacher_required(f):
    """教师权限装饰器"""
    def decorated_function(*args, **kwargs):
        if session.get('user_type') != 'teacher':
            flash('需要教师权限', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/dashboard')
@teacher_required
def dashboard():
    teacher_no = session.get('user_no')
    teacher = Teacher.query.filter_by(teacher_no=teacher_no).first()
    
    if not teacher:
        flash('教师信息不存在', 'error')
        return redirect(url_for('auth.login'))
    
    # 统计数据
    student_count = Student.query.filter_by(teacher_id=teacher.id).count()
    guide_count = Guide.query.filter_by(teacher_no=teacher_no).count()
    paper_count = Paper.query.filter_by(teacher_no=teacher_no).count()
    comment_count = Comment.query.filter_by(teacher_no=teacher_no).count()
    
    # 最新通知
    recent_notices = Notice.query.order_by(Notice.create_date.desc()).limit(5).all()
    
    # 我的学生
    my_students = Student.query.filter_by(teacher_id=teacher.id).all()
    
    return render_template('teacher/dashboard.html', 
                         teacher=teacher,
                         student_count=student_count,
                         guide_count=guide_count,
                         paper_count=paper_count,
                         comment_count=comment_count,
                         recent_notices=recent_notices,
                         my_students=my_students)

@bp.route('/notices')
@teacher_required
def notices():
    page = request.args.get('page', 1, type=int)
    notices = Notice.query.order_by(Notice.create_date.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('teacher/notices.html', notices=notices)

@bp.route('/add_notice', methods=['GET', 'POST'])
@teacher_required
def add_notice():
    # 检查进程状态
    process_status = ProcessStatus.query.first()
    if not process_status or process_status.releasing_notices != '1':
        flash('当前不允许发布通知', 'error')
        return redirect(url_for('teacher.notices'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        lead_foot = request.form.get('lead_foot', '')
        
        if not title or not content:
            flash('请填写标题和内容', 'error')
            return render_template('teacher/add_notice.html')
        
        notice = Notice(
            title=title,
            content=content,
            lead_foot=lead_foot,
            admin_id=session.get('user_id')  # 这里简化处理，实际应该有教师发布通知的字段
        )
        db.session.add(notice)
        db.session.commit()
        flash('通知发布成功', 'success')
        return redirect(url_for('teacher.notices'))
    
    return render_template('teacher/add_notice.html')

@bp.route('/guides')
@teacher_required
def guides():
    teacher_no = session.get('user_no')
    page = request.args.get('page', 1, type=int)
    guides = Guide.query.filter_by(teacher_no=teacher_no).order_by(
        Guide.create_date.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('teacher/guides.html', guides=guides)

@bp.route('/upload_guide', methods=['GET', 'POST'])
@teacher_required
def upload_guide():
    # 检查进程状态
    process_status = ProcessStatus.query.first()
    if not process_status or process_status.upload_paper_guide != '1':
        flash('当前不允许上传指导资料', 'error')
        return redirect(url_for('teacher.guides'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件', 'error')
            return render_template('teacher/upload_guide.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件', 'error')
            return render_template('teacher/upload_guide.html')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 添加时间戳避免文件名冲突
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            
            # 创建教师专用目录
            teacher_no = session.get('user_no')
            teacher_dir = os.path.join(request.form.get('upload_folder'), 'guides', teacher_no)
            os.makedirs(teacher_dir, exist_ok=True)
            
            file_path = os.path.join(teacher_dir, filename)
            file.save(file_path)
            
            guide = Guide(
                file_path=file_path,
                file_name=request.form.get('file_name', file.filename),
                teacher_no=teacher_no
            )
            db.session.add(guide)
            db.session.commit()
            
            flash('指导资料上传成功', 'success')
            return redirect(url_for('teacher.guides'))
        else:
            flash('不支持的文件类型', 'error')
    
    return render_template('teacher/upload_guide.html')

@bp.route('/papers')
@teacher_required
def papers():
    teacher_no = session.get('user_no')
    page = request.args.get('page', 1, type=int)
    papers = Paper.query.filter_by(teacher_no=teacher_no).order_by(
        Paper.upload_time.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('teacher/papers.html', papers=papers)

@bp.route('/review_paper/<int:paper_id>', methods=['GET', 'POST'])
@teacher_required
def review_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('请填写批阅内容', 'error')
            return render_template('teacher/review_paper.html', paper=paper)
        
        comment = Comment(
            paper_id=paper_id,
            teacher_no=session.get('user_no'),
            student_no=paper.student_no,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
        
        flash('批阅提交成功', 'success')
        return redirect(url_for('teacher.papers'))
    
    # 获取该论文的所有批阅记录
    comments = Comment.query.filter_by(paper_id=paper_id).order_by(
        Comment.create_time.desc()).all()
    
    return render_template('teacher/review_paper.html', paper=paper, comments=comments)

@bp.route('/students')
@teacher_required
def students():
    teacher_no = session.get('user_no')
    teacher = Teacher.query.filter_by(teacher_no=teacher_no).first()
    
    if not teacher:
        flash('教师信息不存在', 'error')
        return redirect(url_for('teacher.dashboard'))
    
    students = Student.query.filter_by(teacher_id=teacher.id).all()
    return render_template('teacher/students.html', students=students)

def allowed_file(filename):
    """检查文件类型是否允许"""
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
