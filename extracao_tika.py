# -*- coding: utf-8 -*-
"""
Created on Fri May 31 19:07:32 2022

@author: jasson.silva
"""
#%% dependencies
import os
os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'
from tika import parser
import pandas as pd
import time
import datetime
#%%  converter function
def pdf2txt(url):
    time.sleep(2)
    raw = parser.from_file(url)
    content = raw['content']
    try:
        counter = content.replace(" ","")
        if(len(counter)>0):
            print('\nSucesso, tamanho arquivo:',len(counter),'caracteres')
        else:
            print('\nFracasso',0,'caracteres')
    except:
        print('\nFracasso: (NoneType)')
        
    return content
#%%
def saveFile(arq_dest,raw,url,encoding='utf-8',formatFile =True):
    list_error = []
    with open(arq_dest,'w',encoding=encoding) as out_file:
        print('Destino: ',arq_dest+'\n\n')
        try:
            if formatFile:
                lines = splitLine(raw)
                for i in lines:
                    out_file.writelines(i+'\n')
            else:
                out_file.write(raw)
        except:
            list_error.append(url)
    out_file.close()
    return list_error
    
def splitLine(content):
    lines = content.split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()
        lines[i] = lines[i].replace("  ", "")
    while '' in lines: lines.remove('')
    return lines
#%% save file.txt
df = pd.read_csv('arquivos/editais_lic_2018_2022.csv')
DEST = 'arquivos/txt_editais2'

list_error = []
start_time = time.time()
for i in df.index: 
    if i > 30:
        break
    id_licitacao = str(int(df.iloc[i].ID_LICITACAO))
    id_arquivo = str(int(df.iloc[i].ID_ARQUIVO))
    print('\nConvertendo edital: '+df.iloc[i].NOME_ARQUIVO+' Codigo:'+id_licitacao+'-'+id_arquivo+'\n')
    url = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/'+id_licitacao+'/arquivos/'+id_arquivo
    arq_dest = DEST+'/'+id_licitacao+'-'+id_arquivo+'.txt'
    raw = pdf2txt(url)
    if raw == None:
        list_error.append(url)
    else:
        list_error.extend(saveFile(arq_dest,raw,url,encoding='utf-8',formatFile =False))
print("Tempo de execução: %s " % str(datetime.timedelta(seconds=(time.time() - start_time))))

with open('conversao_erro.txt','w',encoding='utf-8') as file:
    for i in list_error:
        file.writelines(i+'\n')
    file.close()
#%%  teste isolado
url = 'https://sistemas.tce.pi.gov.br/muralic/api/licitacoes/440610/arquivos/437718'
raw = parser.from_file(url)
content = raw['metadata']
with open('arq.txt', 'w', encoding='utf-8') as f:
    f.write(str(content))
print('content',content)

# %%
