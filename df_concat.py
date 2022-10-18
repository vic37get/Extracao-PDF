import pandas as pd

lic_2018_2022 = pd.read_csv('editais_lic_2018_2022.csv',sep=',',encoding='utf-8')
lic_2007_2017 = pd.read_csv('licitacoes_2007_2017.csv',sep=';',encoding='utf-8')

lic_2018_2022.drop(['Unnamed: 0','ID_TIPO_ANEXO', 'ID_MODALIDADE',
       'ID_UNIDADE_GESTORA', 'NOME_ARQUIVO'],axis=1,inplace=True)

lic_2007_2017.drop(['ANO_PROCEDIMENTO'],axis=1,inplace=True)
lic_2007_2017.columns = ['ID_LICITACAO', 'ID_ARQUIVO']

lic_2007_2022 = pd.concat([lic_2007_2017,lic_2018_2022])
lic_2007_2022.to_csv('lic_2007_2022.csv',index=False,encoding='utf-8')