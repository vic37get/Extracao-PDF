import pandas as pd
import os


def readCsv(arquivo):
    dados = pd.read_csv(arquivo, sep=';', encoding='utf-8')
    return dados

def getIdArquivo(df, indice):
    return str(int(df.iloc[indice].ID_ARQUIVO))

def getIdLicitacao(df, indice):
    return str(int(df.iloc[indice].ID_LICITACAO))
