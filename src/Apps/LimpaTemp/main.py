import subprocess


host = "MTZNOTFS031063.linx-inves.com.br"
db = "LINXDMSHELP"
user = "SA"
password = "Linx@2021*"
sqlcmd = (
    r"C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\SQLCMD.EXE")


query_delete =  f"delete from Consulta"
subprocess.call([sqlcmd, "-U", user, "-P", password, "-S", host, "-d", db, "-Q", query_delete])