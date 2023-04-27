import os
from datetime import datetime
import shutil
import re
import pandas as pd

#relacao, anexo

def arquivoInfo(zips_usados, SOURCE_DIR):
    now = datetime.now()
    date_time = now.strftime("%d_%m_%Y")
    diretorio = os.path.join(SOURCE_DIR, 'arquivosDeLog')
    with open('{}/{}.txt'.format(diretorio, date_time), 'w') as f:
        for arquivozip in zips_usados:
            f.write('{}\n'.format(arquivozip))
    f.close()

def getNomeArquivo(listaNomes):
    cod_uags, cod_licitacoes = [], []
    remove_numero = re.compile('(\s)?(\(\d\)(\s)?)')
    for nome in listaNomes:
        nome = re.sub(remove_numero, '', os.path.splitext(nome)[0])
        try:
            cod_uag, cod_doc = nome.split('_')
        except ValueError:
            continue
        cod_uags.append(cod_uag)
        cod_licitacoes.append(cod_doc)
    return cod_uags, cod_licitacoes

def geraDataFrameNomes(cod_uags, cod_licitacoes):
    processados = [0 for i in range(len(cod_uags))]
    dataFrameNomes = pd.DataFrame({'ID-UAG': cod_uags, 'ID-LICITACAO': cod_licitacoes, 'processado': processados})
    dataFrameNomes.to_csv('datasets/arquivosZip.csv', index=False, encoding='utf-8')
      
def selecionaArquivos(SOURCE_DIR):
    lista_nomes = []
    for indice, arquivo in enumerate(os.listdir(SOURCE_DIR)):
        lista_nomes.append(arquivo)
    cod_uags, cod_licitacoes = getNomeArquivo(lista_nomes)
    geraDataFrameNomes(cod_uags, cod_licitacoes)

def processaArquivos(SOURCE_DIR, DEST_DIR, quantidade):
    dfarquivos = pd.read_csv('datasets/arquivosZip.csv')
    arquivosCandidatos = dfarquivos.loc[dfarquivos['processado'] == 0].head(quantidade)
    for arquivo in arquivosCandidatos.index:
        nome_uag = arquivosCandidatos['ID-UAG'][arquivo]
        nome_licitacao = arquivosCandidatos['ID-LICITACAO'][arquivo]
        nome_completo = '{}_{}'.format(nome_uag, nome_licitacao)
        caminho_arquivo = os.path.join(SOURCE_DIR, nome_completo)
        shutil.copy(caminho_arquivo, DEST_DIR)

def moveArquivosProcessados(diretorio_origem, diretorio_destino):
    for diretorio_atual, subdiretorios, arquivos in os.walk(diretorio_origem):
        for arquivo in arquivos:
            caminho_origem = os.path.join(diretorio_atual, arquivo)
            caminho_destino = os.path.join(diretorio_destino, arquivo)
            shutil.move(caminho_origem, caminho_destino)
            
def moveArquivosValidos(SOURCE_DIR, DEST_DIR):
    extensoes_validas = ['.pdf', '.doc', '.docx', '.odt']
    relacao_itens = re.compile('Rela[cç][aã]o', re.IGNORECASE)
    for diretorio_atual, subdiretorios, arquivos in os.walk(SOURCE_DIR):
        for arquivo in arquivos:
            if os.path.splitext(arquivo)[1] in extensoes_validas:
                busca = re.search(relacao_itens, os.path.splitext(arquivo)[0])
                if busca == None:
                    print(arquivo)
                    caminho_origem = os.path.join(diretorio_atual, arquivo)
                    caminho_destino = os.path.join(DEST_DIR, arquivo)
                    shutil.move(caminho_origem, caminho_destino)


SOURCE_DIR = '/var/comprasnet_arquivos'
DEST_DIR = '/var/projetos/arquivos'
processaArquivos(SOURCE_DIR, DEST_DIR, 10000)
#selecionaArquivos(SOURCE_DIR)
#moveArquivosProcessados(PROCESSADOS_DIR, ARQUIVOSPRONTOS_DIR)
#moveArquivosValidos(ARQUIVOSPRONTOS_DIR, PROPARSR_DIR)