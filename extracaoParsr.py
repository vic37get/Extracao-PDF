from conexao import conect
from ManipulacaoDados import readCsv, getIdArquivo, getIdLicitacao, removeArquivosPDF, saveFile
import wget

DIR_ARQUIVOS = 'arquivos/arquivosPDF'
DIR_DESTINO = 'arquivos/arquivosTXT'
INPUT_DATAFRAME = readCsv('.csv')

def downloadPDF(id_licitacao, id_arquivo):
    URL = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/{}/arquivos/{}'.format(id_licitacao, id_arquivo)
    try:
        arquivoPDF = wget.download(URL, "{}/{}-{}.pdf".format(DIR_ARQUIVOS, id_licitacao, id_arquivo))
        print('\nDownload da licitação {}, arquivo {} realizado!'.format(id_licitacao, id_arquivo))
        return arquivoPDF
    except:
        print('\nErro ao realizar o download da licitação {}, arquivo {}!'.format(id_licitacao, id_arquivo))
        return None

def PDFtoText(arquivoPDF, id_licitacao, id_arquivo):
    parsr = conect()
    parsr.send_document(
        file_path=str(arquivoPDF),
        config_path='./defaultConfig.json',
        document_name='{}-{}'.format(id_licitacao, id_arquivo),
        wait_till_finished=False,
        save_request_id=True,
    )
    return parsr

def ExtractText(INPUT_DATAFRAME):
    FAILED_FILES = []
    for file in INPUT_DATAFRAME.index:
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        file_pdf = downloadPDF(id_licitacao, id_arquivo)
        if file_pdf != None:
            PDFtoText(file_pdf, id_licitacao, id_arquivo)
            removeArquivosPDF(DIR_ARQUIVOS)
        else:
            FAILED_FILES.append('{}-{}'.format(id_licitacao, id_arquivo))
    saveFile(FAILED_FILES, 'FailedFiles.txt')

ExtractText(INPUT_DATAFRAME)


