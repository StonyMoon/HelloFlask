import os
from flask import Flask,redirect,make_response,request,abort,render_template,url_for,session,flash
from flask_wtf import Form
from wtforms import StringField,SubmitField , TextAreaField
from wtforms.validators import DataRequired

from flask_script import Manager


manager = Manager(app)



class flask_users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)

def send_mail(to,title,mes):
    msg = Message(title, sender = '934998206@qq.com',recipients=[to])
    msg.body = mes
    mail.send(msg)

@app.route('/index',methods=['POST','GET'])
def hello_world():
    form = NameForm()
    old_name = session.get('name')
    send_mail()
    if form.is_submitted():
        if old_name != form.name.data:
            flash("Looks like you have changed your name!")
        session['name'] = form.name.data #此处知识点:重定向,session段保存用户数据
        return redirect('http://127.0.0.1:5000/index')
    return render_template('index.html' , form=form , name=session.get('name'))
@app.route('/mail',methods = ['POST','GET'])
def mail_sender():
    form = mail_form()
    if form.is_submitted():
        send_mail(form.re.data,form.title.data,form.text.data)
        form.re.data = form.title.data = form.text.data = ''
        return redirect(url_for('mail_sender'))
    return render_template('mail.html',form = form)

if __name__ == '__main__':
    app.run()