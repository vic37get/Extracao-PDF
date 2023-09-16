from parsr_client import ParsrClient as client
import os
from tqdm.auto import tqdm
import shutil
import time

def conect():
   parsr = client('localhost:3001')
   return parsr

def sendToParsr(fileDir: str, filename: str, parsr: client) -> client:
    """
    Envia um arquivo para o servidor parsr, para o texto ser extraido.
    """
    print('Processando arquivo: {}'.format(filename))
    parsr.send_document(
        file_path=fileDir,
        config_path='./defaultConfig.json',
        document_name=filename,
        wait_till_finished=False,
        save_request_id=False,
        refresh_period=2
    )
    return parsr

def searchMarkDown(folder: str) -> bool:
    """
    Verifica se existe um arquivo .md no diretório.
    """
    for file in os.listdir(folder):
        if file.endswith('.md'):
            return True
        else:
            continue
    return False

def removeDirectory(folder: str) -> None:
    """
    Remove um diretório e todos os seus arquivos.
    """
    try:
        os.rmdir(folder)
    except OSError:
        shutil.rmtree(folder)

def getUnprocessedFiles(filesDir: str, dirParsr: str) -> list:
    """
    Retorna uma lista com os arquivos que ainda não foram processados pelo parsr.
    """
    candidateFiles = []
    for file in tqdm(os.listdir(filesDir), desc='Obtendo arquivos não processados'):
        file_exists = False
        filename = os.path.splitext(file)[0]
        for folder in os.listdir(dirParsr):
            # Se encontrar a pasta referente ao nome do arquivo.
            if folder.find(filename) != -1:
                # Se encontrar um arquivo .md nela.
                if searchMarkDown(os.path.join(dirParsr, folder)):
                    file_exists = True
                    break
                else:
                    # Se não encontrar, remover a pasta para reprocessar.
                    removeDirectory(os.path.join(dirParsr, folder))
            else:
                continue
        if file_exists == False:
            candidateFiles.append(file)
    return candidateFiles

def verifyProcessed(dirParsr: str, filename: str) -> bool:
    """
    Verifica se um arquivo já foi processado pelo parsr.
    """
    for folder in os.listdir(dirParsr):
        if folder.find(filename) != -1 and searchMarkDown(os.path.join(dirParsr, folder)) == True:
            return True
        else:
            continue
    return False

def removeTempFiles(dirTempFiles: str) -> None:
    """
    Remove todos os arquivos temporários gerados pelo parsr.
    """
    for file in os.listdir(dirTempFiles):
        try:
            os.remove(os.path.join(dirTempFiles, file))
        except IsADirectoryError:
            try:
                os.rmdir(os.path.join(dirTempFiles, file))
            except OSError:
                shutil.rmtree(os.path.join(dirTempFiles, file))
    print('Arquivos temporários removidos com sucesso!')

def main() -> None:
    filesDir = '/var/projetos/contratos_pncp'
    dirParsr = '/var/projetos/contratos_md'
    dirTmpFiles = '/var/lib/docker/overlay2/3681346938ef22729a503f92c07cb9fc603e5c917b861800c4d467a2b062d9b6/merged/tmp'

    parsr = conect()
    files = getUnprocessedFiles(filesDir, dirParsr)
    for file in tqdm(files, desc='Processando arquivos'):
        removeTempFiles(dirTmpFiles)
        filename = os.path.splitext(file)[0]
        fileDir = os.path.join(filesDir, file)
        sendToParsr(fileDir, filename, parsr)
        inicio = time.time()
        while True:
            fim = time.time()
            if verifyProcessed(dirParsr, filename) == True or (fim - inicio) > 600:
                break
            else:
                continue

if __name__ == "__main__":
    main()
