from flask import flash
from flask_login import login_user, current_user
from models.models import GESTOR, HELPER, BASES, CARGO, TIME, ANALISTA
from app import database, bcrypt
def authLogin(form_login):
    if form_login.validate_on_submit():
        gestor = GESTOR.query.filter_by(EMAIL=form_login.email.data).first()
        helper = HELPER.query.filter_by(EMAIL=form_login.email.data).first()
        analista = ANALISTA.query.filter_by(EMAIL=form_login.email.data).first()

        if gestor and bcrypt.check_password_hash(gestor.SENHA, form_login.password.data):
            login_user(gestor, remember=form_login.remmember.data)
            flash('Login feito com sucesso', 'alert-success')
            return True
        elif helper and bcrypt.check_password_hash(helper.SENHA, form_login.password.data):
            login_user(helper, remember=form_login.remmember.data)
            flash('Login feito com sucesso', 'alert-success')
            return True
        elif analista and bcrypt.check_password_hash(analista.SENHA, form_login.password.data):
            login_user(analista, remember=form_login.remmember.data)
            flash('Login feito com sucesso', 'alert-success')
            return True
        else:
            flash('Falha no login. e-mail ou senha incorretos', 'alert-danger')

def tpsAnalistas():
    analista = str.title(current_user.EMAIL.replace('.', ' ').split('@')[0])
    tpsgerais = database.session.execute("SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA = '{analista}' " + 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsmais15 = database.session.execute(f"SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA = '{analista}' " + 
                    "AND DIAS_ABERTO > 14 "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsbacklog = database.session.execute(f"SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA = '{analista}' " + 
                    "AND DTA_FIM < GETDATE() "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    return tpsgerais, tpsmais15, tpsbacklog

def tpsTimeHelper():
    lista_analista = ""
    analista = database.session.execute("SELECT id, USUARIO " + 
                    "FROM ANALISTA " + 
                    F"WHERE TIME_ID = (SELECT ID FROM TIME WHERE HELPER_ID = '{current_user.id}') ").fetchall()
    for i in analista:
        lista_analista += "'" + i[1] + "',"
    
    tpsanaliticotot = database.session.execute("SELECT grl.ANALISTA, " +
                    "COUNT(grl.NRO_TP) AS FILA, " +
                    "(SELECT COUNT(m15.NRO_TP) " +
                        "FROM CONTROLE_TPS_ANALISTAS m15 " +
                        "WHERE m15.ANALISTA = grl.ANALISTA " +
                        "AND m15.DIAS_ABERTO >= 15) as MAIS15, " +
                    "(SELECT COUNT(m15.NRO_TP) " +
                        "FROM CONTROLE_TPS_ANALISTAS m15 " +
                        "WHERE m15.ANALISTA = grl.ANALISTA " +
                        "AND m15.DTA_FIM < getdate()) as BACKLOG " +
                    "FROM CONTROLE_TPS_ANALISTAS grl " +
                    f"WHERE grl.ANALISTA IN ({lista_analista[:-1]}) " +
                    "GROUP BY grl.ANALISTA").fetchall()

    tpsgerais = database.session.execute("SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsmais15 = database.session.execute(f"SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DIAS_ABERTO > 14 "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsbacklog = database.session.execute(f"SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DTA_FIM < GETDATE() "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    return tpsgerais, tpsmais15, tpsbacklog, tpsanaliticotot

def tpsTimeGestor():
    lista_analista = ""
    analista = database.session.execute("SELECT id, USUARIO " + 
                    "FROM ANALISTA " + 
                    F"WHERE TIME_ID in (SELECT ID FROM TIME WHERE GESTOR_ID = '{current_user.id}') ").fetchall()
    for i in analista:
        lista_analista += "'" + i[1] + "',"
    
    tpsanaliticotot = database.session.execute("SELECT grl.ANALISTA, " +
                "COUNT(grl.NRO_TP) AS FILA, " +
                "(SELECT COUNT(m15.NRO_TP) " +
                    "FROM CONTROLE_TPS_ANALISTAS m15 " +
                    "WHERE m15.ANALISTA = grl.ANALISTA " +
                    "AND m15.DIAS_ABERTO >= 15) as MAIS15, " +
                "(SELECT COUNT(m15.NRO_TP) " +
                    "FROM CONTROLE_TPS_ANALISTAS m15 " +
                    "WHERE m15.ANALISTA = grl.ANALISTA " +
                    "AND m15.DTA_FIM < getdate()) as BACKLOG " +
                "FROM CONTROLE_TPS_ANALISTAS grl " +
                f"WHERE grl.ANALISTA IN ({lista_analista[:-1]}) " +
                "GROUP BY grl.ANALISTA").fetchall()

    tpsgerais = database.session.execute("SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsmais15 = database.session.execute(f"SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DIAS_ABERTO > 14 "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsbacklog = database.session.execute(f"SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DTA_FIM < GETDATE() "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    return tpsgerais, tpsmais15, tpsbacklog, tpsanaliticotot

def tpsTimeCoordenador():
    lista_analista = ""
    analista = database.session.execute("SELECT id, USUARIO " + 
                    "FROM ANALISTA").fetchall()
    for i in analista:
        lista_analista += "'" + i[1] + "',"

    tpsanaliticotot = database.session.execute("SELECT grl.ANALISTA, " +
            "COUNT(grl.NRO_TP) AS FILA, " +
            "(SELECT COUNT(m15.NRO_TP) " +
                "FROM CONTROLE_TPS_ANALISTAS m15 " +
                "WHERE m15.ANALISTA = grl.ANALISTA " +
                "AND m15.DIAS_ABERTO >= 15) as MAIS15, " +
            "(SELECT COUNT(m15.NRO_TP) " +
                "FROM CONTROLE_TPS_ANALISTAS m15 " +
                "WHERE m15.ANALISTA = grl.ANALISTA " +
                "AND m15.DTA_FIM < getdate()) as BACKLOG " +
            "FROM CONTROLE_TPS_ANALISTAS grl " +
            f"WHERE grl.ANALISTA IN ({lista_analista[:-1]}) " +
            "GROUP BY grl.ANALISTA").fetchall()
    tpsgerais = database.session.execute("SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsmais15 = database.session.execute(f"SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DIAS_ABERTO > 14 "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsbacklog = database.session.execute(f"SELECT id, NRO_TP, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DTA_FIM < GETDATE() "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    return tpsgerais, tpsmais15, tpsbacklog, tpsanaliticotot
