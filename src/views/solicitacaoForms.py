from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from models.models import HELPER
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed


class FormAlteracao(FlaskForm):
    nro_tp = IntegerField('Número da TP:', validators=[
        DataRequired(message='Digite apenas números:'), NumberRange(11111111, 99999999, message='O número informado não tem 8 digitos')])
    issue = StringField('ISSUE:')
    alt_cust = SelectField(u'Tipo: ', choices=[('Alt Complementar'), ('Man Evolutiva'), ('Customização')])
    fazendo = TextAreaField(
        'O que o sistema está fazendo:', validators=[DataRequired()])
    fazer = TextAreaField(
        'O que o sistema deveria fazer:', validators=[DataRequired()])
    como = TextAreaField(
        'Como deseja que o sistema faça:', validators=[DataRequired()])
    beneficio = TextAreaField(
        'Qual o beneficio dessa alteração:', validators=[DataRequired()])
    docs = FileField('Adicionar aquivos', validators=[FileAllowed(['zip'])])
    versao = SelectField(u'Versão:', choices=[('5.05'), ('5.06'), ('5.07')])
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

    helper = SelectField(u'Selecione o Helper *')
    btn_submit_encaminhar = SubmitField('Encaminhar')

    def __init__(self):
        super(FormAlteracao, self).__init__()
        self.helper.choices = [(h.USUARIO) for h in HELPER.query.all()]



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
    versao = SelectField(u'Versão', choices=[('5.05'), ('5.06'), ('5.07')])
    versao_ant = SelectField(u'Anterior:', choices=[('Sim'), ('Não')])
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

    helper = SelectField(u'Selecione o Helper *')
    btn_submit_encaminhar = SubmitField('Encaminhar')

    def __init__(self):
        super(FormErro, self).__init__()
        self.helper.choices = [(h.USUARIO) for h in HELPER.query.all()]

class FormServico(FlaskForm):
    nro_tp = IntegerField('Número da TP:', validators=[
        DataRequired(message='Digite apenas números:'), NumberRange(11111111, 99999999, message='O número informado não tem 8 digitos')])
    franqueado = StringField('Franqueado:')
    descricao = TextAreaField(
        'Descreva a solicitação do cliente:', validators=[DataRequired()])
    analise = TextAreaField(
        'O que foi passado de manual e informações ao cliente:', validators=[DataRequired()])
    solucao = TextAreaField(
        'Resolução:')

    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_iniciar = SubmitField('Iniciar Analise')
    btn_submit_info = SubmitField('Solicitar Informação')
    btn_submit_infores = SubmitField('Enviar Informação')
    btn_submit_recus = SubmitField('Recusar')
    btn_submit_final = SubmitField('Finalizar')

    helper = SelectField(u'Selecione o Helper *')
    btn_submit_encaminhar = SubmitField('Encaminhar')

    def __init__(self):
        super(FormServico, self).__init__()
        self.helper.choices = [(h.USUARIO) for h in HELPER.query.all()]

class FormComp(FlaskForm):
    nro_tp = IntegerField('Número da TP:', validators=[
        DataRequired(message='Digite apenas números'), NumberRange(11111111, 99999999, message='O número informado não tem 8 digitos')])
    issue = StringField('ISSUE:')
    grupo = StringField('Grupo:', validators=[DataRequired()])
    oque = TextAreaField(
        'O que o scrip faz:', validators=[DataRequired()])
    porque = TextAreaField(
        'Qual o motivo de não conseguirmos fazer pelo sistema:', validators=[DataRequired()])
    script = FileField('Adicionar aquivos', validators=[FileAllowed(['zip'])])
    solucao = TextAreaField(
        'Resolução:')

    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_iniciar = SubmitField('Iniciar Analise')
    btn_submit_info = SubmitField('Solicitar Informação')
    btn_submit_infores = SubmitField('Enviar Informação')
    btn_submit_aprov = SubmitField('Em compilação')
    btn_submit_recus = SubmitField('Recusar')
    btn_submit_final = SubmitField('Finalizar')

    helper = SelectField(u'Selecione o Helper *')
    btn_submit_encaminhar = SubmitField('Encaminhar')

    def __init__(self):
        super(FormComp, self).__init__()
        self.helper.choices = [(h.USUARIO) for h in HELPER.query.all()]


class FormImport(FlaskForm):
    nro_tp = IntegerField('Número da TP:', validators=[
        DataRequired(message='Digite apenas números'), NumberRange(11111111, 99999999, message='O número informado não tem 8 digitos')])
    issue = StringField('ISSUE:')
    grupo = StringField('Grupo:', validators=[DataRequired()])
    schema = StringField('Schema:')
    tamanho = IntegerField('Tamanho:', validators=[DataRequired()])
    servidor = SelectField(u'Selecione o servidor *', choices=[
        ('POA - POADSKFS044947'), ('BH - BHDSKFS0007909')])
    link = StringField('Local onde o backup está:', validators=[DataRequired()])
    observacao = TextAreaField(
        'Observação:')
    solucao = TextAreaField(
        'Resolução:')

    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_iniciar = SubmitField('Iniciar Importação')
    btn_submit_info = SubmitField('Solicitar Informação')
    btn_submit_infores = SubmitField('Enviar Informação')
    btn_submit_recus = SubmitField('Recusar')
    btn_submit_final = SubmitField('Finalizar')

    helper = SelectField(u'Selecione o Helper *')
    btn_submit_encaminhar = SubmitField('Encaminhar')

    def __init__(self):
        super(FormImport, self).__init__()
        self.helper.choices = [(h.USUARIO) for h in HELPER.query.all()]


class FormShare(FlaskForm):
    titulo = StringField('Titulo:', validators=[DataRequired()])
    produto = StringField('Produto:', validators=[DataRequired()])
    modulo = StringField('Modulo:', validators=[DataRequired()])
    finalidade = TextAreaField('Finaliade:', validators=[DataRequired()])
    link = StringField('Link:', validators=[DataRequired()])
    solucao = TextAreaField(
        'Resolução:')

    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_iniciar = SubmitField('Iniciar Analise')
    btn_submit_info = SubmitField('Solicitar Informação')
    btn_submit_infores = SubmitField('Enviar Informação')
    btn_submit_recus = SubmitField('Recusar')
    btn_submit_final = SubmitField('Finalizar')

    helper = SelectField(u'Selecione o Helper *')
    btn_submit_encaminhar = SubmitField('Encaminhar')

    def __init__(self):
        super(FormShare, self).__init__()
        self.helper.choices = [(h.USUARIO) for h in HELPER.query.all()]


class FormHelp(FlaskForm):
    nro_tp = IntegerField('Número da TP:', validators=[
        DataRequired(message='Digite apenas números'), NumberRange(11111111, 99999999, message='O número informado não tem 8 digitos')])
    menu_dir = StringField('Caminho do Menu:', validators=[DataRequired()])
    menu_cod = IntegerField('Código do Menu:', validators=[
                            DataRequired(message='Digite apenas números')])
    problema = TextAreaField(
        'Descreva a Solicitação/Problema:', validators=[DataRequired()])
    analisado = TextAreaField(
        'O que foi verificado:', validators=[DataRequired()])
    duvida = TextAreaField(
        'O que precisa que o Helper virifique:', validators=[DataRequired()])
    paliativa = TextAreaField(
        'Paliativa:', validators=[DataRequired()])
    docs = FileField('Adicionar aquivos', validators=[FileAllowed(['zip'])])
    db_teste = StringField('Banco de dados:', validators=[DataRequired()])
    versao = SelectField(u'Versão', choices=[('5.05'), ('5.06'), ('5.07')])
    solucao = TextAreaField(
        'Resolução:')
    
    btn_submit_inserir = SubmitField('Inserir')
    btn_submit_salvar = SubmitField('Salvar')
    btn_submit_iniciar = SubmitField('Iniciar Analise')
    btn_submit_info = SubmitField('Solicitar Informação')
    btn_submit_infores = SubmitField('Enviar Informação')
    btn_submit_aprov = SubmitField('Finalizar')
    btn_submit_recus = SubmitField('Cancelar')
    btn_submit_final = SubmitField('Finalizar')

    helper = SelectField(u'Selecione o Helper *')
    btn_submit_encaminhar = SubmitField('Encaminhar')

    def __init__(self):
        super(FormHelp, self).__init__()
        self.helper.choices = [(h.USUARIO) for h in HELPER.query.all()]

