import pandas as pd
import os
from contextlib import contextmanager
import sys

def readCsv(arquivo):
    dados = pd.read_csv(arquivo, sep=',', encoding='utf-8')
    return dados

def getIdArquivo(df, indice):
    return str(int(df.iloc[indice].ID_ARQUIVO))

def getIdLicitacao(df, indice):
    return str(int(df.iloc[indice].ID_LICITACAO))

def removeArquivosPDF(diretorio):
    for arquivo in os.listdir(diretorio):
        if(arquivo.find('.git')) == -1:
            os.remove(os.path.join(diretorio, arquivo))

def saveFile(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for file_failed in data:
            file.write(file_failed)

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def createFolder(NAMEDIR, OUT_DIR):
    DIR = os.path.join(OUT_DIR, NAMEDIR)
    if not os.path.exists(DIR):
        os.mkdir(NAMEDIR)

def concatDF():
    lic_2018_2022 = pd.read_csv('editais_lic_2018_2022.csv',sep=',',encoding='utf-8')
    lic_2007_2017 = pd.read_csv('licitacoes_2007_2017.csv',sep=';',encoding='utf-8')

    lic_2018_2022.drop(['Unnamed: 0','ID_TIPO_ANEXO', 'ID_MODALIDADE',
        'ID_UNIDADE_GESTORA', 'NOME_ARQUIVO'],axis=1,inplace=True)

    lic_2007_2017.drop(['ANO_PROCEDIMENTO'],axis=1,inplace=True)
    lic_2007_2017.columns = ['ID_LICITACAO', 'ID_ARQUIVO']

    lic_2007_2022 = pd.concat([lic_2007_2017,lic_2018_2022])
    lic_2007_2022.to_csv('lic_2007_2022.csv',index=False,encoding='utf-8')

createFolder('teste', '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF')