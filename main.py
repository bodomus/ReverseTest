import os
import sys
import fileutils
import re

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Поиск дублирующих файлов, которые отличаются только суффиксами  20200209_163926.jpg = 20200209_163926-2.jpg

pathes = 'd:/projects/photo/'
output_filename = 'd:/projects/photo/existfile.log'
list = []
dublicate_dict = {}

###
# Dictionary for result found files
filedict = {}
# Total original files
total_original_files = 0
# Total dublicat files
total_dublicat_files = 0
# Total size original files
total_size_original_files = {}
# Total size dublicate files
total_size_dublicate_files = 0
# counter
count = 0
# kyes that apperas in command line arguments
preferences_keys = dict({'sdir': f'-sdir=', 'ddir': f'-ddir=', 'ks': f'-ks=', 'c': '-c'})  # [file] [path]

# object for params command line
params = {'sdir': None, 'ddir': None, 'key': None, "search_type": None}


# class for console color text
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


def compare2Directories(source, destination):
    """Проверить 2 директории. Если в source есть файлы которых нет в директории destination
    вывести эти фыайлы в первом столбце. Если во втором столбце есть файлы которых нет в первом столбце
    вывести эти файлы во втором столбце"""


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def write_strings(filename, dict):
    global total_original_files
    global total_dublicat_files

    file_object = open(filename, 'w+')
    file_object.write(f'total count original files: {total_original_files} \n')
    file_object.write(f'total count duplicate files: {total_dublicat_files} \n')
    sumlambda = lambda item, total: item + total
    sum = 0
    for i in total_size_original_files.values():
        sum += i

    file_object.write(f'total size original files: {sum} [{fileutils.convert_unit(sum, fileutils.SIZE_UNIT.MB)} MB]\n')
    file_object.write(
        f'total size dublicate files: {total_size_dublicate_files}  [{fileutils.convert_unit(total_size_dublicate_files, fileutils.SIZE_UNIT.MB)}] MB \n\n\n')
    for obj in dict.keys():
        value = dict.get(obj)
        if value is not None:
            file_object.write(f'Original file: {obj} \n')
            for f in value:
                file_object.write(f'\t {f} \n')

    get_dublicate_files(dict)
    file_object.write(f'++++++++++duplicate+++++++++++  \n')
    for value in dublicate_dict.values():
        if value is not None:
            file_object.write(f'\t {value} \n')
    file_object.close()


def get_dublicate_files(dict):
    for obj in dict.keys():
        value = dict.get(obj)
        if value is not None:
            for f in value:
                dublicate_dict.update({f: f})


def check_file(fullfilepath):
    """ Проверить файл на существование исходного файла без символа "-" с таким же свойствами"""
    global total_size_original_files
    global total_size_dublicate_files
    global total_original_files
    global total_dublicat_files

    sizefileodublicat = os.path.getsize(path_file)
    total_size_dublicate_files += sizefileodublicat
    dublicatname = os.path.basename(fullfilepath)
    ext = os.path.splitext(dublicatname)[1]
    filename = os.path.splitext(dublicatname)[0]
    index = filename.rfind('-')
    if index > -1:
        originalbodyfilename = filename[0:index]
        originalfilepath = os.path.dirname(fullfilepath) + '/' + originalbodyfilename + ext
        sizeoriginal = os.path.getsize(originalfilepath)
        key = f'{originalfilepath}#{sizeoriginal}'
        ovalue = total_size_original_files.get(key)
        if ovalue is None:
            total_size_original_files[key] = sizeoriginal

        if sizeoriginal == sizefileodublicat:
            print(
                f'Original file name: {originalfilepath} | Dublicat file name: {dublicatname}  Original file size: {sizeoriginal} | Dublicat file size: {sizefileodublicat}')

            value = filedict.get(key)

            if value is not None:
                filedict[key].append(f'{fullfilepath}')
                total_dublicat_files += 1
            else:
                filedict.update({key: [f'{fullfilepath}']})
                total_original_files += 1
                total_dublicat_files += 1


def prepare_files(base_dir1, base_dir2, dict_key):
    """ Сравниваем файлы из base_dir1 с base_dir2
    файл равен если хеш сумма одинакова или наименование и размер одинаков
    Extend `base_dir1`.  Class attribute `instances` keeps track
    of the number of `Keeper` objects instantiated.
    """
    global count
    if '' == base_dir1 or base_dir2 == '':
        raise ("Error base_dir1 or base_dir2 is empty")
    sdict = {}
    ddict = {}

    sdict = fileutils.create_dict(base_dir1, fileutils.Dict_key.FILE_NAME)
    ddict = fileutils.create_dict(base_dir2, fileutils.Dict_key.FILE_NAME)

    compare_directory(ddict, dict_key, sdict)


def compare_directory(ddict, dict_key, sdict):
    global count
    for skey in sdict.keys():
        svalue = sdict.get(skey)
        if svalue is not None:
            dkey = svalue['file_path'] if dict_key == fileutils.Dict_key.FILE_PATH else svalue['file_name']
            dvalue = ddict.get(dkey)
            count += 1
            if dvalue is not None:
                compare_result = compare_2files(count, svalue, dvalue)
                print_compare_result(count, svalue, dvalue, compare_result)
            else:
                print_not_found_result(count, file1=svalue)


def print_not_found_result(count, file1: object):
    s1 = f"{count}.файл не найден "
    print(f"{bcolors.FAIL} {s1}\tИсходный файл: {bcolors.ENDC} {file1['file_path']}", end=f"\n{'-' * 80}\n")


def print_compare_result(count, file1: object, file2: object, operation_result: bool) -> None:
    s1 = f"{count}.файлы равны" if operation_result else f"{count}.файлы не равны"
    print(f"{bcolors.WARNING} {s1}\tИсходный файл \tСравниваемый файл{bcolors.ENDC}")
    print(f"{bcolors.BOLD}Полный путь:{bcolors.ENDC}\t{file1['file_path']}\t {file2['file_path']}")
    print(f"{bcolors.BOLD}Имя файла:{bcolors.ENDC}{bcolors.ENDC}\t{file1['file_name']}\t {file2['file_name']}")
    print(f"{bcolors.BOLD}Размер файла:{bcolors.ENDC}{file1['file_size']}\t {file2['file_size']}\t ")
    print(f"{bcolors.BOLD}hash sum:{bcolors.ENDC}\t{file1['file_hash']}\t {file2['file_hash']} ", end=f"\n{'-' * 80}\n")


def compare_2files(count, file1: object, file2: object) -> bool:
    """
    сравниваем файлы Условия сравнения на равенство имена файлов равны, размер одинаков и хэш суммы совпадают
    filename: file name
    filepath: full path with name
    size: size of file in bytes
    hash: hashfile
    :param file1: #dict с объектом
    :param file2: #dict с объектом
    :return: bool
    :Date: 2022-06-23
    :Version: 1
    :Authors: bodomus@gmail.com
    """
    result = False
    if file1 is None or file2 is None:
        raise ("compare_2files: the input param is None")
    if (file1['file_name'] == file2['file_name']) and (file1['file_hash'] == file2['file_hash']) and (
            file1['file_size'] == file2['file_size']):
        result = True
    return result


def call_is_directory_compare(argslice) -> bool:
    """
    Проверить если запущен режим сравнения директорий (1 режим) - то выполнить его
    :argslice: arguments command line
    :return:
    """
    p1 = get_directory(1, argslice)
    p2 = get_directory(2, argslice)
    tk = get_type_key(argslice)

    if p1 is not None and p2 is not None and tk is not None:
        prepare_files(p1, p2, dict_key=tk)
        return True
    return False


def call_is_file_name_compare(argslice) -> None:
    """
    2 mode
        Проверить если запущен режим сравнения наименования файла (2 режим) - то выполнить его
        :argslice: arguments command line
        :return:
        """
    for item in argslice:
        x = re.search('^-c$', item)
        if x:
            i = 0
            filesize = 0
            for root, dirs, files in os.walk(pathes):
                for file in files:
                    if file.endswith(".mp4") or file.endswith(".jpg") or file.endswith(".cr2"):
                        path_file = os.path.join(root, file)
                        result = re.search(r'-\d+', file)
                        i = i + 1
                        # print(path_file, i)
                        if result != None:
                            size = os.path.getsize(path_file)
                            filesize += size
                            # shutil.move(path_file, 'j:/' + 'VideoFromProjects/'+file)
                            # list.append(f'filename: {path_file}: {size}\n')
                            check_file(path_file)

            # See PyCharm help at https://www.jetbrains.com/help/pycharm/
            write_strings(output_filename, filedict)

            print_hi(filesize)
    return


def get_directory(index: int, args: list) -> object:
    """
        Получить из комагдной строки директорию. index1 - source directory index2-destination directory
        :param index: #1 or 2 source or destination directory
        :param args: command string arguments
        :return: bool
        :Date: 2022-06-23
        :Version: 1
        :Authors: bodomus@gmail.com
        """
    for item in args:
        x = re.search('^-sdir1=\S*$', item) if index == 1 else re.search('^-ddir2=\S*$', item)
        if x:
            return item.replace("-sdir1=" if index == 1 else "-sdir2=", '')
    return None


def get_type_search(args: list) -> object:
    """
        Получить из командной строки параметр поиска по файлу или директории
        :param args: command string arguments
        :Date: 2022-06-23
        :Version: 1
        :Authors: bodomus@gmail.com
        """
    for item in args:
        x = re.search('^-c\S*$', item)
        if x:
            return fileutils.Dict_key.FILE_NAME
    return fileutils.Dict_key.FILE_PATH


def get_type_key(argsslice: list) -> object:
    """
        Получить из командной строки тип ключа для поиска в dict
        :param argsslice: arguments command string
        :return: object
        :Date: 2022-06-27
        :Version: 1
        :Authors: bodomus@gmail.com
        """
    for item in argsslice:
        x = re.search(r"^-sk=file|path$", item)

        if x:
            param = item.replace('-sk=', '')
            return fileutils.Dict_key.FILE_NAME if param == 'file' else fileutils.Dict_key.FILE_PATH
    return None


def prepare_command_string(argsslice: list) -> None:
    source = get_directory(index=1, args=argsslice)
    destiny = get_directory(index=2, args=argsslice)
    tk = get_type_key(argsslice)
    searched_type = get_type_search(argsslice)

    params.update({'sdir': source, 'ddir': destiny, 'key': tk, "search_type": searched_type})


def is_params_valid() -> bool:
    if params["search_type"] == fileutils.Dict_key.FILE_PATH and params["sdir"] is not None and params[
        'ddir'] is not None:
        if params["key"] is None:
            print_help()
            return False
    elif params["search_type"] == fileutils.Dict_key.FILE_NAME:
        return True


def print_help():
    print(f"{bcolors.OKCYAN} Using:\n {bcolors.ENDC}")
    # -sdir1 = d: / Work / CodeBooks - ddir2 = d: / Work / CodeBooks1
    print(
        f"{bcolors.OKCYAN} -sdir1(directory1path) -ddir2(directory2path) search and compare directories(new behaviour)\n {bcolors.ENDC}")
    print(f"{bcolors.OKCYAN} \ks=file[path] search comparison by file or full file path\n {bcolors.ENDC}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # TODO split code on parts. And call them by arg from command string
    args = sys.argv[1:]

    if len(sys.argv) == 1:
        print_help()
        exit()
    prepare_command_string(args)

    call_is_directory_compare(args)
    call_is_file_name_compare(args)
