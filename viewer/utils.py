# coding=cp1251
import json


def parse(filename):
    json_data = open(filename, "r+b").read()
    result = json.loads(json_data)
    return result["Functions"]


def validate_search_list(search_list):
    for item in search_list:
        if (item.get("Snippet") is not None and
                (item.get("Name") is not None or
                 item.get("Ordinal") is not None)):
            raise ValueError(u"Нельзя одновременно задавать ключ \"Snippet\" "
                             u"и \"Name\" или \"Ordinal\"")


def print_tuple(print_list):
    max_file_name = 0
    max_name = 4
    max_ordinal = 7
    for item in print_list:
        path, name, ordinal = item
        if name is None:
            name = "-"
        if ordinal is None:
            ordinal = "-"
        if len(name) > max_name:
            max_name = len(name)
        if len(ordinal) > max_ordinal:
            max_ordinal = len(ordinal)
        if len(path) > max_file_name:
            max_file_name = len(path)

    width = max(max_name, max_ordinal)
    width += 4
    max_file_name += 4
    output = u""
    output += u"+"
    for j in range(max_file_name):
        output += u"-"
    for i in range(2):
        output += u"+"
        for j in range(width):
            output += u"-"
    output += u"+\n"
    output += u"| file"
    for i in range(max_file_name - 5):
        output += u" "
    output += u"| name"
    for i in range(width - 5):
        output += u" "
    output += u"| ordinal"
    for i in range(width - 8):
        output += u" "
    output += u"|\n"
    output += u"+"
    for j in range(max_file_name):
        output += u"-"
    for i in range(2):
        output += u"+"
        for j in range(width):
            output += u"-"
    output += u"+\n"
    for item in print_list:
        path, name, ordinal = item
        if name is None:
            name = u"-"
        if ordinal is None:
            ordinal = u"-"
        output += u"| "
        output += path.decode("cp1251")
        for i in range(max_file_name - len(path) - 1):
            output += u" "
        output += u"| "
        output += name
        for i in range(width - len(name) - 1):
            output += u" "
        output += u"| "
        output += ordinal
        for i in range(width - len(ordinal) - 1):
            output += u" "
        output += u"|"
        output += u"\n"
    output += u"+"
    for j in range(max_file_name):
        output += u"-"
    for i in range(2):
        output += u"+"
        for j in range(width):
            output += u"-"
    output += u"+"
    print(output)
