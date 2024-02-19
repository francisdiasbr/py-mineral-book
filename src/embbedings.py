import numpy as np

from config import get_openai_client

def calculate_cosine_similarity(vec_a, vec_b):
    """
    Calcula a similaridade do cosseno entre dois vetores.
    """
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    return dot_product / (norm_a * norm_b)

def generate_embedding(text):
    """
    Gera embeddings para o texto fornecido utilizando a nova API da OpenAI.
    """
    openai = get_openai_client()
    response = openai.embeddings.create(model='text-embedding-3-small', input=text, encoding_format='float')

    cut_dim = response.data[0].embedding[:256]  # Reduz o tamanho do vetor de embedding para os primeiros 256 elementos.
    norm_dim = normalize_l2(cut_dim)  # Normaliza o vetor reduzido.

    return norm_dim

def normalize_l2(x):
    """
    Normaliza um vetor usando a norma L2 (Euclidiana).
    Pode ser aplicado tanto a vetores (1D) quanto a matrizes (2D), onde a normalização é feita por linha.
    """
    x = np.array(x)  # Converte o input para um array Numpy para facilitar a manipulação.
    if x.ndim == 1:  # Se o array é 1D (um único vetor).
        norm = np.linalg.norm(x)  # Calcula a norma L2 do vetor.
        if norm == 0:  # Evita divisão por zero.
            return x
        return x / norm  # Retorna o vetor normalizado.
    else:  # Se o array é 2D (uma matriz de vetores).
        norm = np.linalg.norm(x, 2, axis=1, keepdims=True)  # Calcula a norma L2 para cada linha (vetor) da matriz.
        return np.where(norm == 0, x, x / norm)  # Normaliza cada linha da matriz.
