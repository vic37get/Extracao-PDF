from operator import index
import requests
import re
from pathlib import Path

ext_set = set()
def getExt(id_licitacao, id_arquivo):
    URL = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/{}/arquivos/{}'.format(id_licitacao, id_arquivo) 
    response = requests.get(URL)
    content_dis = dict(response.headers)['content-disposition']
    extension = Path(re.sub('.*;.{0,2}filename=','',content_dis).replace('"',''))
    if(extension.suffix == ''):
        ext_set.add('No-Extension')
    else:
        if(extension.suffix == '.docx'):
            print(id_licitacao, id_arquivo)
        ext_set.add(extension.suffix)
    #print(content_dis,extension)

import pandas as pd

lics = pd.read_csv('lic_2007_2022.csv',encoding='utf-8',sep=',')

for i in lics.itertuples():
    if(i.Index>200):
        break
    getExt(i.ID_LICITACAO,i.ID_ARQUIVO)
print(ext_set)