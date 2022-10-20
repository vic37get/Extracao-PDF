import re

txt=re.compile(r'ASCII text')
doc=re.compile(r'Composite Document File V2 Document')
java=re.compile(r'Java source')
html=re.compile(r'HTML document')
jpg=re.compile(r'JPEG image data')
xlsx=re.compile(r'Microsoft Excel 2007')
xps=re.compile(r'Microsoft OOXML')
docx=re.compile(r'Microsoft Word 2007')
pdf=re.compile(r'PDF document')
png=re.compile(r'PNG image data')
rar=re.compile(r'RAR archive data')
rtf=re.compile(r'Rich Text Format')
tif=re.compile(r'TIFF image data')
zipe=re.compile(r'Zip archive data')

lista=[(".txt",txt),(".doc",doc),
       (".java",java),(".html",html),
       (".jpg",jpg),(".xlsx",xlsx),
       (".xps",xps),(".docx",docx),
       (".pdf",pdf),(".png",png),
       (".rar",rar),(".rtf",rtf),
       (".tif",tif),(".zip",zipe)]