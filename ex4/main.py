import os
import pandas as pd
import math
# Para instalar as dependências : 'pip install -r requirements.txt'
# Para executar : 'python main.py'
# Para alterar o conjunto de documentos utilizados e suas queries e parâmetros
# , modificar os arquivos dentro das pastas começadas com 'doc_group'

working_directory = 'doc_group_1'
separator_file = 'separators.txt'
stopwords_file = 'stopwords.txt'
frequencies_file = 'frequencies.csv'
index_file = 'weights.csv'
query_file = 'query.txt'

forbidden_files = [separator_file, stopwords_file, index_file, query_file, frequencies_file]

constants = {
    'k1': 1.0,
    'b': 0.75
}

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

def get_query_similarities(query):
    frequencies = get_frequencies()

    query_idx = {}

    query_tokens = list(set(execute_preprocessing(query)))

    N = len(documents)

    document_lengths = {}
    document_texts = {}
    document_tokens = {}
    avg_doclen = 0

    for d in documents:
        document_text = open(f'./{working_directory}/{d}', 'r', encoding='utf8').read()

        document_texts[d] = document_text

        document_tokens[d] = execute_preprocessing(document_text)

        query_idx[d] = 0
        l = len(document_tokens[d])
        document_lengths[d] = l
        avg_doclen += l

    avg_doclen /= N

    for d in documents:
        len_dj = document_lengths[d]
        
        for t in query_tokens: 
            n_i = 0

            for i in list(frequencies.loc[t]):
                if i > 0:
                    n_i += 1
            
            f_ij = document_tokens[d].count(t)

            beta = (constants['k1'] + 1) * f_ij/(f_ij + constants['k1']*((1-constants['b'] + constants['b']*len_dj/avg_doclen)))

            query_idx[d] += beta * math.log2((N - n_i + 0.5)/(n_i + 0.5))
    
    return query_idx

query = None

with open(f'{working_directory}/{query_file}', encoding='utf8') as f:
    query = f.readline()

result = get_query_similarities(query)

print('query: '+ query)

print()
print('result: ')

print()
for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True): print(k, v)