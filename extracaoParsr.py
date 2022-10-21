from utils.conexao import conect
from manipulations.manipulationDados import readCsv, getIdArquivo, getIdLicitacao, removeArquivosPDF, saveFile, suppress_stdout, createFolder
import wget
import magic
from utils.filename import lista as lista_filename
import re
import os
from pathlib import Path
from tqdm import tqdm
from conversions.convertDocAndDocx import docAndDocxToPdf
import shutil

BASE_DIR = '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF'
#BASE_DIR = '/home/victor.silva/Extracao-PDF'
DIR_ARQUIVOS = 'arquivos/arquivosPDF'
OUT_DIR = '/var/projetos/arquivos'
INPUT_DATAFRAME = readCsv('lic_2007_2022.csv')

def getExtension(tipo):
    for ext in lista_filename:
        if re.search(ext[1],tipo):
            return ext[0]

def downloadFile(id_licitacao, id_arquivo, OUT_DIR):
    try:
        URL = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/{}/arquivos/{}'.format(id_licitacao, id_arquivo)
        file = wget.download(URL, "{}/{}-{}".format(DIR_ARQUIVOS, id_licitacao, id_arquivo))
        tipo = magic.from_file(file)
        os.rename(file, file+getExtension(tipo))
        file = file+getExtension(tipo)
        NEW_DIR = Path(OUT_DIR).joinpath(createFolder('arquivos_'+getExtension(tipo), OUT_DIR))
        filename = Path(file).name
        NEW_DIR = NEW_DIR.joinpath(filename)
        shutil.move(file, NEW_DIR)
        return file
    except:
        return None

def PDFtoText(arquivoPDF, id_licitacao, id_arquivo):
    parsr = conect()
    parsr.send_document(
        file_path=str(arquivoPDF),
        config_path='./defaultConfig.json',
        document_name='{}-{}'.format(id_licitacao, id_arquivo),
        wait_till_finished=False,
        save_request_id=True,
    )
    return parsr

def ExtractText():
    FAILED_DOWNLOAD, FAILED_CONVERSION, DOC = [],[],[]
    progress = tqdm(total=len(INPUT_DATAFRAME))
    for file in INPUT_DATAFRAME.index:
        if file == 100:
            break
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        with suppress_stdout():
            file_pdf = downloadFile(id_licitacao, id_arquivo)
        file_pdf = downloadFile(id_licitacao, id_arquivo, OUT_DIR)
        if file_pdf != None:
            PDFtoText(file_pdf, id_licitacao, id_arquivo)
            pathPdfFile = Path(file_pdf)
            if pathPdfFile.suffix.find('.doc')!=-1:
                DOC.append('{}-{}\n'.format(id_licitacao, id_arquivo))
                file_pdf = docAndDocxToPdf(pathPdfFile.name, DIR_ARQUIVOS)
                os.remove(pathPdfFile.name)
                os.chdir(BASE_DIR)
            if file_pdf != False:
                PDFtoText(file_pdf, id_licitacao, id_arquivo)
            else:
                FAILED_CONVERSION.append('{}-{}\n'.format(id_licitacao, id_arquivo))
        else:
            FAILED_DOWNLOAD.append('{}-{}\n'.format(id_licitacao, id_arquivo))
        progress.update(1)
    saveFile(FAILED_DOWNLOAD, 'failedDownload.txt')
    saveFile(FAILED_CONVERSION, 'failedConversion.txt')
    saveFile(FAILED_CONVERSION, 'docAndDocxFiles.txt')
    removeArquivosPDF(DIR_ARQUIVOS)

def saveFiles():
    progress = tqdm(total=len(INPUT_DATAFRAME))
    for file in INPUT_DATAFRAME.index:
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        with suppress_stdout():
            file_pdf = downloadFile(id_licitacao, id_arquivo,OUT_DIR)
        progress.update(1)
        removeArquivosPDF(DIR_ARQUIVOS)
        

if __name__ == "__main__":
    #ExtractText()
    saveFiles()
    #PDFtoText('sampleFile.pdf', '111', '222')