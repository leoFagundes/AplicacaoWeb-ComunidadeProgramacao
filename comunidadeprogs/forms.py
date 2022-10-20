#instalar o falsk_wtf -> pip install flask-wtf
from platform import python_branch
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeprogs.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()]) #DataRequired -> obrigatório
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')


    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Eita dev, nome já cadastrado. Cadastre-se com outro nome ou faça login para continuar')


    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Eita dev, e-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')
        

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()]) #DataRequired -> obrigatório
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'gif', 'svg'])])

    linguagem_python = BooleanField('Python')
    linguagem_cplus = BooleanField('c++')
    linguagem_csharp = BooleanField('c#')
    linguagem_java = BooleanField('Java')
    linguagem_sql = BooleanField('SQL')
    linguagem_javascript = BooleanField('JavaScript')
    linguagem_r = BooleanField('R')
    linguagem_htmlcss = BooleanField('HTML/CSS')
    linguagem_typescript = BooleanField('TypeScript')
    linguagem_php = BooleanField('PHP')
    linguagem_shell = BooleanField('Shell')
    linguagem_ruby = BooleanField('Ruby')
    linguagem_assembly = BooleanField('Assembly')
    linguagem_swift = BooleanField('Swift')
    linguagem_go = BooleanField('Go')

    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        #verificar se ele mudou de email
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')