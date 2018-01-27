#coding:utf8
from . import auth
from flask import render_template, flash, session, redirect, url_for, request
from .. import models, login_manager, db
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from ..email import send_mail
from ..models import Post

#未验证账户禁止访问,暂时关闭此功能
# @auth.before_app_request
# def before_request():
#     if current_user.is_authenticated \
#             and not current_user.confirmed \
#             and request.endpoint[:5] != 'auth.' \
#             and request.endpoint != 'static':
#         return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.hello_world'))
    return redirect(url_for('main.hello_world'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Register', url_for('auth.con', token=token, _external=True))
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('main.hello_world'))


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.is_submitted():
        email = form.email.data
        input_password = form.password.data
        user = models.User.query.filter_by(email=email).first()
        if user != None and user.verify_password(input_password):
            session['name'] = user.name
            login_user(user, form.remember)
            return redirect(url_for('main.hello_world'))
        else:
            flash("输入错误,请重新输入")
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have benn logged out.')
    return redirect(url_for('main.hello_world'))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    return '<h1>Temporarily unable to register</h1>'
    db.create_all()
    form = RegisterForm()
    if form.is_submitted():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        password_ = form.password_.data
        if models.User.query.filter_by(name=name).first() != None:
            flash("该用户名已被使用")
        elif models.User.query.filter_by(email=email).first() != None:
            flash("该邮箱被使用")
        elif password != password_:
            flash("两次输入密码不相同")
        else:
            user = models.User(name=name, email=email)
            user.password_setter(password)
            db.session.add(user)
            db.session.commit()
            session['name'] = name
            token = user.generate_confirmation_token()
            send_mail(email, 'Register', url_for('auth.con', token=token, _external=True))
            flash('请到邮箱里验证帐号')
            return redirect(url_for('main.hello_world'))
    return render_template('register.html', form=form)


@auth.route('/con/<token>', methods=['POST', 'GET'])
def con(token):
    s = Serializer(current_app.config['SECRET_KEY'], 3600)
    try:
        id = s.loads(token)
        models.load_user(id).confirm()
    except:
        print('fail')
        return redirect(url_for('main.hello_world'))
    return redirect(url_for('main.hello_world'))


