from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class CadastroForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])

class postarForm(Form):
   content = TextAreaField("content" ,validators=[DataRequired()])
   user_id = IntegerField("user_id",validators=[DataRequired()])