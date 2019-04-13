import os
import math
import collections
import pandas as pd
import json

lem_docs_path = 'lemmedFiles/'
index_path = 'index/'

docs_list = os.listdir(lem_docs_path)
docs_all_words = {}
in_dict = {}
tf_idf = {}
tf_dict = {}
idf_list = {}
dfr = pd.DataFrame
docs_count = len(docs_list)
for doc_id, item in enumerate(docs_list):
    with open(lem_docs_path + item, encoding='utf-8') as file:
        words = file.readline().split()
        docs_all_words[doc_id] = len(words)  # кол-во слов в конкретном файле
    for word in words:
        if word not in in_dict:
            in_dict[word] = [0] * docs_count
        in_dict[word][doc_id] = 1

for word in in_dict.keys():
    idf = math.log10(docs_count / collections.Counter(in_dict[word])[1])
    idf_list[word] = round(idf, 3)

    for doc_index in range(docs_count):
        tf = in_dict[word][doc_index] / docs_all_words[doc_index]
        if word not in tf_idf:
            tf_idf[word] = [0] * docs_count
            tf_dict[word] = [0] * docs_count
        tf_dict[word][doc_index] = round(tf, 5)
        tf_idf[word][doc_index] = round(float(tf) * float(idf), 5)

df_tf = pd.DataFrame(tf_dict)
df = pd.DataFrame()

df_tfidf = df.from_dict(tf_idf)
df_tf = df.from_dict(tf_dict)
#df_idf = df.from_dict(idf_list)
df_idf = pd.DataFrame(idf_list, index=idf_list.keys())

df_tfidf.to_csv('tf_idf.csv', sep=',', encoding='utf-8')
df_tf.to_csv('tf.csv', sep=',', encoding='utf-8')
df_idf.to_csv('idf.csv', sep=',', encoding='utf-8')

json.dump(idf_list, open('idf.json', 'w', encoding='utf-8'), ensure_ascii=False)
