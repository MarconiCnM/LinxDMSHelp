from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class FormCriaAtualiza(FlaskForm):
    diretorio = StringField('Insira o diretório a ser criado:')
    diretorioatualiza = StringField('Insira o diretório a ser atualizado:')
    versao = SelectField(u'Selecione a versão: ', choices=[('5.07'), ('5.06'), ('5.05'), ('5.04')])
    estrutura = SelectField(u'Selecione a estrutura: ', choices=[('2 Camadas'), ('3 Camadas')])
    programa = SelectField(u'Selecione o programa ', choices=[('Apollo'), ('Bravos'), ('Autoshop'), ('Toyota')])

    btn_submit_criar = SubmitField('Criar')
    btn_submit_atualizar = SubmitField('Atualizar')
