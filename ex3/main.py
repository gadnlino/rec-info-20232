import json
import os
import pandas as pd
import math
import numpy as np
# Para executar : 'python main.py'
# Para alterar o conjunto de documentos utilizados e suas queries e parâmetros
# , modificar os arquivos dentro das pastas começadas com 'doc_group'


# Os arquivos de queries tem sempre 2 linhas:
# Linha 1: tipo da query(AND ou OR)
# Linha 2: definição da query

#Alterar para 'doc_group_2' para executar com valores do exercício 2
working_directory = 'doc_group_2'
separator_file = 'separators.txt'
stopwords_file = 'stopwords.txt'
index_file = 'index.csv'
query_file = 'query.txt'

forbidden_files = [separator_file, stopwords_file, index_file, query_file]

def normalize(string: str):
    return string.upper() 

separators = \
        list(map(lambda x: normalize(x.replace('\n', '')) ,open(f'./{working_directory}/{separator_file}', 'r', encoding='utf8').readlines()))

stopwords = \
        list(map(lambda x: normalize(x.replace('\n', '')), open(f'./{working_directory}/{stopwords_file}', 'r', encoding='utf8').readlines()))

def tokenize(string: str):
    split_char = '$%'
    for s in separators:
        if not(s == ''):
            string = string.replace(s, split_char)

    tokens = list(filter(lambda x: x != '', string.split(split_char)))

    return tokens

def remove_stopwords(strings: 'list[str]'):
    tokens = list(filter(lambda x: x not in stopwords, strings))
    return tokens

def execute_preprocessing(text: str):
    normalized = normalize(text)
    tokens = tokenize(normalized)
    tokens = remove_stopwords(tokens)

    return tokens

documents = [file for file in os.listdir(working_directory) if file.endswith(".txt") and file not in forbidden_files]
documents.sort()

def create_index(query = None):
    all_tokens = list()

    document_texts = {}

    for doc in documents:
        document_text = open(f'./{working_directory}/{doc}', 'r', encoding='utf8').read()

        document_texts[doc] = document_text

        tokens = execute_preprocessing(document_text)

        if(len(all_tokens)> 0):
            all_tokens = list(set(all_tokens).union(set(tokens)))
        else:
            all_tokens = list(set(tokens))
    
    all_tokens.sort()

    frequencies = pd.DataFrame(index = list(all_tokens), columns=list(documents)).fillna(0)

    for d in document_texts:
        document_text = document_texts[d]
        for t in all_tokens:
            frequencies[d][t] = document_text.count(t)

    idx = pd.DataFrame(index = all_tokens, columns=documents).fillna(0)

    for d in documents:
        for t in all_tokens:
            f_td = frequencies[d][t]
            tf_td = 1 + math.log2(f_td) if f_td > 0 else 0.0
            
            n_i = 0

            for i in list(frequencies.loc[t]):
                if i > 0:
                    n_i += 1

            idf_i = math.log2(len(documents)/n_i) if f_td > 0 else 0

            idx[d][t] = tf_td * idf_i if f_td > 0 else 0
    
    if query != None:
        idx.insert(len(idx.columns)-1, 'query', [0]*len(all_tokens))

        query_tokens = list(set(execute_preprocessing(query)))
        for d in documents:
            for t in query_tokens: 
                n_i = 0

                for i in list(frequencies.loc[t]):
                    if i > 0:
                        n_i += 1
                
                idf_i = math.log2(len(documents)/n_i) if n_i > 0 else 0
                
                f_iq = query.count(t)

                tf = (1 + math.log2(f_iq)) if f_iq > 0 else 0

                idx['query'][t] = tf * idf_i

    return idx

if(not os.path.exists(f'./{working_directory}/{index_file}')):
    idx = create_index()
    idx.to_csv(f'{working_directory}/{index_file}')

idx = pd.read_csv(f'{working_directory}/{index_file}',index_col=0)

query = None

with open(f'{working_directory}/{query_file}', encoding='utf8') as f:
    query = f.readline()

idx_query = create_index(query=query)

result = {}

for d in documents:
    norm_query = np.linalg.norm(idx_query['query'])
    norm_d = np.linalg.norm(idx_query[d])
    
    result[d] = np.dot(idx_query['query'], idx_query[d])/(norm_d * norm_query) if norm_query > 0 and norm_d > 0 else 0

print(result)