import subprocess
import os
from tqdm.auto import tqdm

SOURCE_DIR = '/var/projetos/arquivosProntosDoc'
DEST_DIR = '/var/projetos/arquivosProntos'

#.doc para docx
def doc_to_docx(doc_file_path, docx_file_path):
    command = ['unoconv', '-f', 'docx', '-o', docx_file_path, doc_file_path]
    subprocess.run(command)

def converteArquivos(SOURCE_DIR, DEST_DIR):
    for arquivo in tqdm(os.listdir(SOURCE_DIR)):
        caminho_fonte = os.path.join(SOURCE_DIR, arquivo)
        caminho_destino = os.path.join(DEST_DIR, arquivo)
        doc_to_docx(caminho_fonte, caminho_destino)

converteArquivos(SOURCE_DIR, DEST_DIR)
        
        