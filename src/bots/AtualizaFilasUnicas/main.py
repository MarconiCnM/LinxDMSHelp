import subprocess
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

host = "POADSKFS015444"
db = "HELP"
user = "SA"
password = "Linx@2021*"
sqlcmd = (
    r"C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\SQLCMD.EXE")

lista_filas = [
    'ADRIANA.COSTA',
    'ADRIANO.SIMOES',
    'ALINE.VARGAS',
    'ALISSON.RIBEIRO',
    'ANA.HEITELVAN',
    'ANA.STEIN',
    'ARIANA.FREITAG',
    'BRIAN.SILVA',
    'BRUNA.SCHREINER',
    'CARLA.GARCIA',
    'CATARINA.SILVEIRA',
    'DIEGO.ROSA',
    'DIONATA.SILVEIRA',
    'DORVALINO.NETO',
    'ERISON.DAMACENA',
    'FERNANDO.VARGAS',
    'FRANCIELLE.OLIVEIRA',
    'FREDERICO.SCHER',
    'GABRIEL.MARTIN',
    'GILMAR.LAZARI',
    'GISLAINE.RODRIGUES',
    'GUILHERME.TOLFO',
    'IGOR.BECK',
    'JOAO.DUARTE',
    'JOCELI.SILVA',
    'JOSE.PROCIDIO',
    'JUAN.SANTOS',
    'JULIANA.RUFATO',
    'LARISSA.PACHECO',
    'LEONARDO.CORSINO',
    'LEONARDO.DESOUZA',
    'LEONARDO.GUIMARAES',
    'LUANA.SINHORELI',
    'LUCAS.ODY',
    'LUIS.AMARAL',
    'LUIS.SUSIN',
    'MARCIA.FERREIRA',
    'MARLENO.FILHO',
    'PAOLA.RIBEIRO',
    'PRISCILA.POLIMENO',
    'RAFAEL.RESENDE',
    'RAQUEL.KUHN',
    'SAMUEL.ZANATTA',
    'TAMIRES.FONSECA',
    'THAYLLA.SOARES',
    'THIAGO.DAVIS',
    'VANESSA.CALCAO'
]

while True:
    sleep(720)
    for fila in lista_filas:
        try:
            var = ''
            lista = 0

            query_delete = f"delete from control_tps_analyst where analista = '{fila.replace('.', ' ').title()}'"
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

                    lista += 1

                    query_insert = f"insert control_tps_analyst values ({nro_tp}, '{grupo}', '{resumo}', {qtd_dias}, '{status}', '{fila.replace('.', ' ').title()}', '{dta_ult_mov[6:]}', '{dta_encerramento}')"
                    subprocess.call(
                        [sqlcmd, "-U", user, "-P", password, "-S", host, "-d", db, "-Q", query_insert])

                    driver.get(
                        f"http://a-srv63/SUPORTE/sgc_cliente_recurso.asp?recurso={fila}")

            except:
                next
        except:
            next
