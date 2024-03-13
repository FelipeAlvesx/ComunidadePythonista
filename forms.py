from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class CriarConta(FlaskForm):

    username = StringField("Nome de Usuario", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    password_confirm = PasswordField("Confirmação da senha", validators=[DataRequired(), EqualTo('password')])
    submit_button = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail Ja Cadastrado")


class Login(FlaskForm):

    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    remember_data = BooleanField("Lembre-se de mim")
    submit_button_login = SubmitField("Log in")


class EditarPerfil(FlaskForm):
    username = StringField("Nome de Usuario", validators=[DataRequired()])
    email = StringField("E-mail de Usuario", validators=[DataRequired(), Email()])
    foto_perfil = FileField("Atualizar Foto de Perfil  ", validators=[FileAllowed(["jpg", "png"])])
    curso_python = BooleanField("Formação Em Python")
    curso_sql = BooleanField("Formação Em SQL")
    curso_vba = BooleanField("Formação Em Django")
    curso_javascript = BooleanField("Formação Em Django Rest")
    curso_excel = BooleanField("Formação Em Flask")
    curso_powerbi = BooleanField("Formação Em Pandas")
    button_editar_perfil = SubmitField("Editar Perfil")

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("E-mail Ja Cadastrado")

    
class FormCriarPost(FlaskForm):
    title = StringField("Titulo do Post", validators=[DataRequired(), Length(2, 140)])
    body = TextAreaField("Escreva seu Post Aqui", validators=[DataRequired()])
    button_submit = SubmitField("Criar Post")



class FormEditarPost(FlaskForm):
    title = StringField("Novo Titulo", validators=[DataRequired(), Length(2, 140)])
    body = TextAreaField("Edite seu Post", validators=[DataRequired()])
    button_submit = SubmitField("Confirmar Edição")