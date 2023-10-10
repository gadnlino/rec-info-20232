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
frequencies_file = 'frequencies.csv'
index_file = 'weights.csv'
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

def get_frequencies():
    if(os.path.exists(f'./{working_directory}/{frequencies_file}')):
        frequencies = pd.read_csv(f'{working_directory}/{frequencies_file}',index_col=0)
        return frequencies

    all_tokens = list()

    document_tokens = {}

    for doc in documents:
        document_text = open(f'./{working_directory}/{doc}', 'r', encoding='utf8').read()

        tokens = execute_preprocessing(document_text)

        document_tokens[doc] = tokens
        
        if(len(all_tokens) > 0):
            all_tokens = list(set(all_tokens).union(set(tokens)))
        else:
            all_tokens = list(set(tokens))
    
    all_tokens.sort()

    frequencies = pd.DataFrame(index = list(all_tokens), columns=list(documents)).fillna(0)

    for d in document_tokens:
        document_text = document_tokens[d]

        for t in all_tokens:
            f = document_text.count(t)
            frequencies[d][t] = f
    
    frequencies.to_csv(f'./{working_directory}/{frequencies_file}')

    return frequencies

def get_weights():
    if(os.path.exists(f'./{working_directory}/{index_file}')):
        idx = pd.read_csv(f'{working_directory}/{index_file}', index_col=0)
        return idx

    frequencies = get_frequencies()

    idx = pd.DataFrame(index = frequencies.index, columns=documents).fillna(0)

    for d in documents:
        for t in list(frequencies.index):
            f_td = frequencies[d][t]
            tf_td = 1 + math.log2(f_td) if f_td > 0 else 0.0
            
            n_i = 0

            for i in list(frequencies.loc[t]):
                if i > 0:
                    n_i += 1

            idf_i = math.log2(len(documents)/n_i) if f_td > 0 else 0

            idx[d][t] = tf_td * idf_i if f_td > 0 else 0
    
    idx.to_csv(f'{working_directory}/{index_file}')

    return idx

def get_query_index(query):
    frequencies = get_frequencies()

    query_idx = pd.DataFrame(index=frequencies.index, columns=['query']).fillna(0)

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

            query_idx['query'][t] = tf * idf_i
    
    return query_idx

weights = get_weights()

query = None

with open(f'{working_directory}/{query_file}', encoding='utf8') as f:
    query = f.readline()

idx_query = get_query_index(query=query)

result = {}

for d in documents:
    norm_query = np.linalg.norm(idx_query['query'])
    norm_d = np.linalg.norm(weights[d])
    
    result[d] = np.dot(idx_query['query'], weights[d])/(norm_d * norm_query) if norm_query > 0 and norm_d > 0 else 0

print(result)