import tika
from tika import parser
import os
os.environ['TIKA_SERVER_JAR'] = 'https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.19/tika-server-1.19.jar'
FileName = "_EDITAL_TP02.pdf"
PDF_Parse = parser.from_file(FileName)
print(PDF_Parse)
#print(PDF_Parse)