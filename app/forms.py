from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    IntegerField,
)
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')


class FilterForm(FlaskForm):
    type = SelectField(
        'Type',
        choices=[
            ('', 'All'),
            ('recreational', 'Recreational'),
            ('social', 'Social'),
            ('diy', 'DIY'),
            ('education', 'Education'),
            ('charity', 'Charity'),
            ('cooking', 'Cooking'),
            ('relaxation', 'Relaxation'),
            ('music', 'Music'),
            ('busywork', 'Busywork'),
        ],
    )
    participants = IntegerField('Participants', default=1)
    submit = SubmitField('Get Activity')
