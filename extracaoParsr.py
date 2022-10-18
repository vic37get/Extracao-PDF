from conexao import conect
from ManipulacaoDados import readCsv, getIdArquivo, getIdLicitacao, removeArquivosPDF, saveFile
import wget
import magic
from filename import lista as lista_filename
import re
import os
from pathlib import Path
import aspose.words as aw

DIR_ARQUIVOS = 'arquivos/arquivosPDF'
DIR_DESTINO = 'arquivos/arquivosTXT'
INPUT_DATAFRAME = readCsv('lic_2007_2022.csv')

def getExtension(tipo):
    for ext in lista_filename:
        if re.search(ext[1],tipo):
            return ext[0]

def downloadPDF(id_licitacao, id_arquivo):
    URL = 'http://sistemas.tce.pi.gov.br/muralic/api/licitacoes/{}/arquivos/{}'.format(id_licitacao, id_arquivo)
    try:
        arquivoPDF = wget.download(URL, "{}/{}-{}".format(DIR_ARQUIVOS, id_licitacao, id_arquivo))
        tipo = magic.from_file(arquivoPDF)
        os.rename(arquivoPDF, arquivoPDF+getExtension(tipo))
        arquivoPDF = arquivoPDF+getExtension(tipo)
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
        if file == 5:
            break
        id_arquivo = getIdArquivo(INPUT_DATAFRAME, file)
        id_licitacao = getIdLicitacao(INPUT_DATAFRAME, file)
        file_pdf = downloadPDF(id_licitacao, id_arquivo)
        if file_pdf != None:
            p = Path(file_pdf)
            if p.suffix.find('.doc')!=-1:
                doc = aw.Document(file_pdf)
                filename = p.parent.joinpath(p.stem+'.pdf')
                doc.save(filename.__str__())
                file_pdf = filename.__str__()
            PDFtoText(file_pdf, id_licitacao, id_arquivo)
            removeArquivosPDF(DIR_ARQUIVOS)
        else:
            FAILED_FILES.append('{}-{}'.format(id_licitacao, id_arquivo))
    saveFile(FAILED_FILES, 'FailedFiles.txt')

def ExtractTextf():
    FAILED_FILES = []
    id_arquivo = '133985'
    id_licitacao = '190539'
    file_pdf = downloadPDF(id_licitacao, id_arquivo)
    if file_pdf != None:
        p = Path(file_pdf)
        if p.suffix.find('.doc')!=-1:
            doc = aw.Document(file_pdf)
            filename = p.parent.joinpath(p.stem+'.docx')
            print(filename)
            doc.save(filename.__str__())
            file_pdf = filename.__str__()
        PDFtoText(file_pdf, id_licitacao, id_arquivo)
        removeArquivosPDF(DIR_ARQUIVOS)
    else:
        FAILED_FILES.append('{}-{}'.format(id_licitacao, id_arquivo))
#ExtractText(INPUT_DATAFRAME)
# 13753 1827 / 13833 1914
#ExtractTextf()

'''arquivo = '/mnt/c/Users/victor.silva/Documents/doc.pdf'
doc = aw.Document(arquivo)
for page in range(0, doc.page_count):
    extractedPage = doc.extract_pages(page, 1)
    extractedPage.save(f"Output_{page + 1}.jpg")'''
#PDFtoText(doc, '1', '2')



