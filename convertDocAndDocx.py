import subprocess
import os

def docAndDocxToPdf(filename, DIST_DIR, BASE_DIR):
    os.chdir(DIST_DIR)
    subprocess.call(['soffice', '--headless', '--convert-to', 'pdf', filename])
    filenamePDF = filename.split('.')[0]+'.pdf'
    return os.path.join(DIST_DIR, filenamePDF)

