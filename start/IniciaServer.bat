cd C:\LinxDMSHelp
.venv/Scripts/Activate.ps1
$env:FLASK_APP="src/app.py"
$env:FLASK_ENV="development"
flask run --host 0.0.0.0

-------------------------------------

cd C:\LinxDMSHelp
.venv/Scripts/Activate.ps1
cd C:\LinxDMSHelp\src\Apps\AtualizaFilasGerais\
python main.py
