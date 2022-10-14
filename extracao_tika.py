import tika
from tika import parser
import os
os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'
FileName = "_EDITAL_TP02.pdf"
PDF_Parse = parser.from_file(FileName, xmlContent=True)
print(PDF_Parse['content'])
with open('dados.txt', 'w', encoding='utf-8') as f:
    f.write(str(PDF_Parse['content']))