@echo off
set PATH=%PATH%;C:/Program Files/7-Zip/
cd "None"

cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.06/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0506.zip" -o "None\DVI_Atualizacoes_BRAVOS_V0506.zip"

7z e -y "DVI_Atualizacoes_BRAVOS_V0506.zip"

del DVI_Atualizacoes_BRAVOS_V0506.zip
