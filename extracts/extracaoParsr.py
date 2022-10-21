from utils.conexao import conect
from manipulations.manipulationDados import readCsv, getIdArquivo, getIdLicitacao, removeArquivosPDF, saveFile, suppress_stdout
import wget
import magic
from utils.filename import lista as lista_filename
import re
import os
from pathlib import Path
from tqdm import tqdm
from manipulations.manipulationMarkdown import markDownToText, readMarkDownFile
from conversions.convertDocAndDocx import docAndDocxToPdf

BASE_DIR = '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF'
DIR_ARQUIVOS = 'arquivos/arquivosPDF'
DIR_DESTINO = 'arquivos/arquivosTXT'
INPUT_DATAFRAME = readCsv('lic_2007_2022.csv')

def getExtension(tipo):
    for ext in lista_filename:
        if re.search(ext[1],tipo):
            return ext[0]

def downloadPDF(id_licitacao, id_arquivo):
    URL = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/{}/arquivos/{}'.format(id_licitacao, id_arquivo)
    try:
        arquivoPDF = wget.download(URL, "{}/{}-{}".format(DIR_ARQUIVOS, id_licitacao, id_arquivo))
        tipo = magic.from_file(arquivoPDF)
        os.rename(arquivoPDF, arquivoPDF+getExtension(tipo))
        arquivoPDF = arquivoPDF+getExtension(tipo)
        #print('\nDownload da licitação {}, arquivo {} realizado!'.format(id_licitacao, id_arquivo))
        return arquivoPDF
    except:
        print('\nErro ao realizar o download da licitação {}, arquivo {}!'.format(id_licitacao, id_arquivo))
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

def ExtractText(INPUT_DATAFRAME):
    FAILED_DOWNLOAD, FAILED_CONVERSION = [], []
    progress = tqdm(total=len(INPUT_DATAFRAME))
    for file in INPUT_DATAFRAME.index:
        '''if file == 20:
            break'''
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        with suppress_stdout():
            file_pdf = downloadPDF(id_licitacao, id_arquivo)
        if file_pdf != None:
            pathPdfFile = Path(file_pdf)
            if pathPdfFile.suffix.find('.doc')!=-1:
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
    removeArquivosPDF(DIR_ARQUIVOS)

if __name__ == "__main__":
    ExtractText(INPUT_DATAFRAME)