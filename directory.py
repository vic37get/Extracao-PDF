OUT_DIR = '/var/projetos/arquivos/'
DIR_PARSR = '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF/teste'
DEST_DIR = '/mnt/c/Users/victor.silva/Documents/Repositórios/Extracao-PDF/teste'

from utils.filename import lista as list_ext
import os
import shutil

def createTreeDir(OUT_DIR, list_ext):
    for i in list_ext:
        if not(os.path.exists(os.path.join(OUT_DIR,'arquivos_'+i[0]))):
            os.makedirs(os.path.join(OUT_DIR,'arquivos_'+i[0]))
        print('arquivos_'+i[0])

def moveMarkdownFiles(DIR_PARSR, DEST_DIR):
    for folder in os.listdir(DIR_PARSR):
        CURRENT_FOLDER = os.path.join(DIR_PARSR, folder)
        for file in os.listdir(CURRENT_FOLDER):
            if file.find('.md') != -1:
                SOURCE = os.path.join(CURRENT_FOLDER, file)
                DESTINATION = os.path.join(DEST_DIR, file)
                shutil.move(SOURCE, DESTINATION)
            else:
                continue

if __name__ == "__main__":
    pass
    #moveMarkdownFiles(DIR_PARSR, DEST_DIR)