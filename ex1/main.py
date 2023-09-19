import os

wd = 'doc_group_1'

separator_file = 'separators.txt'
stepwords_file = 'stopwords.txt'
index_file = 'index.json'
query_file = 'query.txt'

forbidden_files = [separator_file, stepwords_file, index_file, query_file]

idx = {}


def create_index():
    for file in os.listdir(wd):
        if(file.endswith(".txt") and file not in forbidden_files):
            file_text = open(f'./{wd}/{file}', 'r', encoding='utf8').read()

            print(file_text)

if(os.path.exists(f'./{wd}/{index_file}')):
    create_index()