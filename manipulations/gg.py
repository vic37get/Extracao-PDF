import repackage
repackage.up()

import utils
import os
from pathlib import Path
l = os.listdir('/var/projetos/arquivos/arquivos_.doc_convertidos')
count = 0
for i in l:
    if count > 50:
        break
    p = Path("/var/projetos/arquivos/arquivos_.doc_convertidos").joinpath(i)
    #cmd = "ps2pdf "+p.__str__()+" /var/projetos/arquivos/teste_wv/"+p.stem+".pdf"
    cmd = "abiword --to=pdf --to-name=/var/projetos/arquivos/teste_wv/"+p.stem+".pdf "+p.__str__()
    #"AbiWord --print="+p.__str__()+" && ps2pdf file.ps"
    #cmd = 'wvPDF '+p.__str__()+' /var/projetos/arquivos/teste_wv/'+p.stem+'.pdf'
    print(cmd)
    count += 1
    sh = os.popen(cmd)
    print(sh.read())