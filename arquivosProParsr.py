import os
from datetime import datetime
import shutil
import re
import pandas as pd
import zipfile
import tarfile
from tqdm.auto import tqdm

#relacao, anexo
def extracao(SOURCE_DIR, DEST_DIR, DIR_PRO_PARSR):
    for arquivo in tqdm(os.listdir(SOURCE_DIR)):
        caminho_completo_arquivo = os.path.join(SOURCE_DIR, arquivo)
        if os.path.isfile(caminho_completo_arquivo):
            extrair_arquivo(caminho_completo_arquivo, DEST_DIR, DIR_PRO_PARSR, arquivo)
            
def extrair_arquivo(arquivo, destino, dirProParsr, nomePai):
    count = 0
    if zipfile.is_zipfile(arquivo):
        with zipfile.ZipFile(arquivo, 'r') as zip_ref:
            zip_ref.extractall(destino)
        novo_nome = os.path.splitext(nomePai)[0]
        for filename in zip_ref.namelist():
            if arquivosValidos(filename):
                caminho_completo = os.path.join(destino, filename)
                extensao_arquivo = os.path.splitext(filename)[1]
                caminho_novo = os.path.join(destino, '{}.{}'.format(novo_nome, extensao_arquivo))
                os.rename(caminho_completo, caminho_novo)
                try:
                    shutil.move(caminho_novo, dirProParsr)
                except shutil.Error:
                    count+=1
                    caminho_novo = '{}_{}'.format(caminho_novo, count)
                    shutil.move(caminho_novo, dirProParsr)
                    
            caminho_completo_arquivo = os.path.join(destino, filename)
            if zipfile.is_zipfile(caminho_completo_arquivo):
                extrair_arquivo(caminho_completo_arquivo, destino, dirProParsr, nomePai)
                
    elif tarfile.is_tarfile(arquivo):
        with tarfile.open(arquivo, 'r') as tar_ref:
            tar_ref.extractall(destino)
        novo_nome = os.path.splitext(nomePai)[0]
        for filename in tar_ref.getnames():
            if arquivosValidos(filename):
                caminho_completo = os.path.join(destino, filename)
                extensao_arquivo = os.path.splitext(filename)[1]
                caminho_novo = os.path.join(destino, '{}.{}'.format(novo_nome, extensao_arquivo))
                os.rename(caminho_completo, caminho_novo)
                try:
                    shutil.move(caminho_novo, dirProParsr)
                except shutil.Error:
                    count+=1
                    caminho_novo = '{}_{}'.format(caminho_novo, count)
                    shutil.move(caminho_novo, dirProParsr)
            
            caminho_completo_arquivo = os.path.join(destino, filename)
            if tarfile.is_tarfile(caminho_completo_arquivo):
                extrair_arquivo(caminho_completo_arquivo, destino, dirProParsr, nomePai)
    else:
        print(f'{arquivo} não é um arquivo .zip ou .tar válido')

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
    for arquivo in tqdm(arquivosCandidatos.index):
        nome_uag = arquivosCandidatos['ID-UAG'][arquivo]
        nome_licitacao = arquivosCandidatos['ID-LICITACAO'][arquivo]
        nome_completo = '{}_{}.zip'.format(nome_uag, nome_licitacao)
        caminho_arquivo = os.path.join(SOURCE_DIR, nome_completo)
        shutil.copy(caminho_arquivo, DEST_DIR)
    #dfarquivos.loc[arquivosCandidatos.index, 'processados'] = 1
    
def moveArquivosProcessados(diretorio_origem, diretorio_destino):
    for diretorio_atual, subdiretorios, arquivos in os.walk(diretorio_origem):
        for arquivo in arquivos:
            caminho_origem = os.path.join(diretorio_atual, arquivo)
            caminho_destino = os.path.join(diretorio_destino, arquivo)
            shutil.move(caminho_origem, caminho_destino)

def arquivosValidos(arquivo):
    extensoes_validas = ['.pdf', '.doc', '.docx', '.odt']
    relacao_itens = re.compile('Rela[cç][aã]o', re.IGNORECASE)
    anexo = re.compile('anexo[s]?', re.IGNORECASE)
    if os.path.splitext(arquivo)[1] in extensoes_validas:
        search_relacao_itens = re.search(relacao_itens, os.path.splitext(arquivo)[0])
        search_anexo = re.search(anexo, os.path.splitext(arquivo)[0])
        if search_relacao_itens == None and search_anexo == None:
            return True
    return False
    
def moveArquivosValidos(SOURCE_DIR, DEST_DIR):
    extensoes_validas = ['.pdf', '.doc', '.docx', '.odt']
    relacao_itens = re.compile('Rela[cç][aã]o', re.IGNORECASE)
    anexo = re.compile('anexo[s]?', re.IGNORECASE)
    for diretorio_atual, subdiretorios, arquivos in os.walk(SOURCE_DIR):
        for arquivo in arquivos:
            if os.path.splitext(arquivo)[1] in extensoes_validas:
                busca = re.search(relacao_itens, os.path.splitext(arquivo)[0])
                if busca == None:
                    #print(arquivo)
                    caminho_origem = os.path.join(diretorio_atual, arquivo)
                    caminho_destino = os.path.join(DEST_DIR, arquivo)
                    shutil.move(caminho_origem, caminho_destino)

def main():
    processaArquivos(SOURCE_DIR, DEST_DIR, 100)
    
SOURCE_DIR = '/var/comprasnet_arquivos'
DEST_DIR = '/var/projetos/arquivos'
EXTRACT_DIR = '/var/projetos/arquivosExtraidos'
DIR_PRO_PARSR = '/var/projetos/arquivosProntos'
extracao(DEST_DIR, EXTRACT_DIR, DIR_PRO_PARSR)
#processaArquivos(SOURCE_DIR, DEST_DIR, 100)
#selecionaArquivos(SOURCE_DIR)
#moveArquivosProcessados(PROCESSADOS_DIR, ARQUIVOSPRONTOS_DIR)
#moveArquivosValidos(ARQUIVOSPRONTOS_DIR, PROPARSR_DIR)