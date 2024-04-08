import os
import random
import shutil

def distribute_files(source_folder, target_folders):
    files = os.listdir(source_folder)
    num_files = len(files)
    num_folders = len(target_folders)
    
    files_per_folder = num_files // num_folders
    remainder = num_files % num_folders
    
    # 對目標文件夾進行隨機排序
    random.shuffle(target_folders)
    
    for i, folder in enumerate(target_folders):
        files_to_copy = files[i * files_per_folder : (i + 1) * files_per_folder]
        if i < remainder:
            files_to_copy.append(files[num_folders * files_per_folder + i])
        for file_name in files_to_copy:
            source_file_path = os.path.join(source_folder, file_name)
            target_file_path = os.path.join(folder, file_name)
            shutil.copy(source_file_path, target_file_path)
    
    # 刪除來源文件夾中的文件
    for file_name in files:
        source_file_path = os.path.join(source_folder, file_name)
        os.remove(source_file_path)

