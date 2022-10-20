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