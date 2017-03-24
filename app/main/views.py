from . import main
from flask import Flask,redirect,make_response,request,abort,render_template,url_for,session,flash
from .forms import PostForm,mail_form,EditProfileForm
from app import mail,db,models
from flask_mail import  Message
from ..decorators import admin_required
from flask_login import login_required,current_user
from .. models import User,Post,Permission
@main.route('/index',methods=['POST','GET'])
def send_mail(to, title, mes):
    msg = Message(title, sender='934998206@qq.com', recipients=[to])
    msg.body = mes
    mail.send(msg)
@main.route('/',methods=['POST','GET'])
def hello_world():
    form = PostForm()
    if form.is_submitted() and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body=form.body.data,author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect('http://127.0.0.1:5000/')
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html' , form=form , posts = posts)

@main.route('/mail',methods=['POST','GET'])
def mail_sender():
    form = mail_form()
    if form.is_submitted():
        send_mail(form.re.data,form.title.data,form.text.data)
        form.re.data = form.title.data = form.text.data = ''
        return redirect(url_for('main.mail_sender'))#注意一下此处的转跳地址

    return render_template('mail.html',form = form)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return 'For admins only'

@main.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)

@main.route('/edit-profile',methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.is_submitted:
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.add(current_user)
        db.session.commit()
    return render_template('mail.html',form = form)

