import os

def count_files(folder_path, header):
    count = 0
    
    for filename in os.listdir(folder_path):
        if filename.startswith(header) and os.path.isfile(os.path.join(folder_path, filename)):
            count += 1
    
    return count