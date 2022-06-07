import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

host = "MTZNOTFS031063.linx-inves.com.br"
db = "LINXDMSHELP"
user = "SA"
password = "Linx@2021*"
sqlcmd = (
    r"C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\SQLCMD.EXE")

while True:
    try:
        lista_filas = [
            "DMS APOLLO - SUPORTE APOLLO",
            "DMS APOLLO - SUPORTE BRAVOS",
            "LINX DMS - SUPORTE TOYOTA",
            "LINX DMS - SUPORTE AUTOSHOP",
            "DMS APOLLO - SUPORTE BERÇÁRIO",
            "DMS APOLLO - SUPORTE FINANCEIRO",
            "DMS APOLLO - SUPORTE NFCE/NFSE/TEF",
            "DMS APOLLO - SUPORTE MONTADORAS",
            "DMS APOLLO - SUPORTE MOBILE",
            "DMS APOLLO - SUPORTE CONTABIL/FISCAL",
            "DMS APOLLO - SUPORTE LINX DMS CC1"
        ]

        for fila in lista_filas:
            var = ''
            lista = 0
            p0 = 0
            p1 = 0
            p2 = 0
            p3 = 0

            driver.get(
                f"http://a-srv63/SUPORTE/sgc_cliente_recurso.asp?recurso={fila}")

            try:
                quantidade_tps = driver.find_element(By.XPATH,
                                                     '/html/body/table[1]/tbody/tr[2]/td[1]/div/font/strong').text

                for i in quantidade_tps:
                    var += i

                while lista < int(var):
                    prioridade = ''

                    tp = driver.find_element(By.XPATH,
                                             f"/html/body/table[2]/tbody/tr[{3 + lista}]/td[8]").text

                    for i in tp:
                        prioridade += i

                    if prioridade == 'Altíssima':
                        p0 += 1
                    elif prioridade == 'Alta':
                        p1 += 1
                    elif prioridade == 'Media':
                        p2 += 1
                    elif prioridade == 'Baixa':
                        p3 += 1

                    lista += 1

                    if lista == int(var):
                        if fila == 'DMS APOLLO - SUPORTE APOLLO':
                            query = f"update CONTROLE_TPS_GERAIS set APOLLO_tot={var}, APOLLO_p0={p0}, APOLLO_p1={p1}, APOLLO_p2={p2}, APOLLO_p3={p3} where id=1"
                        elif fila == "DMS APOLLO - SUPORTE BRAVOS":
                            query = f"update CONTROLE_TPS_GERAIS set BRAVOS_tot={var}, BRAVOS_p0={p0}, BRAVOS_p1={p1}, BRAVOS_p2={p2}, BRAVOS_p3={p3} where id=1"
                        elif fila == "LINX DMS - SUPORTE TOYOTA":
                            query = f"update CONTROLE_TPS_GERAIS set TOYOTA_tot={var}, TOYOTA_p0={p0}, TOYOTA_p1={p1}, TOYOTA_p2={p2}, TOYOTA_p3={p3} where id=1"
                        elif fila == "LINX DMS - SUPORTE AUTOSHOP":
                            query = f"update CONTROLE_TPS_GERAIS set AUTOSHOP_tot={var}, AUTOSHOP_p0={p0}, AUTOSHOP_p1={p1}, AUTOSHOP_p2={p2}, AUTOSHOP_p3={p3} where id=1"
                        elif fila == "DMS APOLLO - SUPORTE BERÇÁRIO":
                            query = f"update CONTROLE_TPS_GERAIS set BERCARIO_tot={var}, BERCARIO_p0={p0}, BERCARIO_p1={p1}, BERCARIO_p2={p2}, BERCARIO_p3={p3} where id=1"
                        elif fila == "DMS APOLLO - SUPORTE FINANCEIRO":
                            query = f"update CONTROLE_TPS_GERAIS set FINANCEIRO_tot={var}, FINANCEIRO_p0={p0}, FINANCEIRO_p1={p1}, FINANCEIRO_p2={p2}, FINANCEIRO_p3={p3} where id=1"
                        elif fila == "DMS APOLLO - SUPORTE NFCE/NFSE/TEF":
                            query = f"update CONTROLE_TPS_GERAIS set nfce_tot={var}, nfce_p0={p0}, nfce_p1={p1}, nfce_p2={p2}, nfce_p3={p3} where id=1"
                        elif fila == "DMS APOLLO - SUPORTE MONTADORAS":
                            query = f"update CONTROLE_TPS_GERAIS set MONTADORA_tot={var}, MONTADORA_p0={p0}, MONTADORA_p1={p1}, MONTADORA_p2={p2}, MONTADORA_p3={p3} where id=1"
                        elif fila == "DMS APOLLO - SUPORTE MOBILE":
                            query = f"update CONTROLE_TPS_GERAIS set MOBILE_tot={var}, MOBILE_p0={p0}, MOBILE_p1={p1}, MOBILE_p2={p2}, MOBILE_p3={p3} where id=1"
                        elif fila == "DMS APOLLO - SUPORTE CONTABIL/FISCAL":
                            query = f"update CONTROLE_TPS_GERAIS set contabil_tot={var}, contabil_p0={p0}, contabil_p1={p1}, contabil_p2={p2}, contabil_p3={p3} where id=1"
                        elif fila == "DMS APOLLO - SUPORTE LINX DMS CC1":
                            query = f"update CONTROLE_TPS_GERAIS set CC1_tot={var}, CC1_p0={p0}, CC1_p1={p1}, CC1_p2={p2}, CC1_p3={p3} where id=1"
                        else:
                            print("Erro.")

                    subprocess.call(
                        [sqlcmd, "-U", user, "-P", password, "-S", host, "-d", db, "-Q", query])

            except:
                if fila == 'DMS APOLLO - SUPORTE APOLLO':
                    query = f"update CONTROLE_TPS_GERAIS set APOLLO_tot=0, APOLLO_p0=0, APOLLO_p1=0, APOLLO_p2=0, APOLLO_p3=0 where id=1"
                elif fila == "DMS APOLLO - SUPORTE BRAVOS":
                    query = f"update CONTROLE_TPS_GERAIS set bravos_tot=0, bravos_p0=0, bravos_p1=0, bravos_p2=0, bravos_p3=0 where id=1"
                elif fila == "LINX DMS - SUPORTE TOYOTA":
                    query = f"update CONTROLE_TPS_GERAIS set TOYOTA_tot=0, TOYOTA_p0=0, TOYOTA_p1=0, TOYOTA_p2=0, TOYOTA_p3=0 where id=1"
                elif fila == "LINX DMS - SUPORTE AUTOSHOP":
                    query = f"update CONTROLE_TPS_GERAIS set AUTOSHOP_tot=0, AUTOSHOP_p0=0, AUTOSHOP_p1=0, AUTOSHOP_p2=0, AUTOSHOP_p3=0 where id=1"
                elif fila == "DMS APOLLO - SUPORTE BERÇÁRIO":
                    query = f"update CONTROLE_TPS_GERAIS set BERCARIO_tot=0, BERCARIO_p0=0, BERCARIO_p1=0, BERCARIO_p2=0, BERCARIO_p3=0 where id=1"
                elif fila == "DMS APOLLO - SUPORTE FINANCEIRO":
                    query = f"update CONTROLE_TPS_GERAIS set FINANCEIRO_tot=0, FINANCEIRO_p0=0, FINANCEIRO_p1=0, FINANCEIRO_p2=0, FINANCEIRO_p3=0 where id=1"
                elif fila == "DMS APOLLO - SUPORTE NFCE/NFSE/TEF":
                    query = f"update CONTROLE_TPS_GERAIS set nfce_tot=0, nfce_p0=0, nfce_p1=0, nfce_p2=0, nfce_p3=0 where id=1"
                elif fila == "DMS APOLLO - SUPORTE MONTADORAS":
                    query = f"update CONTROLE_TPS_GERAIS set montadora_tot=0, montadora_p0=0, montadora_p1=0, montadora_p2=0, montadora_p3=0 where id=1"
                elif fila == "DMS APOLLO - SUPORTE MOBILE":
                    query = f"update CONTROLE_TPS_GERAIS set MOBILE_tot=0, MOBILE_p0=0, MOBILE_p1=0, MOBILE_p2=0, MOBILE_p3=0 where id=1"
                elif fila == "DMS APOLLO - SUPORTE CONTABIL/FISCAL":
                    query = f"update CONTROLE_TPS_GERAIS set contabil_tot=0, contabil_p0=0, contabil_p1=0, contabil_p2=0, contabil_p3=0 where id=1"
                elif fila == "DMS APOLLO - SUPORTE LINX DMS CC1":
                    query = f"update CONTROLE_TPS_GERAIS set CC1_tot=0, CC1_p0=0, CC1_p1=0, CC1_p2=0, CC1_p3=0 where id=1"
                else:
                    print("Erro.")

                subprocess.call([sqlcmd, "-U", user, "-P",
                                password, "-S", host, "-d", db, "-Q", query])
    except:
        next
