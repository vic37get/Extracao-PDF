from conexao import conect
from ManipulacaoDados import readCsv, getIdArquivo, getIdLicitacao, removeArquivosPDF
import wget

DIR_ARQUIVOS = 'arquivos/arquivosPDF'
DIR_DESTINO = 'arquivos/arquivosTXT'
INPUT_DATAFRAME = readCsv('editais_lic_tika.csv')

parsr = conect()

id_arquivo = getIdArquivo(INPUT_DATAFRAME, 1)
id_licitacao = getIdLicitacao(INPUT_DATAFRAME, 1)

URL = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/{}/arquivos/{}'.format(id_licitacao, id_arquivo)

try:
    arquivoPDF = wget.download(URL, "{}/{}-{}.pdf".format(DIR_ARQUIVOS, id_licitacao, id_arquivo))
    print('\nDownload da licitação {}, arquivo {} realizado!'.format(id_licitacao, id_arquivo))
except:
    print('\nErro ao realizar o download da licitação {}, arquivo {}!'.format(id_licitacao, id_arquivo))


parsr.send_document(
    file_path='190518-132145.pdf',
    config_path='./defaultConfig.json',
    document_name='Sample File2',
    wait_till_finished=False,
    save_request_id=True,
)

print(parsr.get_text())
print('Processamento executado!')
removeArquivosPDF(DIR_ARQUIVOS)

