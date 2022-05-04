import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

host = "POANOTFS013816"
db = "LINXDMSHELP"
user = "SA"
password = "Linx@2021*"
sqlcmd = (
    r"C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\SQLCMD.EXE")

lista_filas = [
    'DOUGLAS.MUNHOZ',
    'HENRIQUE.JAEGER',
    'JULIANA.RUFATO',
    'NAIARA.ANDRADE',
    'NICOLAS.LERMEN'
]

while True:
    for fila in lista_filas:
        try:
            var = ''
            lista = 0

            query_delete = f"delete from CONTROLE_TPS_ANALISTAS where analista = '{fila.replace('.', ' ').title()}'"
            subprocess.call([sqlcmd, "-U", user, "-P", password,
                            "-S", host, "-d", db, "-Q", query_delete])

            driver.get(
                f"http://a-srv63/SUPORTE/sgc_cliente_recurso.asp?recurso={fila}")

            try:
                quantidade_tps = driver.find_element(
                    By.XPATH, '/html/body/table[1]/tbody/tr[2]/td[1]/div/font/strong').text

                for i in quantidade_tps:
                    var += i

                while lista < int(var):
                    nro_tp = ''
                    grupo = ''
                    resumo = ''
                    qtd_dias = ''
                    status = ''

                    nro_tp_object = driver.find_element(By.XPATH,
                                                        f"/html/body/table[2]/tbody/tr[{3 + lista}]/td[2]/span/a").text

                    for i in nro_tp_object:
                        nro_tp += str(i)

                    grupo_object = driver.find_element(By.XPATH,
                                                       f"/html/body/table[2]/tbody/tr[{3 + lista}]/td[1]/span").text

                    for i in grupo_object:
                        grupo += str(i)

                    grupo = grupo.split(' -')[0]

                    resumo_object = driver.find_element(By.XPATH,
                                                        f"/html/body/table[2]/tbody/tr[{3 + lista}]/td[7]/span").text

                    for i in resumo_object:
                        resumo += str(i)

                    resumo = resumo.replace("'", "")
                    resumo = resumo.replace('"', '')

                    qtd_dias_object = driver.find_element(By.XPATH,
                                                          f"/html/body/table[2]/tbody/tr[{3 + lista}]/td[11]/div/span").text

                    for i in qtd_dias_object:
                        qtd_dias += str(i)

                    status_object = driver.find_element(By.XPATH,
                                                        f"/html/body/table[2]/tbody/tr[{3 + lista}]/td[5]/span").text

                    for i in status_object:
                        status += str(i)

                    driver.get(
                        f"http://a-srv63/SUPORTE/followup_find.asp?OBJETO_ID={nro_tp}")

                    dta_ult_mov = driver.find_element(By.XPATH,
                                                      f"/html/body/table[2]/tbody/tr[1]/td[1]/div[3]/font").text

                    dta_encerramento = driver.find_element(By.XPATH,
                                                      f"/html/body/table[1]/tbody/tr[4]/td[1]/font/strong/font[2]").text

                    prioridade = driver.find_element(By.XPATH,
                                                      f"/html/body/table[1]/tbody/tr[3]/td[1]/p/font/font/strong").text

                    lista += 1

                    query_insert = f"insert CONTROLE_TPS_ANALISTAS values ({nro_tp}, '{fila.replace('.', ' ').title()}', '{grupo}', '{resumo}', {qtd_dias}, '{dta_ult_mov[6:]}', '{dta_encerramento}', '{status}', '{prioridade}')"
                    subprocess.call(
                        [sqlcmd, "-U", user, "-P", password, "-S", host, "-d", db, "-Q", query_insert])

                    driver.get(
                        f"http://a-srv63/SUPORTE/sgc_cliente_recurso.asp?recurso={fila}")

            except:
                next
        except:
            next
