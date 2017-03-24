from flask_wtf import Form
from wtforms import StringField,SubmitField , TextAreaField,PasswordField ,BooleanField
from wtforms.validators import DataRequired,Email
class LoginForm(Form):
    email = StringField('Email',validators= [DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    remember = BooleanField('remember me')
    submit = SubmitField('Submit')

class RegisterForm(Form):
    name = StringField('Name',validators= [DataRequired])
    email = StringField('Email',validators= [Email()])
    password = PasswordField('Password',validators= [DataRequired])
    password_ = PasswordField('Confirmed Password', validators=[DataRequired])
    submit = SubmitField('Submit')