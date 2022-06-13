from flask import flash
from flask_login import current_user
from app import database
from models.models import SOL_ERRO, SOL_HISTORIA, SOL_SERVICO, SOL_SCRIPT, SOL_IMPORT, SOL_SHARE, HELP, ANALISTA, TIME

def tpsAnalistas():
    analista = str.title(current_user.EMAIL.replace('.', ' ').split('@')[0])
    tpsgerais = database.session.execute("SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA = '{analista}' " + 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsmais15 = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA = '{analista}' " + 
                    "AND DIAS_ABERTO > 14 "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsbacklog = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA = '{analista}' " + 
                    "AND DTA_FIM < GETDATE() " 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    return tpsgerais, tpsmais15, tpsbacklog

def tpsTimeHelper():
    lista_analista = ""
    analista = database.session.execute("SELECT id, USUARIO " + 
                    "FROM ANALISTA " + 
                    F"WHERE TIME_ID in (SELECT ID FROM TIME WHERE HELPER_ID = '{current_user.id}') ").fetchall()
    for i in analista:
        lista_analista += "'" + i[1] + "',"

    lista_analista += f"'{current_user.USUARIO}'"
    
    tpsanaliticotot = database.session.execute("SELECT grl.ANALISTA, " +
                    "COUNT(grl.NRO_TP) AS FILA, " +
                    "(SELECT COUNT(m15.NRO_TP) " +
                        "FROM CONTROLE_TPS_ANALISTAS m15 " +
                        "WHERE m15.ANALISTA = grl.ANALISTA " +
                        "AND m15.DIAS_ABERTO >= 15) as MAIS15, " +
                    "(SELECT COUNT(m15.NRO_TP) " +
                        "FROM CONTROLE_TPS_ANALISTAS m15 " +
                        "WHERE m15.ANALISTA = grl.ANALISTA " +
                        "AND m15.ISSUE NOT LIKE '%AUTO%' " +
                        "AND m15.DTA_FIM < getdate()) as BACKLOG, " +
                    "(SELECT COUNT(m15.NRO_TP) " +
                        "FROM CONTROLE_TPS_ANALISTAS m15 " +
                        "WHERE m15.ANALISTA = grl.ANALISTA " +
                        "AND m15.ISSUE LIKE '%AUTO%') as ISSUE " +
                    "FROM CONTROLE_TPS_ANALISTAS grl " +
                    f"WHERE grl.ANALISTA IN ({lista_analista}) " +
                    "GROUP BY grl.ANALISTA").fetchall()

    tpsgerais = database.session.execute("SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista}) " + 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsmais15 = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista}) " + 
                    "AND DIAS_ABERTO > 14 "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsbacklog = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista}) " + 
                    "AND DTA_FIM < GETDATE() "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()

    tpsissue = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista}) " + 
                    "AND ISSUE LIKE '%AUTO%' "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()

    return tpsgerais, tpsmais15, tpsbacklog, tpsanaliticotot, tpsissue

def tpsTimeGestor():
    lista_analista = ""
    analista = database.session.execute("SELECT id, USUARIO " + 
                    "FROM ANALISTA " + 
                    F"WHERE TIME_ID in (SELECT ID FROM TIME WHERE GESTOR_ID = '{current_user.id}') ").fetchall()
    for i in analista:
        lista_analista += "'" + i[1] + "',"
    
    tpsanaliticotot = database.session.execute("SELECT (SELECT distinct usuario " +
        "FROM   analista " +
        "WHERE  usuario = grl.analista)               AS ANALISTA, " +
        "(SELECT nome " +
        "FROM   time " +
        "WHERE  id = (SELECT time_id " +
                     "FROM   analista " +
                     "WHERE  usuario = grl.analista)) AS EQUIPE, " +
        "Count(grl.nro_tp)                             AS FILA, " +
        "(SELECT Count(m15.nro_tp) " +
        "FROM   controle_tps_analistas m15 " +
        "WHERE  m15.analista = grl.analista " +
               "AND m15.dias_aberto >= 15)            AS MAIS15, " +
        "(SELECT Count(m15.nro_tp) " +
        "FROM   controle_tps_analistas m15 " +
        "WHERE  m15.analista = grl.analista " +
               "AND m15.ISSUE NOT LIKE '%AUTO%' " +
               "AND m15.dta_fim < Getdate())          AS BACKLOG, " +
        "(SELECT COUNT(m15.NRO_TP) " +
                        "FROM CONTROLE_TPS_ANALISTAS m15 " +
                        "WHERE m15.ANALISTA = grl.ANALISTA " +
                        "AND m15.ISSUE LIKE '%AUTO%') as ISSUE " +
        "FROM   controle_tps_analistas grl " +
        f"WHERE  grl.analista IN ({lista_analista[:-1]}) " +
        "GROUP  BY grl.analista; ").fetchall()
        

    tpsgerais = database.session.execute("SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsmais15 = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DIAS_ABERTO > 14 "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsbacklog = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DTA_FIM < GETDATE() "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()

    tpsissue = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND ISSUE LIKE '%AUTO%' "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()

    return tpsgerais, tpsmais15, tpsbacklog, tpsanaliticotot, tpsissue

def tpsTimeCoordenador():
    lista_analista = ""
    analista = database.session.execute("SELECT id, USUARIO " + 
                    "FROM ANALISTA").fetchall()
    for i in analista:
        lista_analista += "'" + i[1] + "',"

    tpsanaliticotot = database.session.execute("SELECT (SELECT usuario " +
        "FROM   analista " +
        "WHERE  usuario = grl.analista)               AS ANALISTA, " +
        "(SELECT nome " +
        "FROM   time " +
        "WHERE  id = (SELECT time_id " +
                     "FROM   analista " +
                     "WHERE  usuario = grl.analista)) AS EQUIPE, " +
        "Count(grl.nro_tp)                             AS FILA, " +
        "(SELECT Count(m15.nro_tp) " +
        "FROM   controle_tps_analistas m15 " +
        "WHERE  m15.analista = grl.analista " +
               "AND m15.dias_aberto >= 15)            AS MAIS15, " +
        "(SELECT Count(m15.nro_tp) " +
        "FROM   controle_tps_analistas m15 " +
        "WHERE  m15.analista = grl.analista " +
               "AND m15.ISSUE NOT LIKE '%AUTO%' " +
               "AND m15.dta_fim < Getdate())          AS BACKLOG, " +
        "(SELECT COUNT(m15.NRO_TP) " +
                        "FROM CONTROLE_TPS_ANALISTAS m15 " +
                        "WHERE m15.ANALISTA = grl.ANALISTA " +
                        "AND m15.ISSUE LIKE '%AUTO%') as ISSUE " +
        "FROM   controle_tps_analistas grl " +
        f"WHERE  grl.analista IN ({lista_analista[:-1]}) " +
        "GROUP  BY grl.analista; ").fetchall()
        
    tpsgerais = database.session.execute("SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsmais15 = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DIAS_ABERTO > 14 "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsbacklog = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND DTA_FIM < GETDATE() "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()
    tpsissue = database.session.execute(f"SELECT id, NRO_TP, ISSUE, ANALISTA, GRUPO, RESUMO, DIAS_ABERTO, DATEDIFF(day, DTA_ULT_MOV, getdate()) as DTA_ULT_MOV, DTA_FIM, STATUS, PRIORIDADE " + 
                    "FROM CONTROLE_TPS_ANALISTAS " + 
                    F"WHERE ANALISTA in ({lista_analista[:-1]}) " + 
                    "AND ISSUE LIKE '%AUTO%' "
                    "ORDER BY DIAS_ABERTO DESC").fetchall()

    return tpsgerais, tpsmais15, tpsbacklog, tpsanaliticotot, tpsissue

def contSolAnalista():
    erroAberto = SOL_ERRO.query.filter(SOL_ERRO.STATUS != 'FINALIZADA', SOL_ERRO.ANALISTA_ID == current_user.id).count()
    erroFechado = SOL_ERRO.query.filter(SOL_ERRO.STATUS == 'FINALIZADA', SOL_ERRO.ANALISTA_ID == current_user.id).count()
    alteracaoAberto = SOL_HISTORIA.query.filter(SOL_HISTORIA.STATUS != 'FINALIZADA', SOL_HISTORIA.ANALISTA_ID == current_user.id).count()
    alteracaoFechado = SOL_HISTORIA.query.filter(SOL_HISTORIA.STATUS == 'FINALIZADA', SOL_HISTORIA.ANALISTA_ID == current_user.id).count()
    servicoAberto = SOL_SERVICO.query.filter(SOL_SERVICO.STATUS != 'FINALIZADA', SOL_SERVICO.ANALISTA_ID == current_user.id).count()
    servicoFechado = SOL_SERVICO.query.filter(SOL_SERVICO.STATUS == 'FINALIZADA', SOL_SERVICO.ANALISTA_ID == current_user.id).count()
    scriptAberto = SOL_SCRIPT.query.filter(SOL_SCRIPT.STATUS != 'FINALIZADA', SOL_SCRIPT.ANALISTA_ID == current_user.id).count()
    scriptFechado = SOL_SCRIPT.query.filter(SOL_SCRIPT.STATUS == 'FINALIZADA', SOL_SCRIPT.ANALISTA_ID == current_user.id).count()
    importAberto = SOL_IMPORT.query.filter(SOL_IMPORT.STATUS != 'FINALIZADA', SOL_IMPORT.ANALISTA_ID == current_user.id).count()
    importFechado = SOL_IMPORT.query.filter(SOL_IMPORT.STATUS == 'FINALIZADA', SOL_IMPORT.ANALISTA_ID == current_user.id).count()
    shareAberto = SOL_SHARE.query.filter(SOL_SHARE.STATUS != 'FINALIZADA', SOL_SHARE.ANALISTA_ID == current_user.id).count()
    shareFechado = SOL_SHARE.query.filter(SOL_SHARE.STATUS == 'FINALIZADA', SOL_SHARE.ANALISTA_ID == current_user.id).count()
    helpAberto = HELP.query.filter(HELP.STATUS != 'FINALIZADA', HELP.ANALISTA_ID == current_user.id).count()
    helpFechado = HELP.query.filter(HELP.STATUS == 'FINALIZADA', HELP.ANALISTA_ID == current_user.id).count()

    return erroAberto, erroFechado, alteracaoAberto, alteracaoFechado, servicoAberto, servicoFechado, scriptAberto, scriptFechado, importAberto, importFechado, shareAberto, shareFechado, helpAberto, helpFechado

def contSolHelper():
    erroAberto = SOL_ERRO.query.filter(SOL_ERRO.STATUS != 'FINALIZADA', SOL_ERRO.HELPER_ID == current_user.id).count()
    erroFechado = SOL_ERRO.query.filter(SOL_ERRO.STATUS == 'FINALIZADA', SOL_ERRO.HELPER_ID == current_user.id).count()
    alteracaoAberto = SOL_HISTORIA.query.filter(SOL_HISTORIA.STATUS != 'FINALIZADA', SOL_HISTORIA.HELPER_ID == current_user.id).count()
    alteracaoFechado = SOL_HISTORIA.query.filter(SOL_HISTORIA.STATUS == 'FINALIZADA', SOL_HISTORIA.HELPER_ID == current_user.id).count()
    servicoAberto = SOL_SERVICO.query.filter(SOL_SERVICO.STATUS != 'FINALIZADA', SOL_SERVICO.HELPER_ID == current_user.id).count()
    servicoFechado = SOL_SERVICO.query.filter(SOL_SERVICO.STATUS == 'FINALIZADA', SOL_SERVICO.HELPER_ID == current_user.id).count()
    scriptAberto = SOL_SCRIPT.query.filter(SOL_SCRIPT.STATUS != 'FINALIZADA', SOL_SCRIPT.HELPER_ID == current_user.id).count()
    scriptFechado = SOL_SCRIPT.query.filter(SOL_SCRIPT.STATUS == 'FINALIZADA', SOL_SCRIPT.HELPER_ID == current_user.id).count()
    importAberto = SOL_IMPORT.query.filter(SOL_IMPORT.STATUS != 'FINALIZADA', SOL_IMPORT.HELPER_ID == current_user.id).count()
    importFechado = SOL_IMPORT.query.filter(SOL_IMPORT.STATUS == 'FINALIZADA', SOL_IMPORT.HELPER_ID == current_user.id).count()
    shareAberto = SOL_SHARE.query.filter(SOL_SHARE.STATUS != 'FINALIZADA', SOL_SHARE.HELPER_ID == current_user.id).count()
    shareFechado = SOL_SHARE.query.filter(SOL_SHARE.STATUS == 'FINALIZADA', SOL_SHARE.HELPER_ID == current_user.id).count()
    helpAberto = HELP.query.filter(HELP.STATUS != 'FINALIZADA', HELP.STATUS != 'CANCELADO', HELP.HELPER_ID == current_user.id).count()
    helpFechado = HELP.query.filter(HELP.STATUS == 'FINALIZADA', HELP.HELPER_ID == current_user.id).count()

    return erroAberto, erroFechado, alteracaoAberto, alteracaoFechado, servicoAberto, servicoFechado, scriptAberto, scriptFechado, importAberto, importFechado, shareAberto, shareFechado, helpAberto, helpFechado

def contSolGestor():
    erroAberto = SOL_ERRO.query.filter(SOL_ERRO.STATUS != 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    erroFechado = SOL_ERRO.query.filter(SOL_ERRO.STATUS == 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    alteracaoAberto = SOL_HISTORIA.query.filter(SOL_HISTORIA.STATUS != 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    alteracaoFechado = SOL_HISTORIA.query.filter(SOL_HISTORIA.STATUS == 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    servicoAberto = SOL_SERVICO.query.filter(SOL_SERVICO.STATUS != 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    servicoFechado = SOL_SERVICO.query.filter(SOL_SERVICO.STATUS == 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    scriptAberto = SOL_SCRIPT.query.filter(SOL_SCRIPT.STATUS != 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    scriptFechado = SOL_SCRIPT.query.filter(SOL_SCRIPT.STATUS == 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    importAberto = SOL_IMPORT.query.filter(SOL_IMPORT.STATUS != 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    importFechado = SOL_IMPORT.query.filter(SOL_IMPORT.STATUS == 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    shareAberto = SOL_SHARE.query.filter(SOL_SHARE.STATUS != 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    shareFechado = SOL_SHARE.query.filter(SOL_SHARE.STATUS == 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    helpAberto = HELP.query.filter(HELP.STATUS != 'FINALIZADA', HELP.STATUS != 'CANCELADO').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()
    helpFechado = HELP.query.filter(HELP.STATUS == 'FINALIZADA').join(ANALISTA.query.filter().join(TIME.query.filter_by(GESTOR_ID=current_user.id))).count()

    return erroAberto, erroFechado, alteracaoAberto, alteracaoFechado, servicoAberto, servicoFechado, scriptAberto, scriptFechado, importAberto, importFechado, shareAberto, shareFechado, helpAberto, helpFechado

def contSolCoordenador():
    erroAberto = SOL_ERRO.query.filter(SOL_ERRO.STATUS != 'FINALIZADA').count()
    erroFechado = SOL_ERRO.query.filter(SOL_ERRO.STATUS == 'FINALIZADA').count()
    alteracaoAberto = SOL_HISTORIA.query.filter(SOL_HISTORIA.STATUS != 'FINALIZADA').count()
    alteracaoFechado = SOL_HISTORIA.query.filter(SOL_HISTORIA.STATUS == 'FINALIZADA').count()
    servicoAberto = SOL_SERVICO.query.filter(SOL_SERVICO.STATUS != 'FINALIZADA').count()
    servicoFechado = SOL_SERVICO.query.filter(SOL_SERVICO.STATUS == 'FINALIZADA').count()
    scriptAberto = SOL_SCRIPT.query.filter(SOL_SCRIPT.STATUS != 'FINALIZADA').count()
    scriptFechado = SOL_SCRIPT.query.filter(SOL_SCRIPT.STATUS == 'FINALIZADA').count()
    importAberto = SOL_IMPORT.query.filter(SOL_IMPORT.STATUS != 'FINALIZADA').count()
    importFechado = SOL_IMPORT.query.filter(SOL_IMPORT.STATUS == 'FINALIZADA').count()
    shareAberto = SOL_SHARE.query.filter(SOL_SHARE.STATUS != 'FINALIZADA').count()
    shareFechado = SOL_SHARE.query.filter(SOL_SHARE.STATUS == 'FINALIZADA').count()
    helpAberto = HELP.query.filter(HELP.STATUS != 'FINALIZADA', HELP.STATUS != 'CANCELADO').count()
    helpFechado = HELP.query.filter(HELP.STATUS == 'FINALIZADA').count()

    return erroAberto, erroFechado, alteracaoAberto, alteracaoFechado, servicoAberto, servicoFechado, scriptAberto, scriptFechado, importAberto, importFechado, shareAberto, shareFechado, helpAberto, helpFechado

def pegaLink(form_atualizacria):
    versao = form_atualizacria.versao.data
    estrutura = form_atualizacria.estrutura.data
    programa = form_atualizacria.programa.data
    if versao == '5.07':
        if estrutura == '2 Camadas':
            if programa == 'Apollo':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_Apollo0507.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0507.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip'
            elif programa == 'Bravos':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_BRAVOS0507.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0507.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip'
            elif programa == 'Toyota':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_TOYOTA_0507.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0507.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip'
            elif programa == 'Autoshop':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_AUTOSHOP_0507.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0507.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip'
        elif estrutura == '3 Camadas':
            if programa == 'Apollo':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_Apollo0507_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_Apollo0507_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0507_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0507_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip'
            elif programa == 'Bravos':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_BRAVOS0507_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_BRAVOS0507_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip'
            elif programa == 'Toyota':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_TOYOTA_0507_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_TOYOTA_0507_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0507_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0507_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip'
            elif programa == 'Autoshop':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_AUTOSHOP_0507_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_AUTOSHOP_0507_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0507_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0507_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip'
        else:
            flash('Erro', 'alert-danger')
    if versao == '5.06':
        if estrutura == '2 Camadas':
            if programa == 'Apollo':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_Apollo0506.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0506.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/script0506.zip'
            elif programa == 'Bravos':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_BRAVOS0506.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0506.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/script0506.zip'
            elif programa == 'Toyota':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_TOYOTA_0506.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0506.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/script0506.zip'
            elif programa == 'Autoshop':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_AUTOSHOP_0506.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0506.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/script0506.zip'
        elif estrutura == '3 Camadas':
            if programa == 'Apollo':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_Apollo0506_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_Apollo0506_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0506_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0506_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/script0506.zip'
            elif programa == 'Bravos':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_BRAVOS0506_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_BRAVOS0506_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0506_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0506_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/script0506.zip'
            elif programa == 'Toyota':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_TOYOTA_0506_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_TOYOTA_0506_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0506_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0506_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/script0506.zip'
            elif programa == 'Autoshop':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_AUTOSHOP_0506_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/DVI_AUTOSHOP_0506_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0506_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0506_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Liberacao_Inicial/script0506.zip'
        else:
            flash('Erro', 'alert-danger')
    if versao == '5.05':
        if estrutura == '2 Camadas':
            if programa == 'Apollo':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_Apollo0505.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0505.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/script0505.zip'
            elif programa == 'Bravos':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_BRAVOS0505.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0505.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/script0505.zip'
            elif programa == 'Toyota':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_TOYOTA_0505.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0505.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/script0505.zip'
            elif programa == 'Autoshop':
                linkliberacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_AUTOSHOP_0505.zip'
                linkatualizacao = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0505.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/script0505.zip'
        elif estrutura == '3 Camadas':
            if programa == 'Apollo':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_Apollo0505_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_Apollo0505_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0505_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0505_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/script0505.zip'
            elif programa == 'Bravos':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_BRAVOS0505_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_BRAVOS0505_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0505_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0505_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/script0505.zip'
            elif programa == 'Toyota':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_TOYOTA_0505_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_TOYOTA_0505_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0505_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_TOYOTA_V0505_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/script0505.zip'
            elif programa == 'Autoshop':
                linkliberacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_AUTOSHOP_0505_Client.zip'
                linkliberacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/DVI_AUTOSHOP_0505_Server.zip'
                linkatualizacaoclient = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0505_3Camadas_Client.zip'
                inkatualizacaoserver = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Atualizacoes_DVI/DVI_Atualizacoes_AUTOSHOP_V0505_3Camadas_Server.zip'
                linkscript = 'https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.05/Liberacao_Inicial/script0505.zip'
        else:
            flash('Erro', 'alert-danger')
        
    if estrutura == '2 Camadas':
        return linkliberacao, linkatualizacao, linkscript
    elif estrutura == '3 Camadas':
        return linkliberacaoclient, linkliberacaoserver, linkatualizacaoclient, inkatualizacaoserver, linkscript