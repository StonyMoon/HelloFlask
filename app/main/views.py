#coding:utf8
from . import main
from flask import Flask, redirect, make_response, request, abort, render_template, url_for, session, flash
from .forms import PostForm, mail_form, EditProfileForm, CommentForm,TodoForm
from app import mail, db, models
from flask_mail import Message
from ..decorators import admin_required
from flask_login import login_required, current_user
from ..models import User, Post, Permission, Comment,TodoList
import datetime

@main.route('/index', methods=['POST', 'GET'])
def send_mail(to, title, mes):
    msg = Message(title, sender='934998206@qq.com', recipients=[to])
    msg.body = mes
    mail.send(msg)


@main.route('/todo', methods=['POST', 'GET'])
@login_required
@admin_required
def todo():
    form = TodoForm()
    if form.is_submitted():
        todo = TodoList(body = form.task.data)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('main.todo'))
    todo = TodoList.query.order_by(TodoList.id.asc()).all()
    return render_template('todo.html', form=form,todo=todo)

@main.route('/todo/delete/<id>')
@login_required
@admin_required
def delete_todo(id):
    db.session.delete(TodoList.query.get_or_404(id))
    db.session.commit()
    return

@main.route('/', methods=['POST', 'GET'])
def hello_world():
    page = request.args.get('page', 1, type=int)  # 无参数则默认为1,type作用:参数无法转为int时则默认为1

    form = PostForm()
    if form.is_submitted() and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body=form.body.data, author_id=current_user.id, title=form.title.data, type=form.post_type.data,
                    timestamp=datetime.datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.hello_world'))
    # 分页
    if current_user.is_administrator():
        pagination = Post.query.order_by(Post.id.desc()).paginate(page, per_page=10, error_out=False)
    else:
        pagination = Post.query.filter(Post.visible == 1).order_by(Post.id.desc()).paginate(page, per_page=10,
                                                                                            error_out=False)
    # 拿到一页内容
    todo = TodoList.query.order_by(TodoList.id.asc()).all()
    posts = pagination.items
    types = get_types()

    return render_template('blog.html', form=form, posts=posts, pagination=pagination, todo=todo, types=types)


@main.route('/mail', methods=['POST', 'GET'])
def mail_sender():
    form = mail_form()
    if form.is_submitted():
        send_mail(form.re.data, form.title.data, form.text.data)
        form.re.data = form.title.data = form.text.data = ''
        return redirect(url_for('main.mail_sender'))  # 注意一下此处的转跳地址

    return render_template('mail.html', form=form)


@main.route('/delete/<id>')
@login_required
@admin_required
def delete(id):
    db.session.delete(Comment.query.get_or_404(id))
    db.session.commit()
    return


@main.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.id.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.is_submitted():
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.add(current_user)
        db.session.commit()
    return render_template('mail.html', form=form)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    form = CommentForm()
    post = Post.query.get_or_404(id)
    comments = post.comments.order_by(Comment.id.desc()).all()
    if form.is_submitted():
        comment = Comment(post_id=id, author_id=current_user.id, body=form.body.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.post', id=id))
    types = get_types()
    return render_template('post.html', post=post, form=form, comments=comments, types=types)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = PostForm()
    post = Post.query.get_or_404(id)
    if post.author_id != current_user.id and not current_user.is_administrator():
        abort(404)
    if form.is_submitted():
        post.body = form.body.data
        post.title = form.title.data
        post.type = form.post_type.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.hello_world'))
    form.body.data = post.body
    form.title.data = post.title
    form.post_type.data = post.type
    return render_template('edit.html', post=post, form=form)


@main.route('/type/<type>')
def select(type):
    page = request.args.get('page', 1, type=int)  # 无参数则默认为1,type作用:参数无法转为int时则默认为1
    form = PostForm()
    if form.is_submitted() and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body=form.body.data, author_id=current_user.id, title=form.title.data, type=form.post_type.data)
        db.session.add(post)
        db.session.commit()
        return redirect('http://127.0.0.1:5000/')
    # 分页
    if current_user.is_administrator():
        pagination = Post.query.filter_by(type=type).order_by(Post.id.desc()).paginate(page, per_page=10,
                                                                                          error_out=False)
    else:
        pagination = Post.query.filter_by(type=type).filter(Post.visible == 1).order_by(Post.id.desc()).paginate(page,
                                                                                                                 per_page=10,
                                                                                                                 error_out=False)
    # 拿到一页内容
    posts = pagination.items
    types = get_types()
    return render_template('blog.html', form=form, posts=posts, pagination=pagination, types=types)



@main.route('/search/<word>')
def search(word):
    page = request.args.get('page', 1, type=int)  # 无参数则默认为1,type作用:参数无法转为int时则默认为1
    form = PostForm()
    if current_user.is_administrator():
        pagination = Post.query.filter(Post.title.like('%' + word + '%')).order_by(Post.id.desc()).paginate(page,
                                                                                                            per_page=10,
                                                                                                            error_out=False)
    else:
        pagination = Post.query.filter(Post.title.like('%' + word + '%')).filter(Post.visible == 1).order_by(
            Post.id.desc()).paginate(page,
                                     per_page=10,
                                     error_out=False)

    # 拿到一页内容
    posts = pagination.items
    types = get_types()
    return render_template('blog.html', form=form, posts=posts, pagination=pagination, types=types)


def get_types():
    if current_user.is_administrator():
        types = db.session.query(Post.type).all()
    else:
        types = db.session.query(Post.type).filter(Post.visible == 1).all()
    tp = {}
    for each in types:
        if tp.get(each[0]) is None:
            tp[each[0]] = 1
        else:
            tp[each[0]] += 1
    return tp
