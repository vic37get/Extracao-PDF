from lib2to3.pytree import convert
from conexao import conect
from manipulacaoDados import readCsv, getIdArquivo, getIdLicitacao, removeArquivosPDF, saveFile, suppress_stdout
import wget
import magic
from filename import lista as lista_filename
import re
import os
from pathlib import Path
from tqdm import tqdm
from manipulacaoMarkdown import markDownToText, readMarkDownFile
from convertDocAndDocx import docAndDocxToPdf

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
    FAILED_FILES = []
    progress = tqdm(total=len(INPUT_DATAFRAME))
    for file in INPUT_DATAFRAME.index:
        '''if file == 20:
            break'''
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        with suppress_stdout():
            file_pdf = downloadPDF(id_licitacao, id_arquivo)
        if file_pdf != None:
            p = Path(file_pdf)
            if p.suffix.find('.doc')!=-1:
                file_pdf = docAndDocxToPdf(p.name, DIR_ARQUIVOS)
                os.remove(p.name)
                os.chdir(BASE_DIR)
            PDFtoText(file_pdf, id_licitacao, id_arquivo)
        else:
            FAILED_FILES.append('{}-{}\n'.format(id_licitacao, id_arquivo))
        progress.update(1)
    saveFile(FAILED_FILES, 'FailedFiles.txt')
    removeArquivosPDF(DIR_ARQUIVOS)

if __name__ == "__main__":
    #dados = readMarkDownFile('4242-766.md')
    #exto = markDownToText(dados)
    ExtractText(INPUT_DATAFRAME)