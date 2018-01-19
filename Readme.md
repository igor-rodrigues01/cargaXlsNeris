
# Carga em banco: Sema e Icmbio

## Script que realiza a carga de dois arquivos .xls com dados do sema e do icmbio
## na base de dados definidada no arquivo contants.py no servidor 10.1.8.58.

### Este script irá baixar os arquivos .xls, criar um diretório para os downloads do dia
### ("file/xls_YYYY-MM-DD"), ler os dados de ambos os arquivos (o .xls icmbio terá a segunda folha ignorada pois dados são irrelevantes), remover todos os dados das tabelas
### "sema" e "icmbio" realizar a inserção nestas tabelas.

# Pré Requisitos

## Altere os dados de conexão no arquivo constants.py

### Para que este script funcione de forma precisa, na lib xlrd, para corrigir
### um problema de obtencao de formatacao das celulas na linha 793 do arquvivo
### /home/<user>/.virtualenvs/<EnvironmentName>/lib/python3.5/site-packages/xlrd/xlsx.py
### (ou um path equivalente que chegue no source code das lib's python) 
### foi alterado: "if formatting_info:" para "if not formatting_info:"