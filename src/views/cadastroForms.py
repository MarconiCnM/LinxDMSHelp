from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, IntegerField
from models.models import GESTOR, HELPER, TIME, CARGO
from wtforms.validators import DataRequired, Email, Length, EqualTo

class FormCadGestor(FlaskForm):
    nome = StringField('Nome *',
                        validators=[DataRequired()])
    email = StringField('Endereço de e-mail *',
                        validators=[DataRequired(), Email()])
    senha = PasswordField(
        'Senha *')
    confirma_senha = PasswordField(
        'Confirme sua senha *', validators=[EqualTo('senha')])
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_redirect = SubmitField('Inserir')
    btn_submit_excluir = SubmitField('Excluir')

class FormCadHelper(FlaskForm):
    nome = StringField('Nome *',
                        validators=[DataRequired()])
    email = StringField('Endereço de e-mail *',
                        validators=[DataRequired(), Email()])
    senha = PasswordField(
        'Senha *')
    confirma_senha = PasswordField(
        'Confirme sua senha *', validators=[EqualTo('senha')])
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_redirect = SubmitField('Inserir')
    btn_submit_excluir = SubmitField('Excluir')

class FormCadBase(FlaskForm):
    codigo = IntegerField('Codigo', validators=[DataRequired()])
    cliente = StringField('Informe o cliente *',
                        validators=[DataRequired()])
    servidor = SelectField(u'Selecione o servidor *', choices=[
        ('POA - POADSKFS044947'), ('BH - BHDSKFS0007909')])
    estrutura = SelectField(u'Selecione a estrutura *', choices=[
        ('Oracle'), ('SQLServer')])
    instancia = StringField('Informe a instancia')
    usuario = StringField('Informe o usuario')
    marca = StringField('Informe as marcas *',
                        validators=[DataRequired()])
    tamanho = IntegerField('Informe o tamanho *',
                        validators=[DataRequired()])
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_redirect = SubmitField('Inserir')
    btn_submit_excluir = SubmitField('Excluir')

class FormCadCargo(FlaskForm):
    codigo = IntegerField('Codigo *',
                        validators=[DataRequired()])
    cargo = SelectField(u'Selecione o cargo *', choices=[
        ('Analista Jr I'), ('Analista Jr II'), ('Analista Pl I'), ('Analista Pl II'), ('Analista Sr I'), ('Analista Sr II'), ('Especialista I'), ('Especialista II'), ('Lider Tecnico')])
    metas = StringField('Meta diaria *',
                        validators=[DataRequired()])
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_redirect = SubmitField('Inserir')
    btn_submit_excluir = SubmitField('Excluir')


class FormCadTime(FlaskForm):
    codigo = IntegerField('Codigo *',
                        validators=[DataRequired()])
    nome = StringField('Nome do Time *',
                        validators=[DataRequired()])
    helper = SelectField(u'Selecione o Helper *')
    gestor = SelectField(u'Selecione o Gestor *')
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_redirect = SubmitField('Inserir')
    btn_submit_excluir = SubmitField('Excluir')

    def __init__(self):
        super(FormCadTime, self).__init__()
        self.helper.choices = [(h.USUARIO) for h in HELPER.query.all()]
        self.gestor.choices = [(g.USUARIO) for g in GESTOR.query.all()]

class FormCadAnalista(FlaskForm):
    nome = StringField('Nome *',
                        validators=[DataRequired()])
    email = StringField('Endereço de e-mail *',
                        validators=[DataRequired(), Email()])
    senha = PasswordField(
        'Senha *')
    confirma_senha = PasswordField(
        'Confirme sua senha *', validators=[EqualTo('senha')])
    cargo = SelectField(u'Selecione o Cargo *')
    time = SelectField(u'Selecione o Time *')
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_redirect = SubmitField('Inserir')
    btn_submit_excluir = SubmitField('Excluir')

    
    def __init__(self):
        super(FormCadAnalista, self).__init__()
        self.cargo.choices = [(h.CARGO) for h in CARGO.query.all()]
        self.time.choices = [(g.NOME) for g in TIME.query.all()]