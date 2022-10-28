OUT_DIR = '/var/projetos/arquivos/'
DIR_PARSR = '/var/projetos/parsr'
#DIR_PARSR = './teste'
DEST_DIR = '/var/projetos/arquivos_md'
#DEST_DIR = '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF/teste'
FILES_DIR = '/var/projetos/arquivos/arquivos_.pdf'

from utils.filename import lista as list_ext
import os
import shutil
from tqdm import tqdm

def createTreeDir(OUT_DIR, list_ext):
    for i in list_ext:
        if not(os.path.exists(os.path.join(OUT_DIR,'arquivos_'+i[0]))):
            os.makedirs(os.path.join(OUT_DIR,'arquivos_'+i[0]))
        print('arquivos_'+i[0])

def moveMarkdownFiles(DIR_PARSR, DEST_DIR):
    folders = os.listdir(DIR_PARSR)
    progress = tqdm(total=len(folders), desc='Movendo arquivos Markdown...')
    for folder in folders:
        CURRENT_FOLDER = os.path.join(DIR_PARSR, folder)
        for file in os.listdir(CURRENT_FOLDER):
            if file.find('.md') != -1:
                SOURCE = os.path.join(CURRENT_FOLDER, file)
                DESTINATION = os.path.join(DEST_DIR, file)
                #shutil.move(SOURCE, DESTINATION)
                shutil.copy(SOURCE, DESTINATION)
            else:
                continue
        progress.update(1)

def getUnprocessedFiles(FILES_DIR, DIR_PARSR):
    candidate_files = []
    files = os.listdir(FILES_DIR)
    progress = tqdm(total=len(files), desc='Obtendo arquivos não processados...')
    for file in files:
        file_exist = False
        filename = file.split('.')[0]
        for folder in os.listdir(DIR_PARSR):
            if folder.find(filename) != -1:
                file_exist = True
        if file_exist == False:
            candidate_files.append(file)
        progress.update(1)
    return candidate_files

if __name__ == "__main__":
    pass
    #getUnprocessedFiles(FILES_DIR, DIR_PARSR)
    #moveMarkdownFiles(DIR_PARSR, DEST_DIR)