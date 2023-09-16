from utils.conexao import conect
from manipulacao.manipulationFile import getFilename
from manipulacao.manipulationMarkdown import searchMarkDown
from extracoes.directory import getUnprocessedFiles
import os
import shutil
from tqdm.auto import tqdm

DIR_PARSR = '/var/projetos/contratos_md'
FILES_DIR = '/var/projetos/contratos_pncp'
DIR_TEMPFILES = '/var/lib/docker/overlay2/3681346938ef22729a503f92c07cb9fc603e5c917b861800c4d467a2b062d9b6/merged/tmp'

def pdfToText(arquivoPDF, filename):
    parsr = conect()
    print('Processando arquivo: {}'.format(filename))
    parsr.send_document(
        file_path=str(arquivoPDF),
        config_path='./extracoes/defaultConfig.json',
        document_name='{}'.format(filename),
        wait_till_finished=False,
        save_request_id=False,
    )
    return parsr

def removeTempFiles(DIR_TEMPFILES: str) -> None:
    """
    Remove todos os arquivos temporários gerados pelo parsr.
    """
    for file in os.listdir(DIR_TEMPFILES):
        try:
            os.remove(os.path.join(DIR_TEMPFILES, file))
        except IsADirectoryError:
            shutil.rmtree(os.path.join(DIR_TEMPFILES, file))
    print('Arquivos temporários removidos com sucesso!')

def extractTextFromDIR(FILES_DIR, DIR_PARSR):
    files = getUnprocessedFiles(FILES_DIR, DIR_PARSR)
    removeTempFiles(DIR_TEMPFILES)
    list_files = []
    for index, file in enumerate(tqdm(files)):
        if index %30 != 0 or index == 0:
            filename = getFilename(file)
            list_files.append(filename)
            dir_arquivo = os.path.join(FILES_DIR, file)
            pdfToText(dir_arquivo, filename)
        else:
            """
            Verifica se os arquivos foram processados pelo parsr.
            """
            created = False
            while(created == False):
                countMd = 0
                for file_item in list_files:
                    for folder in os.listdir(DIR_PARSR):
                        if folder.find(file_item) != -1 and searchMarkDown(DIR_PARSR, folder) == True:
                            countMd+=1
                            if countMd == 15:
                                created = True
                                #-----------------
                                filename = getFilename(file)
                                dir_arquivo = os.path.join(FILES_DIR, file)
                                pdfToText(dir_arquivo, filename)
                                list_files = []
                                removeTempFiles(DIR_TEMPFILES)
                        else:
                            continue
    
if __name__ == "__main__":
    extractTextFromDIR(FILES_DIR, DIR_PARSR)