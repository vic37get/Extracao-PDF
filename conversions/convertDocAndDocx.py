from genericpath import exists
import subprocess
import os

def docAndDocxToPdf(filename, DIST_DIR):
    os.chdir(DIST_DIR)
    subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', filename], stdout=subprocess.DEVNULL)
    filenamePDF = filename.split('.')[0]+'.pdf'
    if searchPdf(filenamePDF) == True:
        return os.path.join(DIST_DIR, filenamePDF)
    else:
        return False

def searchPdf(arquivo):
    if arquivo in os.listdir('.'):
        return True
    else:
        return False