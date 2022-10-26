from pathlib import Path
from tarfile import DIRTYPE
from pandas import read_csv,DataFrame
import re
from tqdm import tqdm

SEARCH_LIST = ['ITEM','PE[CÇ]AS|P[CÇ]S','UNI|UND|UNIDADE','QTD|QUANT|QUANTIDADE','TIPO','VALOR|VAL|V\..{2,4}','TOTAL|TOT','DES[CÇ]R|DES[CÇ]RI[CÇ][ÃA]O']
SEARCH_LIST = [re.compile(i,re.IGNORECASE) for i in SEARCH_LIST]
VALUES = re.compile('(R$)? ?((\d{1,}\.)*\d{1,},\d{0,2})',re.IGNORECASE)

BASE_PATH = Path('/var/projetos/parsr')

RESULTADO = []

arquivos = BASE_PATH.iterdir()
arquivos = [Path('/var/projetos/parsr/407000-416723-ba4ab45426b7d512ac625726b7889c')]
def filterTables():
    dfs = []
    for posixPath in arquivos:
        csvGlob = posixPath.rglob('*.csv')
        for csvArch in sorted(csvGlob):
            df = read_csv(csvArch,encoding='utf-8',sep=';')
            df.dropna(inplace=True)
            #ponto para return
            if len(df)!=0:
                dfs.append([df,posixPath.stem,csvArch.stem])
                #print(df.iloc[-1],'\n\n')
    return dfs

for ind,tabelas in enumerate(filterTables()):
    df,pp,arch = tabelas
    string_columns = ''.join(str(col) for col in df.columns)
    contains = False
    for regexp in SEARCH_LIST:
        if re.search(regexp,string_columns):
            contains = True
            break
    if contains and len(df)!=0:
        #print(df.head(),len(df))
        for col in df.columns:
            if re.search(SEARCH_LIST[6],col):
                valores = df[col].values
                try:
                    valores = [re.search(VALUES,valor).groups(1)[1] for valor in valores]
                    valores = [float(valor.replace('.','').replace(',','.')) for valor in valores]
                    ##print(posixPath.stem)
                    ##print(csvArch.stem)
                    #print(list(df.columns))
                    #print(valores,sum(valores))
                    ###print(sum(valores))
                    registro = [pp,arch,sum(valores)]
                    RESULTADO.append(registro)
                    ###print('\n\n')
                except:
                    ...

res = DataFrame(RESULTADO)
res.columns = ['LICITACAO','ARQUIVO_CSV','PREVISAO_TOTAL_CALCULADO']
res.to_csv('resultado_.csv',index=False,sep=';',encoding='utf-8')
read_csv('resultado_.csv',sep=';').to_csv('resultado_.csv',index=False,sep=',')