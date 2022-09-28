from datetime import datetime, timedelta
import shutil
import os
import psutil
import time
import ctypes
import sys

backup_dir = '\\path\\to\\backup\\dir'
save_file = 'SAVEDATA'
second_save_file = 'SAVEDATA_BACKUP'
save_dir = 'path\\to\steam\\userdata\\91248288\\1255630\\remote'
process_name = "WWE2K22_x64.exe"
log_file = '\\path\\to\\log_location\\log_file.txt'

sys.stdout = open(log_file, 'wt')
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


# Backs up the file and then adds time stamp to the name
def backup_files(file):
    shutil.copyfile(f"{save_dir}\\{file}", f"{backup_dir}\\{file}")
    os.rename(f"{backup_dir}\\{file}", f"{backup_dir}\\{timestamp}_{file}")

# creates a list of the files sorted by time in order to overwrite the oldest file.
def sorted_ls(path):
    ctime = lambda f: os.stat(os.path.join(path, f)).st_ctime
    return list(sorted(os.listdir(path), key=ctime))


old_time = datetime.now() - timedelta(hours=2)
run = True
while run:
    now = datetime.now()
    log_time = now.strftime("%I:%M %p")
    print(f"{log_time} - Setting time...")

# checks process list to find game running. If it does it then checks that it has been greater than
# an hour since the last backup. If so, it backs up the fie and then removes the oldest one.
# After completing it waits for an hour and then runs again
    for proc in psutil.process_iter():

        if proc.name() == process_name and now >= old_time + timedelta(hours=1):
            print(f"{log_time} - Found game running...")
            # this sleep is here because copying the save immediately on game launch can corrupt the save
            time.sleep(120)

            print(f"{log_time} - Finished sleep. Backing up files...")
            timestamp = now.strftime("%I-%M-%p")
            backup_files(save_file)
            backup_files(second_save_file)

            max_files = 10
            del_list = sorted_ls(backup_dir)[0:len(sorted_ls(backup_dir)) - max_files]

            for file in del_list:
                os.remove(f"{backup_dir}\\{file}")
            print(f"{log_time} - Deleting old files...")

            old_time = now

            time.sleep(3600)
