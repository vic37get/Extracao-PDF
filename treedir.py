OUT_DIR = '/var/projetos/arquivos/'

from filename import lista as list_ext
import os

for i in list_ext:
    if not(os.path.exists(os.path.join(OUT_DIR,'arquivos_'+i[0]))):
        os.makedirs(os.path.join(OUT_DIR,'arquivos_'+i[0]))
    print('arquivos_'+i[0])