# ==================================================================================================================
# Import de biblioteca
import os

# ==================================================================================================================
# Definição de caminho do arquivo bash
raiz = r'C:\Users\Taking\OneDrive - taking\Área de Trabalho\Projeto Esteira BI'
caminho_arquivo = raiz + r'\Projeto\arquivos\credenciais.sh'
arquivo = caminho_arquivo.replace("\\", "/")


# ==================================================================================================================
# Abrindo arquivo
with open(arquivo, 'r') as file:
    # Pegando conteudo do arquivo e quebrando por linha
    for linha in file.read().split('\n'):
        # Separando cada linha por chave e valor
        valores_linha = linha.split('=')
        # Conferindo se valor na linha é valido
        if len(valores_linha) > 1:
            # Pegando a chave
            chave = valores_linha[0]
            # Pegando o valor
            valor = '='.join(valores_linha[1:])

            # Defindo a variável de ambiente
            os.environ[chave] = valor