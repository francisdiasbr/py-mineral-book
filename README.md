# 🔮  Mineral-book

*Este código é uma solução completa para extrair, processar, armazenar e buscar informações sobre minerais de forma semântica. Ele ilustra a aplicação de técnicas de NLP e busca semântica em conjuntos de dados reais, proporcionando uma base para sistemas de recomendação, busca aprimorada e análise de texto.*

Este projeto faz parte de um sistema que interage com a Wikipedia. Ele: 
- Extrai informações sobre minerais;
- Processa essas informações utilizando técnicas de Processamento de Linguagem Natural (NLP) para gerar embeddings (representações vetoriais), e utiliza esses dados tanto para armazenamento quanto para busca semântica em um banco de dados MongoDB. 


## Funções principais:

`extract_list(max)`: Esta função acessa a lista de minerais na Wikipedia e extrai os nomes e URLs de até max minerais. Os nomes e URLs são armazenados em um dicionário para uso posterior.

`extract_item(url)`: Dada a URL de uma página da Wikipedia, essa função extrai o texto do primeiro parágrafo após o primeiro cabeçalho de nível 2 (`<h2>`). É utilizada para obter uma descrição resumida de um mineral específico.

`save_minerals(document)`: Esta função é responsável por salvar as informações de um mineral no MongoDB. Ela gera embeddings para o nome e descrição do mineral usando a função generate_embedding, e então salva ou atualiza a entrada no banco de dados usando o nome do mineral como chave.

`search_minerals(filters={}, search_text='')`: Esta função busca minerais no MongoDB utilizando filtros convencionais e/ou busca semântica baseada em texto. Para buscas semânticas, ela gera um embedding do texto de busca, compara esse embedding com os embeddings armazenados dos minerais (calculando a similaridade do cosseno), e retorna os resultados ordenados pela similaridade.

`sync_minerals(max)`: Esta função organiza o processo de sincronização dos minerais da Wikipedia em conjunto com o banco de dados, descrita:
- Para cada mineral na lista obtida pela função `extract_list`, ela extrai a descrição usando `extract_item`, prepara um documento com essas informações e os embeddings gerados, e salva esse documento no MongoDB através da função `save_minerals`.

## Componentes Externos e Técnicas:

`Embeddings (Representações Vetoriais)`: O sistema utiliza embeddings para representar semanticamente os nomes e descrições dos minerais. Esses embeddings são vetores de alta dimensão que capturam o contexto e o significado das palavras, permitindo buscas semânticas baseadas na similaridade do conteúdo textual.

`Similaridade do Cosseno`: Para comparar embeddings e realizar buscas semânticas, o sistema utiliza a similaridade do cosseno. Essa métrica mede o cosseno do ângulo entre dois vetores no espaço multidimensional, sendo uma maneira eficaz de determinar quão semelhantes são dois documentos em termos de seu conteúdo semântico.

`MongoDB`: O sistema utiliza o MongoDB, um banco de dados NoSQL, para armazenar os dados dos minerais, incluindo os nomes, URLs, descrições textuais e seus embeddings. O MongoDB é escolhido por sua flexibilidade em lidar com documentos e estruturas de dados complexas, como vetores.


## How to use

### install local environment (once)
python3 -m venv venv

### active local environment
source venv/bin/activate

### install requirements
pip install -r requirements.txt

### run
python app.py
