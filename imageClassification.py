import fitz
import pandas as pd
import numpy as np
from pathlib import Path

from extracaoParsr import INPUT_DATAFRAME,DIR_ARQUIVOS,downloadPDF,removeArquivosPDF
from manipulacaoDados import getIdArquivo,getIdLicitacao
from tqdm import tqdm

def classifier(pdf_file):
    with open(pdf_file,"rb") as f:
        pdf = fitz.open(f)
        res = []
        for page in pdf:
            image_area = 0.0
            text_area = 0.0
            for b in page.get_text("blocks"):
                if '<image:' in b[4]:
                    #print(b)
                    r = fitz.Rect(b[:4])
                    #print(r)
                    image_area = image_area + abs(r)
                else:
                    r = fitz.Rect(b[:4])
                    text_area = text_area + abs(r)
            total_area = image_area+text_area
            if(total_area==0):
                res.append(-2)
                continue
            image_percent = image_area/total_area*100
            text_percent = text_area/total_area*100
            if(image_percent>75):
                res.append(0)
            elif(text_percent>75):
                res.append(1)
            else:
                res.append(-1)
        return res

def classifier_pdf(file_path):
    classifier_result = classifier(file_path)
    classifier_result =  np.asarray(classifier_result)
    counts = np.unique(classifier_result,return_counts=True)
    total = np.sum(counts[1])
    ind = 1
    entry = False
    for i,j in zip(counts[0],counts[1]):
        if j/total > 0.65:
            ind = i
            entry = True
    if(not(entry)):
        ind = -1
    return ind
    
from contextlib import contextmanager
import sys, os
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

OUTPUT_TYPE_DATAFRAME = './tipos.csv'
def saveData(save=True):
    result = []
    progress = tqdm(total=len(INPUT_DATAFRAME))
    for file in INPUT_DATAFRAME.index:
        if(file>4000):
            break
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        progress.update(1)
        with suppress_stdout():
            file_pdf = downloadPDF(id_licitacao, id_arquivo)
        if file_pdf == None:
            continue
        if Path(file_pdf).suffix != '.pdf':
            removeArquivosPDF(DIR_ARQUIVOS)
            continue
        type_pdf = classifier_pdf(file_pdf)
        if(type_pdf==0):
            result.append([id_licitacao,id_arquivo,'image'])
            ...
        if(type_pdf==1):
            result.append([id_licitacao,id_arquivo,'text'])
            ...
        if(type_pdf==-1):
            result.append([id_licitacao,id_arquivo,'half'])
            ...
        if(type_pdf==-2):
            result.append([id_licitacao,id_arquivo,'empty'])
            ...
        removeArquivosPDF(DIR_ARQUIVOS)
    if save:
        df = pd.DataFrame(result)
        df.columns = ['ID-LICITACAO','ID-ARQUIVO','TIPO']
        df.to_csv(OUTPUT_TYPE_DATAFRAME,index=False,sep=',')
            
saveData()