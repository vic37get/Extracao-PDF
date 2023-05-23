import wget
import magic
import shutil
from utils.filename import lista as filename_list
from tqdm import tqdm
from manipulacao.manipulationFile import *
import os
from pathlib import Path

INPUT_DATAFRAME = readCsv('licitacoes-2023.csv')
DIR_ARQUIVOS = '/var/projetos/DIR_ARQUIVOS'
OUT_DIR = '/var/projetos/OUT_DIR'

def downloadFile(id_licitacao, id_arquivo, OUT_DIR, DIR_ARQUIVOS):
    try:
        URL = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/{}/arquivos/{}'.format(id_licitacao, id_arquivo)
        file = wget.download(URL, "{}/{}-{}".format(DIR_ARQUIVOS, id_licitacao, id_arquivo))
        file_type = magic.from_file(file)
        os.rename(file, file+getExtension(file_type, filename_list))
        file = file+getExtension(file_type, filename_list)
        #---------
        NEW_DIR = Path(OUT_DIR).joinpath(createFolder('arquivos_'+getExtension(file_type, filename_list), OUT_DIR))
        filename = Path(file).name
        NEW_DIR = NEW_DIR.joinpath(filename)
        shutil.move(file, NEW_DIR)
        return file
    except:
        return None

def downloadFiles(INPUT_DATAFRAME, OUT_DIR, DIR_ARQUIVOS):
    progress = tqdm(total=len(INPUT_DATAFRAME))
    for file in INPUT_DATAFRAME.index:
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        with suppress_stdout():
            downloadFile(id_licitacao, id_arquivo, OUT_DIR, DIR_ARQUIVOS)
        progress.update(1)
        removeArquivosPDF(DIR_ARQUIVOS)

if __name__ == "__main__":
    downloadFiles(INPUT_DATAFRAME, OUT_DIR, DIR_ARQUIVOS)
    pass