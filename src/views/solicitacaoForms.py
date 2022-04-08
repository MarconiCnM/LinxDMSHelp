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
    docs = FileField('Adicionar aquivos', validators=[DataRequired(),
                                             FileAllowed(['zip'])])
    db_teste = StringField('Banco de dados:', validators=[DataRequired()])
    versao = SelectField(u'Versão', choices=[('5.02'), ('5.03'), ('5.04'), ('5.05')])
    versao_ant = SelectField(u'Versão', choices=[('Sim'), ('Não')])
    
    btn_submit_inserir = SubmitField('Inserir')