@echo off
mkdir "C:\Bravos-3Camadas-507"
cd "C:\Bravos-3Camadas-507"
cUrl.exe "https://distribuicao.blob.core.windows.net/suporte/Marconi/Modelo-3Camadas.zip" -o "C:\Bravos-3Camadas-507\Modelo.zip"

unzip "C:\Bravos-3Camadas-507\Modelo"
xcopy "C:\Bravos-3Camadas-507\Modelo-3Camadas\." "C:\Bravos-3Camadas-507" /e

rmdir Modelo-3Camadas /s /q

cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_BRAVOS0507_Client.zip" -o "C:\Bravos-3Camadas-507\DVI_BRAVOS0507_Client.zip"
cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_BRAVOS0507_Server.zip" -o "C:\Bravos-3Camadas-507\DVI_BRAVOS0507_Server.zip"
cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Client.zip" -o "C:\Bravos-3Camadas-507\DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Client.zip"
cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Server.zip" -o "C:\Bravos-3Camadas-507\DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Client.zip"
cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip" -o "C:\Bravos-3Camadas-507\DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Client.zip"

unzip -o "DVI_BRAVOS0507_Client"
unzip -o "DVI_BRAVOS0507_Server"
unzip -o "DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Client" 
unzip -o "DVI_Atualizacoes_BRAVOS_V0507_3Camadas_Server" 
unzip -o "script0507" 

    