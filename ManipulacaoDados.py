import pandas as pd
import os

def readCsv(arquivo):
    dados = pd.read_csv(arquivo, sep=',', encoding='utf-8')
    return dados

def getIdArquivo(df, indice):
    return str(int(df.iloc[indice].ID_ARQUIVO))

def getIdLicitacao(df, indice):
    return str(int(df.iloc[indice].ID_LICITACAO))

def removeArquivosPDF(diretorio):
    for arquivo in os.listdir(diretorio):
        os.remove(os.path.join(diretorio, arquivo))

def saveFile(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for file_failed in data:
            file.write(file_failed)
