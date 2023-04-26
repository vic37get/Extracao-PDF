import os
from datetime import datetime
import shutil

SOURCE_DIR = '/var/comprasnet_arquivos'
DEST_DIR = '/var/projetos/arquivosZip'
PROCESSADOS_DIR = '/var/projetos/docsProcessados'

def arquivoInfo(zips_usados, SOURCE_DIR):
    now = datetime.now()
    date_time = now.strftime("%d_%m_%Y")
    diretorio = os.path.join(SOURCE_DIR, 'arquivosDeLog')
    with open('{}/{}.txt'.format(diretorio, date_time), 'w') as f:
        for arquivozip in zips_usados:
            f.write(arquivozip)
    f.close()

def percorreDir(DEST_DIR, SOURCE_DIR, quantidade):
    zips_usados = []
    for indice, arquivo in enumerate(os.listdir(SOURCE_DIR)):
        print(indice)
        zips_usados.append(arquivo)
        sourc_arquivo = os.path.join(SOURCE_DIR, arquivo)
        print(sourc_arquivo)
        dest_arquivo = os.path.join(DEST_DIR, arquivo)
        print(dest_arquivo)
        try:
            shutil.copy(sourc_arquivo, DEST_DIR)
        except shutil.SameFileError:
            print('Arquivo já existe')
        except PermissionError:
            print('Permissão negada')
        except:
            print('Ocorreu um erro!')
        if indice == quantidade:
            arquivoInfo(zips_usados, SOURCE_DIR)
            return

def moveArquivosProcessados(SOURCE_DIR, DEST_DIR):
    for indice, arquivo in enumerate(os.listdir(SOURCE_DIR)):
        print(indice)
        extensao = os.path.splitext(arquivo)[1]
        print(extensao)
        filepath = os.path.join(SOURCE_DIR, arquivo)
        print('CAMINHO: ',filepath)
        print('DESTINO: ', DEST_DIR)
        if extensao == '.doc' or extensao == '.DOC' or extensao == '.docx':
            print('é doc', arquivo)
            print(DEST_DIR)
            #shutil.move(filepath, DEST_DIR)
    
        
percorreDir(DEST_DIR, SOURCE_DIR, 10000)
#moveArquivosProcessados(SOURCE_DIR, PROCESSADOS_DIR)