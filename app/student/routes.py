from flask import render_template, redirect, url_for, flash, request, session, send_from_directory
from werkzeug.utils import secure_filename
from app import db
from app.models import Student, Teacher, Notice, Guide, Paper, Comment, ProcessStatus
from app.student import bp
import os
from datetime import datetime

def student_required(f):
    """学生权限装饰器"""
    def decorated_function(*args, **kwargs):
        if session.get('user_type') != 'student':
            flash('需要学生权限', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/dashboard')
@student_required
def dashboard():
    student_no = session.get('user_no')
    student = Student.query.filter_by(student_no=student_no).first()
    
    if not student:
        flash('学生信息不存在', 'error')
        return redirect(url_for('auth.login'))
    
    # 统计数据
    paper_count = Paper.query.filter_by(student_no=student_no).count()
    comment_count = Comment.query.filter_by(student_no=student_no).count()
    
    # 最新通知
    recent_notices = Notice.query.order_by(Notice.create_date.desc()).limit(5).all()
    
    # 我的论文
    my_papers = Paper.query.filter_by(student_no=student_no).order_by(
        Paper.upload_time.desc()).limit(5).all()
    
    # 最新的批阅
    recent_comments = Comment.query.filter_by(student_no=student_no).order_by(
        Comment.create_time.desc()).limit(5).all()
    
    return render_template('student/dashboard.html', 
                         student=student,
                         paper_count=paper_count,
                         comment_count=comment_count,
                         recent_notices=recent_notices,
                         my_papers=my_papers,
                         recent_comments=recent_comments)

@bp.route('/notices')
@student_required
def notices():
    page = request.args.get('page', 1, type=int)
    notices = Notice.query.order_by(Notice.create_date.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('student/notices.html', notices=notices)

@bp.route('/notice/<int:notice_id>')
@student_required
def view_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    return render_template('student/view_notice.html', notice=notice)

@bp.route('/guides')
@student_required
def guides():
    page = request.args.get('page', 1, type=int)
    guides = Guide.query.order_by(Guide.create_date.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('student/guides.html', guides=guides)

@bp.route('/download_guide/<int:guide_id>')
@student_required
def download_guide(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    
    # 更新下载次数
    guide.download_time += 1
    db.session.commit()
    
    # 获取文件目录和文件名
    file_dir = os.path.dirname(guide.file_path)
    file_name = os.path.basename(guide.file_path)
    
    return send_from_directory(file_dir, file_name, as_attachment=True)

@bp.route('/papers')
@student_required
def papers():
    student_no = session.get('user_no')
    page = request.args.get('page', 1, type=int)
    papers = Paper.query.filter_by(student_no=student_no).order_by(
        Paper.upload_time.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('student/papers.html', papers=papers)

@bp.route('/upload_paper', methods=['GET', 'POST'])
@student_required
def upload_paper():
    # 检查进程状态
    process_status = ProcessStatus.query.first()
    if not process_status or process_status.upload_end_evaluate != '1':
        flash('当前不允许上传论文', 'error')
        return redirect(url_for('student.papers'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有选择文件', 'error')
            return render_template('student/upload_paper.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('没有选择文件', 'error')
            return render_template('student/upload_paper.html')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 添加时间戳避免文件名冲突
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            # 创建学生专用目录
            student_no = session.get('user_no')
            student_dir = os.path.join(request.form.get('upload_folder'), 'papers', student_no)
            os.makedirs(student_dir, exist_ok=True)

            file_path = os.path.join(student_dir, filename)

            # 查找是否已有论文，若有则删除旧文件和数据库记录
            old_paper = Paper.query.filter_by(student_no=student_no).order_by(Paper.upload_time.desc()).first()
            if old_paper:
                try:
                    if os.path.exists(old_paper.save_path):
                        os.remove(old_paper.save_path)
                except Exception:
                    pass
                db.session.delete(old_paper)
                db.session.commit()

            file.save(file_path)

            paper = Paper(
                paper_name=request.form.get('paper_name', file.filename),
                student_no=student_no,
                teacher_no=request.form.get('teacher_no'),
                save_path=file_path
            )
            db.session.add(paper)
            db.session.commit()

            flash('论文上传成功', 'success')
            return redirect(url_for('student.papers'))
        else:
            flash('不支持的文件类型', 'error')
    
    # 获取学生信息以获取指导教师
    student_no = session.get('user_no')
    student = Student.query.filter_by(student_no=student_no).first()
    
    return render_template('student/upload_paper.html', student=student)

@bp.route('/paper/<int:paper_id>')
@student_required
def view_paper(paper_id):
    student_no = session.get('user_no')
    paper = Paper.query.filter_by(id=paper_id, student_no=student_no).first_or_404()
    
    # 获取该论文的所有批阅记录
    comments = Comment.query.filter_by(paper_id=paper_id).order_by(
        Comment.create_time.desc()).all()
    
    return render_template('student/view_paper.html', paper=paper, comments=comments)

@bp.route('/download_paper/<int:paper_id>')
@student_required
def download_paper(paper_id):
    student_no = session.get('user_no')
    paper = Paper.query.filter_by(id=paper_id, student_no=student_no).first_or_404()
    
    # 获取文件目录和文件名
    file_dir = os.path.dirname(paper.save_path)
    file_name = os.path.basename(paper.save_path)
    
    return send_from_directory(file_dir, file_name, as_attachment=True)

@bp.route('/comments')
@student_required
def comments():
    student_no = session.get('user_no')
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(student_no=student_no).order_by(
        Comment.create_time.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('student/comments.html', comments=comments)

@bp.route('/profile')
@student_required
def profile():
    student_no = session.get('user_no')
    student = Student.query.filter_by(student_no=student_no).first()
    
    if not student:
        flash('学生信息不存在', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('student/profile.html', student=student)

@bp.route('/update_profile', methods=['GET', 'POST'])
@student_required
def update_profile():
    student_no = session.get('user_no')
    student = Student.query.filter_by(student_no=student_no).first()
    
    if not student:
        flash('学生信息不存在', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        student.username = request.form.get('username')
        student.sex = request.form.get('sex')
        student.birth = request.form.get('birth')
        student.native_place_id = request.form.get('native_place_id', type=int)
        
        db.session.commit()
        flash('个人信息更新成功', 'success')
        return redirect(url_for('student.profile'))
    
    return render_template('student/update_profile.html', student=student)

def allowed_file(filename):
    """检查文件类型是否允许"""
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
