import json
import os
import pandas as pd

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

#  o index é um json no formato:
# {"token1": {"nome_documento_1": frequencia_documento_1, "nome_documento_2": frequencia_documento_2}}
def create_index():
    idx = pd.DataFrame(index = documents)

    for file in documents:
        document_text = open(f'./{working_directory}/{file}', 'r', encoding='utf8').read()

        tokens = execute_preprocessing(document_text)

        for t in tokens:
            if(t not in idx):
                idx.insert(0, t, [0] * len(documents))

            if(file not in idx[t]):
                    idx[t][file] = 1
            else:
                idx[t][file] = idx[t][file] + 1

    
    idx.to_csv(f'{working_directory}/{index_file}')

if(not os.path.exists(f'./{working_directory}/{index_file}')):
    create_index()

idx = pd.read_csv(f'{working_directory}/{index_file}')

query_type = None
query_tokens = None

with open(f'{working_directory}/{query_file}', encoding='utf8') as f:
    query_type = f.readline().strip().upper()
    query_tokens = execute_preprocessing(f.readline())

first_token = query_tokens.pop(0)

result = set(list(idx.columns))

for t in query_tokens:
    if(t in idx):
        docs = [documents[i] for i in range(len(documents)) if idx[t][i] > 0]

        if(query_type == 'OR'):
            result = set().union(set(docs))
        else:
            result = set(result).intersection(set(docs))

result = list(result)

result.sort()

print(result)