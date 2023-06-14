import os
import time
import shutil
import re
import pandas as pd
import zipfile
import tarfile
from tqdm.auto import tqdm

def time_stamp():
    return time.time() * 1000

def extracao(SOURCE_DIR, DEST_DIR, DIR_PRO_PARSR):
    for arquivo in tqdm(os.listdir(SOURCE_DIR)):
        caminho_completo_arquivo = os.path.join(SOURCE_DIR, arquivo)
        if os.path.isfile(caminho_completo_arquivo):
            extrair_arquivo(caminho_completo_arquivo, DEST_DIR, DIR_PRO_PARSR, arquivo)
            
def extrair_arquivo(arquivo, destino, dirProParsr, nomePai):
    if zipfile.is_zipfile(arquivo):
        try:
            with zipfile.ZipFile(arquivo, 'r') as zip_ref:
                zip_ref.extractall(destino)
        except:
            print(f'{arquivo} não é um arquivo zip válido.')
            return
        novo_nome = os.path.splitext(nomePai)[0]
        for filename in zip_ref.namelist():
            if arquivosValidos(filename):
                caminho_completo = os.path.join(destino, filename)
                extensao_arquivo = os.path.splitext(filename)[1]
                caminho_novo = os.path.join(destino, '{}{}'.format(novo_nome, extensao_arquivo))
                try:
                    os.rename(caminho_completo, caminho_novo)
                except FileNotFoundError:
                    continue
                try:
                    shutil.move(caminho_novo, dirProParsr)
                except shutil.Error:
                    nomeIncrementado = '{}_{}'.format(novo_nome, time_stamp())
                    arquivoNaoDuplicado = os.path.join(destino, '{}{}'.format(nomeIncrementado, extensao_arquivo))
                    os.rename(caminho_novo, arquivoNaoDuplicado)
                    shutil.move(arquivoNaoDuplicado, dirProParsr)
                    
            caminho_completo_arquivo = os.path.join(destino, filename)
            if zipfile.is_zipfile(caminho_completo_arquivo):
                extrair_arquivo(caminho_completo_arquivo, destino, dirProParsr, nomePai)
                
    elif tarfile.is_tarfile(arquivo):
        count+=1
        try:
            with tarfile.open(arquivo, 'r') as tar_ref:
                tar_ref.extractall(destino)
        except:
            print(f'{arquivo} não é um arquivo tar válido.')
            return
        novo_nome = os.path.splitext(nomePai)[0]
        for filename in tar_ref.getnames():
            count+=1
            if arquivosValidos(filename):
                caminho_completo = os.path.join(destino, filename)
                extensao_arquivo = os.path.splitext(filename)[1]
                caminho_novo = os.path.join(destino, '{}.{}'.format(novo_nome, extensao_arquivo))
                try:
                    os.rename(caminho_completo, caminho_novo)
                except FileNotFoundError:
                    continue
                try:
                    shutil.move(caminho_novo, dirProParsr)
                except shutil.Error:
                    nomeIncrementado = '{}_{}'.format(novo_nome, time_stamp())
                    arquivoNaoDuplicado = os.path.join(destino, '{}.{}'.format(nomeIncrementado, extensao_arquivo))
                    os.rename(caminho_novo, arquivoNaoDuplicado)
                    shutil.move(arquivoNaoDuplicado, dirProParsr)
                    
            caminho_completo_arquivo = os.path.join(destino, filename)
            if zipfile.is_zipfile(caminho_completo_arquivo):
                extrair_arquivo(caminho_completo_arquivo, destino, dirProParsr, nomePai)
    else:
        print(f'{arquivo} não é um arquivo .zip ou .tar válido')

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
    for arquivo in os.listdir(SOURCE_DIR):
        lista_nomes.append(arquivo)
    cod_uags, cod_licitacoes = getNomeArquivo(lista_nomes)
    geraDataFrameNomes(cod_uags, cod_licitacoes)

def processaArquivos(SOURCE_DIR, DEST_DIR, quantidade):
    dfarquivos = pd.read_csv('datasets/arquivosZip.csv')
    arquivosCandidatos = dfarquivos.loc[dfarquivos['processados'] != 1].head(quantidade)
    for arquivo in tqdm(arquivosCandidatos.index):
        nome_uag = arquivosCandidatos['ID-UAG'][arquivo]
        nome_licitacao = arquivosCandidatos['ID-LICITACAO'][arquivo]
        try:
            nome_completo = '{}_{}.zip'.format(nome_uag, nome_licitacao)
            caminho_arquivo = os.path.join(SOURCE_DIR, nome_completo)
            shutil.copy(caminho_arquivo, DEST_DIR)
        except:
            pass
    dfarquivos.loc[arquivosCandidatos.index, 'processados'] = 1
    dfarquivos.to_csv('datasets/arquivosZip.csv', index=False, encoding='utf-8')

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
    
def main():
    #processaArquivos(SOURCE_DIR, DEST_DIR, 50000)
    extracao(DEST_DIR, EXTRACT_DIR, DIR_PRO_PARSR)
    
SOURCE_DIR = '/var/comprasnet_arquivos'
DEST_DIR = '/var/projetos/arquivos'
EXTRACT_DIR = '/var/projetos/arquivosExtraidos'
DIR_PRO_PARSR = '/var/projetos/arquivosProntos'
main()