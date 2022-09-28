from datetime import datetime
import shutil
import os

backup_dir = '\\path\\to\\backup\\dir'
save_file = 'SAVEDATA'
second_save_file = 'SAVEDATA_BACKUP'
save_dir = 'path\\to\\steam\\userdata\\folder\\1255630\\remote'

timestamp = datetime.now().strftime("%I-%M-%p")
modified_time = os.path.getctime(f"{save_dir}\\{save_file}")


# Backs up the file and then adds time stamp to the name
def backup_files(file):
    shutil.copyfile(f"{save_dir}\\{file}", f"{backup_dir}\\{file}")
    os.rename(f"{backup_dir}\\{file}", f"{backup_dir}\\{timestamp}_{file}")


backup_files(save_file)
backup_files(second_save_file)

max_files = 10


def sorted_ls(path):
    ctime = lambda f: os.stat(os.path.join(path, f)).st_ctime
    return list(sorted(os.listdir(path), key=ctime))


del_list = sorted_ls(backup_dir)[0:len(sorted_ls(backup_dir)) - max_files]

for file in del_list:
    os.remove(f"{backup_dir}\\{file}")
