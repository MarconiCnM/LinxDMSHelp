from app import database, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_username(id_username):
    gestor = GESTOR.query.get(int(id_username))
    helper = HELPER.query.get(int(id_username))
    analista = ANALISTA.query.get(int(id_username))
    if gestor:
        return gestor
    elif helper:
        return helper
    elif analista:
        return analista

    
class TIME(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    CODIGO = database.Column(database.Integer, nullable=False)
    NOME = database.Column(database.String, nullable=False)
    GESTOR_ID = database.Column(
        database.Integer, database.ForeignKey('GESTOR.id'))
    HELPER_ID = database.Column(
        database.Integer, database.ForeignKey('HELPER.id'))
    ANALISTAS = database.relationship('ANALISTA', backref='time')

class CARGO(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    CODIGO = database.Column(database.Integer, nullable=False)
    CARGO = database.Column(database.String, nullable=False)
    META = database.Column(database.String, nullable=False)
    ANALISTAS = database.relationship('ANALISTA', backref='grupo')

class ANALISTA(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    USUARIO = database.Column(database.String, nullable=False)
    EMAIL = database.Column(database.String, nullable=False)
    SENHA = database.Column(database.String, nullable=False)
    CARGO_ID = database.Column(
        database.Integer, database.ForeignKey('CARGO.id'))
    TIME_ID = database.Column(
        database.Integer, database.ForeignKey('TIME.id'))
    SOL_ERRO = database.relationship('SOL_ERRO', backref='requester')
    SOL_SERVICO = database.relationship('SOL_SERVICO', backref='requester')
    SOL_SCRIPT = database.relationship('SOL_SCRIPT', backref='requester')
    SOL_IMPORT = database.relationship('SOL_IMPORT', backref='requester')
    SOL_SHARE = database.relationship('SOL_SHARE', backref='requester')
    SOL_HISTORIA = database.relationship(
        'SOL_HISTORIA', backref='requester')
    HELP = database.relationship(
        'HELP', backref='requester')
    TIPO = database.Column(database.String, default='A')

class HELPER(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    USUARIO = database.Column(database.String, nullable=False)
    EMAIL = database.Column(database.String, nullable=False)
    SENHA = database.Column(database.String, nullable=False)
    LIDER = database.Column(database.String, nullable=False, default='N')
    TIME = database.relationship('TIME', backref='HELP')
    SOL_ERRO = database.relationship('SOL_ERRO', backref='finisher')
    SOL_SERVICO = database.relationship('SOL_SERVICO', backref='finisher')
    SOL_SCRIPT = database.relationship('SOL_SCRIPT', backref='finisher')
    SOL_IMPORT = database.relationship('SOL_IMPORT', backref='finisher')
    SOL_SHARE = database.relationship('SOL_SHARE', backref='finisher')
    SOL_HISTORIA = database.relationship(
        'SOL_HISTORIA', backref='finisher')
    HELP = database.relationship(
        'HELP', backref='finisher')
    TIPO = database.Column(database.String, default='H')
    

class GESTOR(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    USUARIO = database.Column(database.String, nullable=False)
    EMAIL = database.Column(database.String, nullable=False)
    SENHA = database.Column(database.String, nullable=False)
    TIME = database.relationship('TIME', backref='GESTAO')
    TIPO = database.Column(database.String, default='G')


class SOL_ERRO(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    NRO_TP = database.Column(database.Integer, nullable=False)
    ISSUE = database.Column(database.String)
    CAMINHO_MENU = database.Column(database.String, nullable=False)
    CODIGO_MENU = database.Column(database.Integer, nullable=False)
    FAZENDO = database.Column(database.Text, nullable=False)
    FAZER = database.Column(database.Text, nullable=False)
    PALIATIVA = database.Column(database.Text, nullable=False, default='N/A')
    DOCS = database.Column(database.Text, nullable=False)
    BANCO = database.Column(database.String, nullable=False)
    VERSAO = database.Column(database.String, nullable=False)
    VERSAO_ANT = database.Column(database.String, nullable=False)
    SOLUCAO = database.Column(database.Text)
    STATUS = database.Column(database.String, nullable=False, default='NÃO INICIADO')
    ANALISTA_ID = database.Column(
        database.Integer, database.ForeignKey('ANALISTA.id'), nullable=False)
    HELPER_ID = database.Column(
        database.Integer, database.ForeignKey('HELPER.id'))
    DTA_CREATE = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow)
    DTA_CONCLUDED = database.Column(database.DateTime)

class SOL_SERVICO(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    NRO_TP = database.Column(database.Integer, nullable=False)
    FRANQUEADO = database.Column(database.String, nullable=False)
    DESC = database.Column(database.Text, nullable=False)
    ANALISE = database.Column(database.Text, nullable=False)
    SOLUCAO = database.Column(database.Text)
    STATUS = database.Column(database.String, nullable=False, default='NÃO INICIADO')
    ANALISTA_ID = database.Column(
        database.Integer, database.ForeignKey('ANALISTA.id'), nullable=False)
    HELPER_ID = database.Column(
        database.Integer, database.ForeignKey('HELPER.id'))
    DTA_CREATE = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow)
    DTA_CONCLUDED = database.Column(database.DateTime)

class SOL_SCRIPT(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    NRO_TP = database.Column(database.Integer, nullable=False)
    ISSUE = database.Column(database.String)
    GRUPO = database.Column(database.String, nullable=False)
    OQUE = database.Column(database.Text, nullable=False)
    PORQUE = database.Column(database.Text, nullable=False)
    SCRIPT = database.Column(database.Text, nullable=False)
    SOLUCAO = database.Column(database.Text)
    STATUS = database.Column(database.String, nullable=False, default='NÃO INICIADO')
    ANALISTA_ID = database.Column(
        database.Integer, database.ForeignKey('ANALISTA.id'), nullable=False)
    HELPER_ID = database.Column(
        database.Integer, database.ForeignKey('HELPER.id'))
    DTA_CREATE = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow)
    DTA_CONCLUDED = database.Column(database.DateTime)

class SOL_IMPORT(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    NRO_TP = database.Column(database.Integer, nullable=False)
    GRUPO = database.Column(database.String, nullable=False)
    ISSUE = database.Column(database.String)
    SCHEMA = database.Column(database.String)
    TAMANHO = database.Column(database.String, nullable=False)
    SERVIDOR = database.Column(database.String, nullable=False)
    DIR_ARQ = database.Column(database.Text, nullable=False)
    OBS = database.Column(database.Text)
    SOLUCAO = database.Column(database.Text)
    STATUS = database.Column(database.String, nullable=False, default='NÃO INICIADO')
    ANALISTA_ID = database.Column(
        database.Integer, database.ForeignKey('ANALISTA.id'), nullable=False)
    HELPER_ID = database.Column(
        database.Integer, database.ForeignKey('HELPER.id'))
    DTA_CREATE = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow)
    DTA_CONCLUDED = database.Column(database.DateTime)

class SOL_SHARE(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    TITULO = database.Column(database.String, nullable=False)
    PRODUTO = database.Column(database.String, nullable=False)
    MODULO = database.Column(database.String, nullable=False)
    FINALIDADE = database.Column(database.Text, nullable=False)
    LINK = database.Column(database.Text, nullable=False)
    SOLUCAO = database.Column(database.Text)
    STATUS = database.Column(database.String, nullable=False, default='NÃO INICIADO')
    ANALISTA_ID = database.Column(
        database.Integer, database.ForeignKey('ANALISTA.id'), nullable=False)
    HELPER_ID = database.Column(
        database.Integer, database.ForeignKey('HELPER.id'))
    DTA_CREATE = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow)
    DTA_CONCLUDED = database.Column(database.DateTime)

class SOL_HISTORIA(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    NRO_TP = database.Column(database.Integer, nullable=False)
    ISSUE = database.Column(database.String)
    FAZENDO = database.Column(database.Text, nullable=False)
    FAZER = database.Column(database.Text, nullable=False)
    COMO = database.Column(database.Text, nullable=False)
    BENEFICIO = database.Column(database.Text, nullable=False)
    VERSAO = database.Column(database.String, nullable=False)
    DOCS = database.Column(database.Text, nullable=False)
    ALT_CUST = database.Column(database.Text, nullable=False)
    SOLUCAO = database.Column(database.Text)
    STATUS = database.Column(database.String, nullable=False, default='NÃO INICIADO')
    ANALISTA_ID = database.Column(
        database.Integer, database.ForeignKey('ANALISTA.id'), nullable=False)
    HELPER_ID = database.Column(
        database.Integer, database.ForeignKey('HELPER.id'))
    DTA_CREATE = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow)
    DTA_CONCLUDED = database.Column(database.DateTime)


class HELP(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    NRO_TP = database.Column(database.Integer, nullable=False)
    CAMINHO_MENU = database.Column(database.String, nullable=False)
    CODIGO_MENU = database.Column(database.Integer, nullable=False)
    PROBLEMA = database.Column(database.Text, nullable=False)
    ANALISADO = database.Column(database.Text, nullable=False)
    DUVIDA = database.Column(database.Text, nullable=False)
    PALIATIVA = database.Column(database.Text, nullable=False, default='N/A')
    DOCS = database.Column(database.Text, nullable=False)
    BANCO = database.Column(database.String, nullable=False)
    VERSAO = database.Column(database.String, nullable=False)
    SOLUCAO = database.Column(database.Text)
    STATUS = database.Column(database.String, nullable=False, default='NÃO INICIADO')
    ANALISTA_ID = database.Column(
        database.Integer, database.ForeignKey('ANALISTA.id'), nullable=False)
    HELPER_ID = database.Column(
        database.Integer, database.ForeignKey('HELPER.id'))
    DTA_CREATE = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow)
    DTA_CONCLUDED = database.Column(database.DateTime)

class BASES(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    CODIGO = database.Column(database.Integer, nullable=False)
    CLIENTE = database.Column(database.String, nullable=False)
    CHARSET = database.Column(database.String)
    SERVIDOR = database.Column(database.String, nullable=False)
    ESTRUTURA = database.Column(database.String, nullable=False)
    INSTANCIA = database.Column(database.String)
    USUARIO = database.Column(database.String)
    MARCA = database.Column(database.String, nullable=False)
    TAMANHO = database.Column(database.Integer, nullable=False)

class MOV_SOL(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    NRO_TP = database.Column(database.Integer, nullable=False)
    TITULO = database.Column(database.String, nullable=False)
    TIPO = database.Column(database.String, nullable=False)
    HELPER = database.Column(database.String, nullable=False)
    ANALISTA = database.Column(database.String, nullable=False)
    RESUMO = database.Column(database.Text, nullable=False)
    STATUS = database.Column(database.Text, nullable=False)
    DTA_CREATE = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow)

class CONTROLE_TPS_ANALISTAS(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    NRO_TP = database.Column(database.Integer, unique=True)
    ISSUE = database.Column(database.String)
    ANALISTA = database.Column(database.String, nullable=False)
    GRUPO = database.Column(database.String, nullable=False)
    RESUMO = database.Column(database.String, nullable=False)
    DIAS_ABERTO = database.Column(database.Integer, nullable=False)
    DTA_FIM = database.Column(
        database.DateTime)
    DTA_ULT_MOV = database.Column(
        database.DateTime, default=datetime.utcnow)
    STATUS = database.Column(database.String, nullable=False)
    PRIORIDADE = database.Column(database.String, nullable=False)

class CONTROLE_TPS_GERAIS(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    APOLLO_tot = database.Column(database.String, nullable=False)
    APOLLO_p0 = database.Column(database.String, nullable=False)
    APOLLO_p1 = database.Column(database.String, nullable=False)
    APOLLO_p2 = database.Column(database.String, nullable=False)
    APOLLO_p3 = database.Column(database.String, nullable=False)
    BRAVOS_tot = database.Column(database.String, nullable=False)
    BRAVOS_p0 = database.Column(database.String, nullable=False)
    BRAVOS_p1 = database.Column(database.String, nullable=False)
    BRAVOS_p2 = database.Column(database.String, nullable=False)
    BRAVOS_p3 = database.Column(database.String, nullable=False)
    TOYOTA_tot = database.Column(database.String, nullable=False)
    TOYOTA_p0 = database.Column(database.String, nullable=False)
    TOYOTA_p1 = database.Column(database.String, nullable=False)
    TOYOTA_p2 = database.Column(database.String, nullable=False)
    TOYOTA_p3 = database.Column(database.String, nullable=False)
    AUTOSHOP_tot = database.Column(database.String, nullable=False)
    AUTOSHOP_p0 = database.Column(database.String, nullable=False)
    AUTOSHOP_p1 = database.Column(database.String, nullable=False)
    AUTOSHOP_p2 = database.Column(database.String, nullable=False)
    AUTOSHOP_p3 = database.Column(database.String, nullable=False)
    BERCARIO_tot = database.Column(database.String, nullable=False)
    BERCARIO_p0 = database.Column(database.String, nullable=False)
    BERCARIO_p1 = database.Column(database.String, nullable=False)
    BERCARIO_p2 = database.Column(database.String, nullable=False)
    BERCARIO_p3 = database.Column(database.String, nullable=False)
    FINANCEIRO_tot = database.Column(database.String, nullable=False)
    FINANCEIRO_p0 = database.Column(database.String, nullable=False)
    FINANCEIRO_p1 = database.Column(database.String, nullable=False)
    FINANCEIRO_p2 = database.Column(database.String, nullable=False)
    FINANCEIRO_p3 = database.Column(database.String, nullable=False)
    NFCE_tot = database.Column(database.String, nullable=False)
    NFCE_p0 = database.Column(database.String, nullable=False)
    NFCE_p1 = database.Column(database.String, nullable=False)
    NFCE_p2 = database.Column(database.String, nullable=False)
    NFCE_p3 = database.Column(database.String, nullable=False)
    MONTADORA_tot = database.Column(database.String, nullable=False)
    MONTADORA_p0 = database.Column(database.String, nullable=False)
    MONTADORA_p1 = database.Column(database.String, nullable=False)
    MONTADORA_p2 = database.Column(database.String, nullable=False)
    MONTADORA_p3 = database.Column(database.String, nullable=False)
    MOBILE_tot = database.Column(database.String, nullable=False)
    MOBILE_p0 = database.Column(database.String, nullable=False)
    MOBILE_p1 = database.Column(database.String, nullable=False)
    MOBILE_p2 = database.Column(database.String, nullable=False)
    MOBILE_p3 = database.Column(database.String, nullable=False)
    CONTABIL_tot = database.Column(database.String, nullable=False)
    CONTABIL_p0 = database.Column(database.String, nullable=False)
    CONTABIL_p1 = database.Column(database.String, nullable=False)
    CONTABIL_p2 = database.Column(database.String, nullable=False)
    CONTABIL_p3 = database.Column(database.String, nullable=False)
    CC1_tot = database.Column(database.String, nullable=False)
    CC1_p0 = database.Column(database.String, nullable=False)
    CC1_p1 = database.Column(database.String, nullable=False)
    CC1_p2 = database.Column(database.String, nullable=False)
    CC1_p3 = database.Column(database.String, nullable=False)
