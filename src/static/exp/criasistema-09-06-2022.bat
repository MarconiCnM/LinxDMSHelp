mkdir "C:\Bravos-2Camadas-507"
cd "C:\Bravos-2Camadas-507"
cUrl.exe "https://distribuicao.blob.core.windows.net/suporte/Marconi/Modelo.zip" -o "C:\Bravos-2Camadas-507\Modelo.zip"

unzip "C:\Bravos-2Camadas-507\Modelo.zip"
copy "C:\Bravos-2Camadas-507\Modelo\." "C:\Bravos-2Camadas-507"

cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/DVI_Apollo0507.zip" -o "C:\Bravos-2Camadas-507\DVI_Apollo0507.zip"
cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Atualizacoes_DVI/DVI_Atualizacoes_Apollo_V0507.zip" -o "C:\Bravos-2Camadas-507\DVI_Atualizacoes_Apollo_V0507.zip"
cUrl.exe "https://distribuicao.blob.core.windows.net/dms/DVI/Versoes/v5.07/Liberacao_Inicial/script0507.zip" -o "C:\Bravos-2Camadas-507\script0507.zip"

unzip "C:\Bravos-2Camadas-507\DVI_Apollo0507.zip"
unzip "C:\Bravos-2Camadas-507\DVI_Atualizacoes_Apollo_V0507.zip"
unzip "C:\Bravos-2Camadas-507\script0507.zip"
