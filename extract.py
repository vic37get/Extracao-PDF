from pathlib import Path
import argparse,os,shutil,re

parser = argparse.ArgumentParser()
parser.add_argument('--input','-i',type=str, required=True)
parser.add_argument('--output','-o',type=str, required=True)
opt = parser.parse_args()

def extract_all():
    input = Path(opt.input)
    for i,p in enumerate(input.glob("*.zip")):
        extract_dir = Path(opt.output).joinpath(p.stem)
        if not os.path.exists(extract_dir):
            os.mkdir(extract_dir)
            shutil.unpack_archive(p,extract_dir)
        if i > 30:
            break

registro = dict()
def findEdital(input=Path(opt.output),registro=dict()):
    for dir in input.glob('*'):
        def find(name,directory):
            registro[name] = {'EDITAL':''}
            lista_arquivos = directory.glob('*')
            lista_arquivos = sorted(lista_arquivos, key=os.path.getmtime)
            for files in lista_arquivos:
                if os.path.isfile(files):
                    if files.name.split('.')[1] == 'zip':
                        if not os.path.exists(files.parent.joinpath(files.stem)):
                            os.mkdir(dir.joinpath(files.stem))
                            shutil.unpack_archive(files,dir.joinpath(files.stem))
                            find(dir.name,dir)
                    else:
                        pattern = re.compile('EDITAL|PREGAO',flags=re.I)
                        if re.search(pattern=pattern,string=files.stem) != None:
                            registro[name]['EDITAL'] = files
                else:
                    find(name,files)
                    ...
        find(dir.name,dir)

extract_all()
findEdital(input=Path(opt.output),registro=registro)

#for k,v in registro.items():
    #print(k)
    #print(' '*4,v['EDITAL'])

def move_files(src_dir, dst_dir):
    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)
        if os.path.isdir(file_path):
            move_files(file_path, dst_dir)
        else:
            try:
                shutil.move(file_path, dst_dir)
            except shutil.Error:
                # Arquivo já existe no destino, ignorar
                pass

src_dir = 'INPUT_DIR'
dst_dir = 'OUTPUT_DIR'
move_files(src_dir, dst_dir)