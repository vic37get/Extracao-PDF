from utils.conexao import conect
from manipulations.manipulationFile import *
from manipulations.manipulationMarkdown import *
from conversions.convertDocAndDocx import *
from downloadFile import *
import os
from pathlib import Path
from tqdm import tqdm

BASE_DIR = '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF'
DIR_PARSR = '/var/projetos/parsr'
#BASE_DIR = '/home/victor.silva/Extracao-PDF'
DIR_ARQUIVOS = 'arquivos/arquivosPDF'
OUT_DIR = '/var/projetos/arquivos'
#FILES_DIR = '/var/projetos/arquivos/arquivos_.pdf'
FILES_DIR = '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF/teste'
INPUT_DATAFRAME = readCsv('lic_2007_2022.csv')

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

def extractText(INPUT_DATAFRAME, OUT_DIR, DIR_ARQUIVOS, BASE_DIR):
    FAILED_DOWNLOAD, FAILED_CONVERSION, DOC = [],[],[]
    progress = tqdm(total=len(INPUT_DATAFRAME))
    for file in INPUT_DATAFRAME.index:
        #if file == 100:
            #break
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        with suppress_stdout():
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

def extractTextFromDIR(FILES_DIR, DIR_PARSR):
    files = os.listdir(FILES_DIR)
    progress = tqdm(total=len(files))
    list_files = []
    for index, file in enumerate(files):
        #if index == 2:
            #break
        if index %30 != 0 or index == 0:
            filename = getFilename(file)
            list_files.append(filename)
            id_licitacao, id_arquivo = getIds(filename)
            dir_arquivo = os.path.join(FILES_DIR, file)
            pdfToText(dir_arquivo, id_licitacao, id_arquivo)

        else:
            created = False
            while(created == False):
                countMd = 0
                for file_item in list_files:
                    for folder in os.listdir(DIR_PARSR):
                        if folder.find(file_item) != -1 and searchMarkDown(DIR_PARSR, folder) == True:
                            countMd+=1
                            if countMd >=15:
                                created = True
                                #-----------------
                                filename = getFilename(file)
                                id_licitacao, id_arquivo = getIds(filename)
                                dir_arquivo = os.path.join(FILES_DIR, file)
                                pdfToText(dir_arquivo, id_licitacao, id_arquivo)
                                list_files = []
                        else:
                            continue
        progress.update(1)
    
if __name__ == "__main__":
    extractTextFromDIR(FILES_DIR, DIR_PARSR)
    #ExtractText()
    #downloadFiles()
    #PDFtoText('386221-416852.pdf', '111', '222')