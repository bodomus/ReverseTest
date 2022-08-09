import os
from enum import Enum, unique
from pathlib import Path
import hashlib

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Key for Search Dictionary
class Dict_key(Enum):
    # Search by file name
    FILE_NAME = 1,
    # Search by file path
    FILE_PATH = 2


def get_file_size_in_bytes(file_path):
    """ Get size of file at given path in bytes"""
    size = os.path.getsize(file_path)
    return size


def get_file_size_in_bytes_2(file_path):
    """ Get size of file at given path in bytes"""
    # get statistics of the file
    stat_info = os.stat(file_path)
    # get size of file in bytes
    size = stat_info.st_size
    return size


def get_file_size_in_bytes_3(file_path):
    """ Get size of file at given path in bytes"""
    # get file object
    file_obj = Path(file_path)
    # Get file size from stat object of file
    size = file_obj.stat().st_size
    return size


# Enum for size units
class SIZE_UNIT(Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_unit(size_in_bytes, unit):
    """ Convert the size from bytes to other units like KB, MB or GB"""
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


def get_file_size(file_name, size_type=SIZE_UNIT.BYTES):
    """ Get file in size in given unit like KB, MB or GB"""
    size = os.path.getsize(file_name)
    return convert_unit(size, size_type)


def get_hash(filename):
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(BUF_SIZE)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            sha1.update(fb)  # Update the hash
            fb = f.read(BUF_SIZE)  # Read the next block from the file
    return sha1.hexdigest()


def create_dict(fileDir: object, dict_key: enumerate) -> dict:
    """Создаем dict из директории. key нименование файла или путь надо создавать параметр
     value dict с объектом
     filename: file name
     file_path: full path with name
     size: size of file in bytes
     hash: hashfile
     :rtype: object
     :Date: 2002-03-22
     :Version: 1
     :Authors:
        - Me
        - Myself
        - I
    полный путь ?"""
    # TODO Add param for using key in dictionary
    global Dict_key
    dir = {}

    index = 0;
    for root, dirs, files in os.walk(fileDir):
        for file in files:
            file_item = {}
            ff = os.path.join(root, file)
            statinfo = os.stat(ff)
            hash = get_hash(ff)
            file_item['file_size'] = statinfo.st_size
            file_item['file_name'] = file
            file_item['file_path'] = ff
            file_item['file_hash'] = hash
            index += 1
            print(f'{bcolors.OKBLUE}{index:d}.{bcolors.ENDC}\t {bcolors.OKBLUE}file_name:{bcolors.ENDC} {file} \t{bcolors.OKBLUE}file_size:{bcolors.ENDC} {statinfo.st_size:d} \t{bcolors.OKBLUE}file_hash:{bcolors.ENDC} {hash} ')

            size = os.path.getsize(ff)
            name = os.path.basename(ff)

            kkey = file if dict_key == Dict_key.FILE_NAME else ff
            value = dir.get(kkey)
            if value is not None:
                exception_message = f"{bcolors.FAIL}Error the same key %s is found in dictionary{bcolors.ENDC}" % kkey
                raise ValueError(exception_message)
            dir.update({kkey: file_item})

    print("\nКоличество элементов в источнике: %d\n " % len(dir))
    return dir





