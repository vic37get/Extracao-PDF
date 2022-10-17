#from conexao import conect
from ManipulacaoDados import readCsv, getIdArquivo, getIdLicitacao
import wget
import os

DIR_ARQUIVOS = 'arquivos/arquivosPDF'
DIR_DESTINO = 'arquivos/arquivosTXT'
INPUT_DATAFRAME = readCsv('editais_lic_tika.csv')

#parsr = conect()

id_arquivo = getIdArquivo(INPUT_DATAFRAME, 1)
id_licitacao = getIdLicitacao(INPUT_DATAFRAME, 1)

URL = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/{}/arquivos/{}'.format(id_licitacao, id_arquivo)

try:
    response = wget.download(URL, "{}/arquivo.pdf".format(DIR_ARQUIVOS))
    print('Download da licitação {}, arquivo {} realizado!'.format(id_licitacao, id_arquivo))
except:
    print('Erro ao realizar o download da licitação {}, arquivo {}!'.format(id_licitacao, id_arquivo))

'''
parsr.send_document(
    file_path='./exemplo2.pdf',
    config_path='./defaultConfig.json',
    document_name='Sample File2',
    wait_till_finished=False,
    save_request_id=True,
)
'''

print('Processamento executado!')
print(response)

os.remove("{}/arquivo.pdf".format(DIR_ARQUIVOS))

