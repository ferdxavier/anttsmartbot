import os
from pathlib import Path

dir_name_denied = ".denied"
dir_name_sucess = ".successfullyprocessed"
allowed_extensions = ['.xls', '.xlsx', '.ods']

def exist_file(path):
    if os.path.exists(path):
        return {"exist": True, "message": f'Arquivo "{path}" não encontrado!'}
    else:
        return {"exist": False, "message": "O arquivo não existe."}

def list_files(path):
    if path[len(path) - 1] != "/":
        path = path + '/'
        
    try:
        dirs = os.listdir(path)
    except NotADirectoryError:
        return []
    except FileNotFoundError:
        return []
    
    files = []  
    for name_file in dirs:
        item = Path(path + name_file)
        if item.is_file():
            files.append({"name": name_file, "fullpath": path + name_file})
    
    return files

def process_denied_extensions(files):
    denied_file = []
    for file in files:
        if os.path.splitext(file['name'])[1] not in allowed_extensions:
            denied_file.append(file)
            
    return denied_file

def move_files(files, defaul_path, dir_destination):
    if defaul_path[len(defaul_path) - 1] != "/":
        defaul_path = defaul_path + '/'
        
    denied_dir = Path(defaul_path +"/" +dir_destination)
    if not os.path.exists(denied_dir):
        os.mkdir(defaul_path +"/" +dir_destination)
        
    for file in files:
        source = file['fullpath']
        destination = defaul_path +dir_destination +'/' +file['name']
        os.rename(source, destination)
        
def move_denied_extensions(files, defaul_path):
    move_files(files, defaul_path, dir_name_denied)

def move_processed_allowed_files(files, defaul_path):
    move_files(files, defaul_path, dir_name_sucess)