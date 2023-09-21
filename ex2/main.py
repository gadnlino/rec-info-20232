import json
import os

# Para executar : 'python main.py'
# Para alterar o conjunto de documentos utilizados e suas queries e parâmetros
# , modificar os arquivos dentro das pastas começadas com 'doc_group'

# Os arquivos de queries tem sempre 2 linhas:
# Linha 1: tipo da query(AND ou OR)
# Linha 2: definição da query

def normalize(string: str):

    return string.upper()

#Alterar para 'doc_group_2' para executar com valores do exercício 2
working_directory = 'doc_group_2'

separator_file = 'separators.txt'

stopwords_file = 'stopwords.txt'

index_file = 'index.json'

query_file = 'query.txt'

forbidden_files = [separator_file, stopwords_file, index_file, query_file]

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

#  o index é um json no formato:
# {"token1": {"nome_documento_1": frequencia_documento_1, "nome_documento_2": frequencia_documento_2}}
def create_index():
    idx = {}

    for file in os.listdir(working_directory):
        if(file.endswith(".txt") and file not in forbidden_files):

            document_text = open(f'./{working_directory}/{file}', 'r', encoding='utf8').read()

            tokens = execute_preprocessing(document_text)

            for t in tokens:
                if(t not in idx):
                    idx[t] = {}

                if(file not in idx[t]):
                        idx[t][file] = 1
                else:
                    idx[t][file] = idx[t][file] + 1

    idx_json_str = json.dumps(idx)

    with open(f'{working_directory}/{index_file}','w', encoding='utf8') as f:

        f.write(idx_json_str)

if(not os.path.exists(f'./{working_directory}/{index_file}')):
    create_index()

with open(f'{working_directory}/{index_file}', encoding='utf8') as f:

    idx = json.loads(f.read())

query_type = None
query_tokens = None

with open(f'{working_directory}/{query_file}', encoding='utf8') as f:
    query_type = f.readline().strip().upper()
    query_tokens = execute_preprocessing(f.readline())

first_token = query_tokens.pop(0)

result = set(idx[first_token].keys())

for t in query_tokens:
    if(t in idx):
        if(query_type == 'OR'):
            result = set(result).union(set(idx[t].keys()))
        else:
            result = set(result).intersection(set(idx[t].keys()))

result = list(result)

result.sort()

print(result)