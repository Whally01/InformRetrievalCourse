import os
import re
from collections import defaultdict, Counter
import json
import pandas as pd
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def bold(txt):
    return '\x1b[1m%s\x1b[0m' % txt


def index_docs(data):
    index_dict = {}  # dict like {'привет':['1.txt', '4.txt' ,'6.txt'], 'лол': ['2.txt', '4.txt']}
    for dic in data:
        for key in dic:
            for text in dic.values():
                for word in text.split():
                    index_dict.setdefault(word, [])
                    if key not in index_dict[word]:
                        index_dict[word].append(key)
    return index_dict


def read_file(rootdir):
    filenames = os.listdir(rootdir)
    data = []
    for filename in filenames:
        with open(os.path.join(rootdir, filename), 'r') as input:
            data.append({filename: input.read()})
    return data


def search(data, index, query):
    query_splitted = query.split()
    result = []
    for docname in data:
        query_copy = query
        for word in query_splitted:
            check = 0

            # if word == '~':
            #     query_copy = query_copy.replace(word, 'not')

            if word.isalnum():
                m = morph.parse(word)[0]
                lem = m.normal_form

                if lem in index:  # если слово было проиндексировано
                    if docname in index[lem]:
                        check = 1
                query_copy = query_copy.replace(word, check.__str__())

        if eval(query_copy):
            # print_result(query_copy)
            result.append(docname)

    return result


data = read_file('/home/dr/PycharmProjects/inform_retrive/scraper/lemmedFiles')
# for d in data:
#     for key in d:
#         print(d[key])
index = index_docs(data)
dict = {}
for dic in data:
    for key in dic:
        dict.setdefault(key, dic[key])


def print_result(result):
    print('кол-во док-ов: {0} \n {1} \n {2}'.format(len(result), result, '-' * 80))


# json.dump(index, open('invert_index_new.json', 'w', encoding='utf-8'), ensure_ascii=False)
# df = pd.DataFrame.from_dict(index, orient='index')
# print(df)
# df.to_csv('invert_new.csv', sep=',', encoding='utf-8')


print_result(search(dict, index, 'радио'))

print_result(search(dict, index, 'радио & ~ утро'))

print_result(search(dict, index, 'шкатулка | такие'))

print_result(search(dict, index, 'шкатулка  &  ~ такие'))

print_result(search(dict, index, '~ дефицит & корабль & гемма | дефицит '))
