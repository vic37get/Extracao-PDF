import os
from tqdm.auto import tqdm
import shutil

SOURCE_DIR = '/var/projetos/arquivosProntos'
DEST_DIR = '/var/projetos/arquivosProntosDoc'

def moveArqsDocs(SOURCE_DIR, DEST_DIR):
    for arquivo in tqdm(os.listdir(SOURCE_DIR)):
        #print(os.path.splitext(arquivo)[1])
        if os.path.splitext(arquivo)[1] == '.doc' or os.path.splitext(arquivo)[1] == '.odt':
            caminho_origem = os.path.join(SOURCE_DIR, arquivo )
            caminho_destino = os.path.join(DEST_DIR, arquivo)
            try:
                shutil.move(caminho_origem, caminho_destino)
            except shutil.Error:
                pass
        
moveArqsDocs(SOURCE_DIR, DEST_DIR)