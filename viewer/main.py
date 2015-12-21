# coding=cp1251
import argparse
import os

import utils
import viewer

parser = argparse.ArgumentParser(description=u"Поиск подключенных к PE-файлу "
                                             u"функций.")

parser.add_argument("-f", "--filename", help=u"Исследуемый файл")
parser.add_argument("-d", "--directory", help=u"Исследуемая директория")
parser.add_argument("-s", "--search", help=u"Файл формата JSON, являющий "
                                           u"собой список искомых функций. "
                                           u"Функции могут искаться по имени "
                                           u"или ординалу.")


def search(path, search_dict, result_list):
    if not os.path.exists(path):
        message = u"Указанный путь к исследуемому файлу/папке не существует."
        raise ValueError(message)

    if os.path.isdir(path):
        for subfile in os.listdir(path):
            search(path + "\\" + subfile, search_dict, result_list)
    elif os.path.isfile(path) and os.access(path, os.X_OK):
        try:
            view = viewer.Viewer(path)
        except Exception:
            return
        result_file = view.search_imports(search_dict)
        if result_file:
            result_list.extend(result_file)


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.filename and not args.directory:
        msg = u"На вход должен быть подан путь к исследуемому файлу или папке."
        raise TypeError(msg)
    if args.filename and args.directory:
        msg = u"Не может быть одновременно подан и путь файла, и путь папки."
        raise TypeError(msg)

    if not args.search:
        msg = u"На вход должен быть подан путь к файлу с искомыми функциями."
        raise TypeError(msg)

    investigating = utils.parse(args.search)
    utils.validate_search_list(investigating)

    result_list = []
    search(args.filename or args.directory,
           investigating,
           result_list)
    utils.print_tuple(result_list)
