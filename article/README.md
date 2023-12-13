# Instruções

### Passos iniciais
- E necessario baixar a base de dados armazenada no formato SQLite, a partir do seguinte link: https://drive.google.com/file/d/169G6ZdMLUoT-OAcoY1nrqE8uhdWtSOQZ/view?usp=sharing
- Extrair esse arquivo dentro da pasta `/src`
- No arquivo `sqlite_utils.py`, substituir o valor de `SQLITE_FILE` para o caminho do arquivo que foi extraído.

### Instalação das dependências

- Dentro da pasta `/src`, executar o seguinte comando: `pip install -r requirements.txt`

### Arquivo por arquivo

- `data_sampling/news.py` e `data_sampling/reddit.py`: Foram os arquivos utilizados para a amostragem dos tweets e comentários do reddit a partir dos dados brutos.
- `utils.py`: Arquivo com funções utilitarias usadas nos demais arquivos.
- `tokenizers.py`: Arquivo para realizar a tokenização dos textos, de acordo com o Porter Stemmer. Também possui uma chamada para tokenização de sentenças, que é usada para obter o resumo das notícias.
- `global_values.py`: Arquivo para obter as estatísticas globais dos documentos armazenados(número de tokens distintos, número médio de tokens por documento, etc).
- `sqlite_utils.py`: Camada de acesso aos dados armazenados no SQLite.
- `execute_processing.py`: E onde é feita a análise e a geração das métricas. A execução é feita com o comando: `python execute_processing.py`. Ao final da execução, são gerados 3 arquivos: `scores.csv`, contendo a similaridade da notícia com cada um dos documentos, `metrics.csv`, a métrica para cada notícia, e `average_metrics.csv`, as métricas quando consideradas todo o conjunto de dados.
