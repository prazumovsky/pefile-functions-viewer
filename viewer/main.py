# coding=cp1251
import argparse
import os

import utils
import viewer

parser = argparse.ArgumentParser(description=u"����� ������������ � PE-����� "
                                             u"�������.")

parser.add_argument("-f", "--filename", help=u"����������� ����")
parser.add_argument("-d", "--directory", help=u"����������� ����������")
parser.add_argument("-s", "--search", help=u"���� ������� JSON, �������� "
                                           u"����� ������ ������� �������. "
                                           u"������� ����� �������� �� ����� "
                                           u"��� ��������.")


def search(path, search_dict, result_list):
    if not os.path.exists(path):
        message = u"��������� ���� � ������������ �����/����� �� ����������."
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
        msg = u"�� ���� ������ ���� ����� ���� � ������������ ����� ��� �����."
        raise TypeError(msg)
    if args.filename and args.directory:
        msg = u"�� ����� ���� ������������ ����� � ���� �����, � ���� �����."
        raise TypeError(msg)

    if not args.search:
        msg = u"�� ���� ������ ���� ����� ���� � ����� � �������� ���������."
        raise TypeError(msg)

    investigating = utils.parse(args.search)
    utils.validate_search_list(investigating)

    result_list = []
    search(args.filename or args.directory,
           investigating,
           result_list)
    utils.print_tuple(result_list)
