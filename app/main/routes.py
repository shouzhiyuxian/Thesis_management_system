from flask import render_template, redirect, url_for, session
from app.main import bp

@bp.route('/')
def index():
    """首页"""
    return render_template('main/index.html')

@bp.route('/about')
def about():
    """关于页面"""
    return render_template('main/about.html')
