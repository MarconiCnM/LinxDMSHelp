@echo off
set PATH=%PATH%;C:/Program Files/7-Zip/
cd "C:\Bravos-2Camadas-506"

cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0507.zip" -o "C:\Bravos-2Camadas-506\DVI_Atualizacoes_BRAVOS_V0507.zip"

7z e -y "DVI_Atualizacoes_BRAVOS_V0507.zip"

del DVI_Atualizacoes_BRAVOS_V0507.zip
