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
DIR_PARSR = '/var/projetos/parsr'
#BASE_DIR = '/home/victor.silva/Extracao-PDF'
DIR_ARQUIVOS = 'arquivos/arquivosPDF'
OUT_DIR = '/var/projetos/arquivos'
#DIR_PDFS = '/var/projetos/arquivos/arquivos_.pdf'
DIR_PDFS = '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF/teste'
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

def pdfToText(arquivoPDF, id_licitacao, id_arquivo):
    parsr = conect()
    parsr.send_document(
        file_path=str(arquivoPDF),
        config_path='./defaultConfig.json',
        document_name='{}-{}'.format(id_licitacao, id_arquivo),
        wait_till_finished=False,
        save_request_id=False,
    )
    return parsr

def extractText():
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
            pdfToText(file_pdf, id_licitacao, id_arquivo)
            pathPdfFile = Path(file_pdf)
            if pathPdfFile.suffix.find('.doc')!=-1:
                DOC.append('{}-{}\n'.format(id_licitacao, id_arquivo))
                file_pdf = docAndDocxToPdf(pathPdfFile.name, DIR_ARQUIVOS)
                os.remove(pathPdfFile.name)
                os.chdir(BASE_DIR)
            if file_pdf != False:
                pdfToText(file_pdf, id_licitacao, id_arquivo)
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
            downloadFile(id_licitacao, id_arquivo,OUT_DIR)
        progress.update(1)
        removeArquivosPDF(DIR_ARQUIVOS)

def getFilename(arquivo):
    filename = arquivo.split('.')[0]
    return filename

def getIds(filename):
    file = filename.split('-')       
    id_licitacao = file[0]
    id_arquivo = file[1]
    return id_licitacao, id_arquivo

def extractTextFromDIR(DIR, raiz):
    arquivos = os.listdir(DIR)
    progress = tqdm(total=len(arquivos))
    list_files = []
    for index, arquivo in enumerate(arquivos):
        if index %15 != 0 or index == 0:
            filename = getFilename(arquivo)
            list_files.append(filename)
            id_licitacao, id_arquivo = getIds(filename)
            dir_arquivo = os.path.join(DIR, arquivo)
            pdfToText(dir_arquivo, id_licitacao, id_arquivo)

        else:
            created = False
            while(created == False):
                countMd = 0
                for file in list_files:
                    for folder in os.listdir(raiz):
                        if folder.find(file) != -1 and searchMarkDown(raiz, folder) == True:
                            countMd+=1
                            if countMd >=14:
                                created = True
                                #-----------------
                                filename = getFilename(arquivo)
                                id_licitacao, id_arquivo = getIds(filename)
                                dir_arquivo = os.path.join(DIR, arquivo)
                                pdfToText(dir_arquivo, id_licitacao, id_arquivo)
                                list_files = []
                        else:
                            continue
        progress.update(1)

def searchMarkDown(raiz, folder):
    for j in os.listdir(os.path.join(raiz, folder)):
        if j.find('.md') != -1:
            return True
    return False

if __name__ == "__main__":
    extractTextFromDIR(DIR_PDFS, DIR_PARSR)
    #ExtractText()
    #saveFiles()
    #PDFtoText('386221-416852.pdf', '111', '222')