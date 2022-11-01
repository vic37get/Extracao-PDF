from pathlib import Path
from tarfile import DIRTYPE
from pandas import read_csv,DataFrame,concat
import re
from tqdm import tqdm

SEARCH_LIST = ['ITEM','PE[CÇ]AS|P[CÇ]S','QTD|QUANT|QUANTIDADE','TIPO','VALOR|VAL|V\..{2,4}','TOTAL|TOT','DES[CÇ]R|DES[CÇ]RI[CÇ][ÃA]O']
#SEARCH_LIST = ['ITEM','PE[CÇ]AS|P[CÇ]S','UNI|UND|UNIDADE','QTD|QUANT|QUANTIDADE','TIPO','VALOR|VAL|V\..{2,4}','TOTAL|TOT','DES[CÇ]R|DES[CÇ]RI[CÇ][ÃA]O']
NEGATIVE = ['Unnamed: \d']
SEARCH_LIST = [re.compile(i,re.IGNORECASE) for i in SEARCH_LIST]
NEGATIVE = [re.compile(i,re.IGNORECASE) for i in NEGATIVE]
VALUES = re.compile('(R$)? ?((\d{1,}[.,]?){1,}(\d{2})?)',re.IGNORECASE)

BASE_PATH = Path('/var/projetos/parsr')

RESULTADO = []

arquivos = list(BASE_PATH.iterdir())
arquivos = [Path('/var/projetos/parsr/128642-68028-b1529ee0ae7c996ed422484c4908fb')]
def filterTables():
    bar = tqdm(total=len(arquivos),desc='FilterTables')
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
        bar.update(1)
    return dfs

def concatTablesEqual():
    list_tabelas = filterTables()
    lista_classificados = []
    bar = tqdm(total=len(list_tabelas),desc='ConcatTablesEqual')
    for tabelas in list_tabelas:
        df,pp,arch = tabelas
        string_columns = ''.join(str(col) for col in df.columns)
        contains = False
        #print(string_columns)
        for regexp in SEARCH_LIST:
            if re.search(regexp,string_columns):
                contains = True
                break
        if not contains:
            for regexp in NEGATIVE:
                if re.search(regexp,string_columns):
                    ...
            line_one = ''.join(str(p_col) for p_col in df.iloc[df.index[0]])
            for regexp in SEARCH_LIST:
                if re.search(regexp,line_one):
                    contains = True
                    break
            if contains:
                df.columns = list(df.iloc[df.index[0]])
                df.drop(index=df.index[0],inplace=True)
            #print('\n\n')
        #print(df.head(2),contains)
        #print('\n\n')
        lista_classificados.append([df,contains,pp,arch])
        bar.update(1)
    return lista_classificados

def map_concat():
    lista_classificados = concatTablesEqual()
    list_to_concat = []
    i = 0
    while(i<len(lista_classificados)):
        prop_head = lista_classificados[i]
        if(prop_head[1]):
            head = prop_head
            bodys = []
            for j in range(i+1,len(lista_classificados)):
                body = lista_classificados[j]
                if not(body[1]) and len(head[0].columns) == len(body[0].columns):
                    bodys.append(body)
                else:
                    break
            #print(head)
            to_concat = [head,bodys]
            list_to_concat.append(to_concat)
        i += 1
    return list_to_concat

def mapper_full():
    list_to_concat = map_concat()
    lista_tabelas_completas = []
    for i in list_to_concat:
        #print(list_to_concat[-2][1])
        colunas = i[0][0].columns
        pp = i[0][2]
        arch = i[0][3]
        head = i[0][0]
        print(head)
        for j in i[1]:
            body = j[0]
            col = DataFrame(list(body.columns)).T
            col.columns = head.columns
            body.columns = head.columns
            try:
                head = concat([head,col,body],axis=0)
            except:
                ...
        lista_tabelas_completas.append([head,pp,arch])
    return lista_tabelas_completas

def calculate():
    lista_tabelas_completas = mapper_full()
    bar = tqdm(total=len(lista_tabelas_completas))
    for elem in lista_tabelas_completas:
        df,pp,arch = elem
        #print(df)
        for col in df.columns:
            #print(col,type(col))
            #if re.search(SEARCH_LIST[5],str(col)):
            if re.search(SEARCH_LIST[5],str(col)):
                #print(col)
                try:
                    valores = df[str(col)].values
                    valores = [re.search(VALUES,valor).groups(1)[1] for valor in valores]
                    valores = [valor[::-1].replace(',','-',1) for valor in valores]
                    valores = [float(valor[::-1].replace('.','').replace('-','.').replace(',','')) for valor in valores]
                    #valores = [float(valor.replace('.','').replace(',','.')) for valor in valores]
                    #print(pp)
                    #print(arch)
                    #print(list(df.columns))
                    #print(valores,sum(valores))
                    ###print(sum(valores))
                    id_licitacao,id_arquivo,arquivo = pp.split('-')
                    csv_id,ord = arch.split('-')[2:]
                    registro = [id_licitacao,id_arquivo,arquivo,csv_id+'-'+ord,sum(valores)]
                    RESULTADO.append(registro)
                    ###print('\n\n')
                except:
                    ...
                ...
        bar.update(1)

calculate()

res = DataFrame(RESULTADO)
res.columns = ['ID-LICITACAO','ID-ARQUIVO','PARSR','ARQUIVO_CSV','TOTAL']
res.to_csv('resultado_t.csv',index=False,sep=',',encoding='utf-8')
