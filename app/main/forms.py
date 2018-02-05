#coding:utf8
from flask_wtf import FlaskForm as Form
from wtforms import StringField,SubmitField , TextAreaField,PasswordField ,BooleanField,SelectField
from wtforms.validators import DataRequired,Email,InputRequired
from flask_pagedown.fields import PageDownField#和表格一样用就好
class NameForm(Form):
    name = StringField('Your name',validators= [DataRequired])
    submit = SubmitField('Submit')

class mail_form(Form):
    re = StringField('to', validators=[DataRequired])
    title = StringField('title', validators=[DataRequired])
    text = TextAreaField('message:',validators=[DataRequired])
    submit = SubmitField('Submit')

class PostForm(Form):

    title = StringField('title',validators=[InputRequired()])
    body = PageDownField('What \'s your mind?',validators=[DataRequired])
    post_type = StringField('tag', validators=[InputRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    about_me = TextAreaField('about me')
    location = StringField('location')
    submit = SubmitField('Submit')

class CommentForm(Form):
    body = PageDownField('What \'s your mind?',validators=[DataRequired])
    submit = SubmitField('Submit')

class TodoForm(Form):
    task = TextAreaField('What to do?')
    submit = SubmitField('Submit')