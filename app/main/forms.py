from flask_wtf import Form
from wtforms import StringField,SubmitField , TextAreaField,PasswordField ,BooleanField
from wtforms.validators import DataRequired,Email
class NameForm(Form):
    name = StringField('Your name',validators= [DataRequired])
    submit = SubmitField('Submit')

class mail_form(Form):
    re = StringField('to', validators=[DataRequired])
    title = StringField('title', validators=[DataRequired])
    text = TextAreaField('message:',validators=[DataRequired])
    submit = SubmitField('Submit')

class PostForm(Form):
    body = TextAreaField('What \'s your mind?',validators=[DataRequired])
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    about_me = TextAreaField('about me')
    location = StringField('location')
    submit = SubmitField('Submit')
