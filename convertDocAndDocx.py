import subprocess
import os
from manipulacaoDados import suppress_stdout

def docAndDocxToPdf(filename, DIST_DIR):
    os.chdir(DIST_DIR)
    subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', filename], stdout=subprocess.DEVNULL)
    filenamePDF = filename.split('.')[0]+'.pdf'
    return os.path.join(DIST_DIR, filenamePDF)

