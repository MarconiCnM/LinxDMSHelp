import scrapy
import subprocess

host = "POANOTFS013816"
db = "LINXDMSHELP"
user = "SA"
password = "Linx@2021*"
sqlcmd = (
    r"C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\SQLCMD.EXE")

time = [
    "ALAN.MACHADO",
    "ANDRESSA.AGUIAR",
    "DIEFERSON.WEREN",
    "GABRIEL.REOLON",
    "DOUGLAS.MUNHOZ",
    "HENRIQUE.JAEGER",
    "JULIANA.RUFATO",
    "NAIARA.ANDRADE",
    "NICOLAS.LERMEN",
    "ALISSON.RIBEIRO",
    "KATRYNE.SILVA",
    "BRIAN.SILVA",
    "DIEGO.ROSA",
    "DORVALINO.NETO",
    "FERNANDO.VARGAS",
    "JOCELI.SILVA",
    "CATARINA.SILVEIRA",
    "GABRIEL.MARTIN",
    "PAOLA.RIBEIRO",
    "VANESSA.CALCAO",
    "THIAGO.DAVIS",
    "BRUNA.SCHREINER",
    "LUIS.AMARAL",
    "THAYLLA.SOARES",
    "DIONATA.SILVEIRA",
    "LEONARDO.CORSINO",
    "ADRIANO.SIMOES",
    "ADRIANA.COSTA",
    "JESSICA.PAULA",
    "GISLAINE.RODRIGUES",
    "LUIS.SUSIN",
    "PRISCILA.POLIMENO",
    "FRANCIELLE.OLIVEIRA",
    "GILMAR.LAZARI",
    "RODRIGO.MOREIRA",
    "GUILHERME.TOLFO",
    "ERISON.DAMACENA",
    "ANA.HEITELVAN",
    "ARIANA.FREITAG",
    "TAMIRES.FONSECA",
    "IGOR.BECK",
    "STEFANO.BECK",
    "ALISSON.COSTA",
    "ARTHUR.DINIZ",
    "BRUNO.ZEFERINO",
    "JOANA.OLIVEIRA",
    "JUAN.SANTOS",
    "MARIA.GABRIELA",
    "SAMUEL.ZANATTA",
    "CARLA.GARCIA",
    "MARCIA.FERREIRA",
    "LUANA.SINHORELI",
    "JOSE.PROCIDIO",
    "LEONARDO.GUIMARAES",
    "ANA.STEIN"
]


query_delete =  f"delete from CONTROLE_TPS_ANALISTAS"
subprocess.call([sqlcmd, "-U", user, "-P", password, "-S", host, "-d", db, "-Q", query_delete])

class WfSpider(scrapy.Spider):
    name = 'nro_tps'
    start_urls = []
    for analista in time:
            start_urls.append(f'http://a-srv63/SUPORTE/sgc_cliente_recurso.asp?recurso={analista}')

    def parse(self, response):
        lista_tps = response.css('a::text').getall()
        
        for index, tp in enumerate(lista_tps):
            nro_tp = tp
            analista = response.css(f'.SLA_fora:nth-child({index + 3}) td:nth-child(6) .style5::text').get()
            if analista is None:
                analista = response.css(f'.SLA_dentro:nth-child({index + 3}) td:nth-child(6) .style5::text').get()
            grupo = response.css(f'.SLA_fora:nth-child({index + 3}) td:nth-child(1) .style5::text').get()
            if grupo is None:
                grupo = response.css(f'.SLA_dentro:nth-child({index + 3}) td:nth-child(1) .style5::text').get()
            resumo = response.css(f'.SLA_fora:nth-child({index + 3}) td:nth-child(7) .style5::text').get()
            if resumo is None:
                resumo = response.css(f'.SLA_dentro:nth-child({index + 3}) td:nth-child(7) .style5::text').get()
            qtd_dias = response.css(f'.SLA_fora:nth-child({index + 3}) .style17::text').get()
            if qtd_dias is None:
                qtd_dias = response.css(f'.SLA_dentro:nth-child({index + 3}) .style17::text').get()
            status = response.css(f'.SLA_fora:nth-child({index + 3}) td:nth-child(5) .style5::text').get()
            if status is None:
                status = response.css(f'.SLA_dentro:nth-child({index + 3}) td:nth-child(5) .style5::text').get()
            prioridade =  response.css(f'.SLA_fora:nth-child({index + 3}) .style12:nth-child(8)::text').get()
            if prioridade is None:
                prioridade =  response.css(f'.SLA_dentro:nth-child({index + 3}) .style12:nth-child(8)::text').get()
            
            query_insert =  f"insert CONTROLE_TPS_ANALISTAS values ({nro_tp}, null, '{analista.replace('.', ' ').title()}', '{grupo}', '{resumo}', {qtd_dias}, null, null, '{status}', '{prioridade}')"
            subprocess.call([sqlcmd, "-U", user, "-P", password, "-S", host, "-d", db, "-Q", query_insert])
        
        for tp in lista_tps:
            link = f'http://a-srv63/SUPORTE/followup_find.asp?OBJETO_ID={tp}'
            yield scrapy.Request(
                link,
                callback=self.parse_category
            )
    
    def parse_category(self, response):
        nro_tp = response.css('tr:nth-child(1) font font strong::text').get()
        issue = response.css('table~ table td > p > font::text').getall()
        ult_mov = response.css('tr:nth-child(1) div > font::text').get()
        dta_fim = response.css('tr:nth-child(4) strong font+ font::text').get()
        for mov in issue:
            if mov.find('AUTO-') > 0:
                issue = [mov[mov.rfind('AUTO-'):-11]]
                if len(mov[mov.rfind('AUTO-'):-11]) > 10:
                    issue = 'N'
        
        for mov in issue:
            if mov.find('AUTO-') < 0:
                issue = 'N'

        for i in ult_mov:
            ult_mov = ult_mov.strip()

        query_insert =  f"update CONTROLE_TPS_ANALISTAS set issue = '{issue[0]}', dta_ult_mov = '{ult_mov}', dta_fim = '{dta_fim}' where nro_tp = {nro_tp}"

        yield subprocess.call([sqlcmd, "-U", user, "-P", password, "-S", host, "-d", db, "-Q", query_insert])