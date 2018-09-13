import os
from os.path import isfile, join, isdir

base_path = join('..', 'files')


def getFileNames(folder_name):
    """Get names of files in a local folder"""
    path = join(base_path, folder_name)
    file_names = []
    for file in os.listdir(path):
        if isfile(join(path, file)):
            file_names.append(file)
    return file_names


def moveFile(source_folder, source_filename, destination_folder, destination_file_name):
    """move a file from the source_folder + source_filename to 
    destination_folder + destination_file_name
    """
    source_path = join(base_path, source_folder, source_filename)
    with open(source_path, 'rb') as f:
        data = f.read()

    destination_path = join(base_path, destination_folder)
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    with open(join(destination_path, destination_file_name), 'w+b') as f:
        result = f.write(data)

    os.remove(source_path)
    return result
