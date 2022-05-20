from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from models.models import GESTOR, HELPER, TIME, CARGO
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed


class FormAlteracao(FlaskForm):
    nro_tp = IntegerField('Número da TP:', validators=[
        DataRequired(message='Digite apenas números'), NumberRange(11111111, 99999999, message='O número informado não tem 8 digitos')])
    issue = StringField('ISSUE:')
    alt_cust = SelectField(u'Tipo: ', choices=[('Alteção complementar'), ('Manutenção evolutiva'), ('Customização')])
    menu_dir = StringField('Caminho do Menu:', validators=[DataRequired()])
    menu_cod = IntegerField('Código do Menu:', validators=[
                            DataRequired(message='Digite apenas números')])
    fazendo = TextAreaField(
        'O que o sistema está fazendo:', validators=[DataRequired()])
    fazer = TextAreaField(
        'O que o sistema deveria fazer:', validators=[DataRequired()])
    como = TextAreaField(
        'Como deseja que o sistema faça:', validators=[DataRequired()])
    paliativa = TextAreaField(
        'Paliativa:', validators=[DataRequired()])
    docs = FileField('Adicionar aquivos', validators=[DataRequired(),
                                             FileAllowed(['zip'])])
    db_teste = StringField('Banco de dados:', validators=[DataRequired()])
    versao = SelectField(u'Versão', choices=[('5.02'), ('5.03'), ('5.04'), ('5.05')])

    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_inserir = SubmitField('Inserir')

class FormErro(FlaskForm):
    nro_tp = IntegerField('Número da TP:', validators=[
        DataRequired(message='Digite apenas números'), NumberRange(11111111, 99999999, message='O número informado não tem 8 digitos')])
    issue = StringField('ISSUE:')
    menu_dir = StringField('Caminho do Menu:', validators=[DataRequired()])
    menu_cod = IntegerField('Código do Menu:', validators=[
                            DataRequired(message='Digite apenas números')])
    fazendo = TextAreaField(
        'O que o sistema está fazendo:', validators=[DataRequired()])
    fazer = TextAreaField(
        'O que o sistema deveria fazer:', validators=[DataRequired()])
    paliativa = TextAreaField(
        'Paliativa:', validators=[DataRequired()])
    docs = FileField('Adicionar aquivos', validators=[FileAllowed(['zip'])])
    db_teste = StringField('Banco de dados:', validators=[DataRequired()])
    versao = SelectField(u'Versão', choices=[('5.04'), ('5.05'), ('5.06'), ('5.07')])
    versao_ant = SelectField(u'Versão', choices=[('Sim'), ('Não')])
    solucao = TextAreaField(
        'Resolução:')
    
    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_iniciar = SubmitField('Iniciar Analise')
    btn_submit_info = SubmitField('Solicitar Informação')
    btn_submit_infores = SubmitField('Enviar Informação')
    btn_submit_aprov = SubmitField('Aprovar Abertura')
    btn_submit_recus = SubmitField('Recusar Abertura')
    btn_submit_rotulo = SubmitField('Solicita Rotulo')
    btn_submit_final = SubmitField('Finalizar')

