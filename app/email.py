from flask_mail import  Message
from flask import redirect,render_template,url_for
from app import mail
from .main.forms import mail_form
def send_mail(to, title, mes):
    msg = Message(title, sender='934998206@qq.com', recipients=[to])
    msg.body = mes
    mail.send(msg)
