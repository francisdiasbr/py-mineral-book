import numpy as np
import requests
import re
from bs4 import BeautifulSoup
from bson import ObjectId
from config import get_mongo_collection
from src.embbedings import calculate_cosine_similarity, generate_embedding

def clean_text(text):
    # Remove múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    # Adiciona espaços após pontuações se necessário
    text = re.sub(r'([.,!?;:])([^\s])', r'\1 \2', text)
    # Corrige formatação de fórmulas químicas
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)  # Espaço entre números e letras (simples ajuste)
    return text.strip()

def extract_item(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    properties = {
        'Category': None,
        'Formula': None,
        'IMA Symbol': None,
        'Strunz classification': None,
        'Dana classification': None,
        'Crystal system': None,
        'Space group': None,
        'Unit cell': None,
        'Color': None,
        'Cleavage': None,
        'Fracture': None,
        'Mohs scale': None,
        'Luster': None,
        'Streak': None,
        'Diaphaneity': None,
        'Specific gravity': None,
        'Optical properties': None,
        'Ultraviolet fluorescence': None,
        'Absorption spectra': None,
        'image_url': '',
        'image_caption': '',
        'description_paragraph': ''
    }

    rows = soup.find_all('tr')
    for row in rows:
        header = row.find('th')
        data = row.find('td')
        if header and data and header.text.strip() in properties:
            properties[header.text.strip()] = data.text.strip()
    
        # Encontrar a última tag <tr>
    if rows:
        last_tr = rows[-2]
        
        description_paragraph = last_tr.find_next('p')
        if description_paragraph:
            paragraph_text = description_paragraph.get_text(separator=' ', strip=True)
            cleaned_text = clean_text(paragraph_text)
            print("cleaned:", cleaned_text)  # Dar console no primeiro parágrafo
            properties['description_paragraph'] = cleaned_text

    image_td = soup.find('td', class_='infobox-image')
    if image_td:
        image_tag = image_td.find('img')
        if image_tag and 'src' in image_tag.attrs:
            properties['image_url'] = f"https:{image_tag['src']}"
        caption_div = image_td.find('div', class_='infobox-caption')
        if caption_div:
            properties['image_caption'] = caption_div.get_text(strip=True)

    return properties

def extract_list(max):
    url = 'https://en.wikipedia.org/wiki/List_of_minerals'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    minerals = {}
    minerals_divs = soup.find_all('div', class_='div-col')
    
    for div in minerals_divs:
        mineral_links = div.find_all('li')
        
        for link in mineral_links[:max]:
            a = link.find('a')
            if a and 'href' in a.attrs:
                mineral_name = a.text.strip()
                mineral_url = f"https://en.wikipedia.org{a['href']}"
                minerals[mineral_name] = mineral_url
            # Decrementa max para garantir que a contagem total não exceda o máximo
            max -= 1
            if max <= 0:
                break
        if max <= 0:
            break

    return minerals

def save_minerals(document):
    
    collection = get_mongo_collection('minerals')
    
    # generate embedding
    vector_name = generate_embedding(document['name'])
    document['vector_name'] = vector_name.tolist()

    # condition to replace
    query = { 'name': document['name'] }

    # insert or replace if exists
    collection.replace_one(query, document, upsert=True)

    return True

def search_minerals(filters={}, search_text=''):

    collection = get_mongo_collection('minerals')

    # search with normal filter
    if filters.get('_id'):
        filters['_id'] = ObjectId(filters['_id'])

    # search with embedding
    if search_text:
        search_embedding = generate_embedding(search_text)

    # result array
    search_result = []

    # find and search items in collection
    for item in collection.find(filters):
        # serialize object id key
        item['_id'] = str(item['_id'])
        if search_text:
            item_vector_name = np.array(item.get('vector_name', False))

            vector_name_similarity = calculate_cosine_similarity(search_embedding, item_vector_name)

            # set similarity in searched item
            item['similarity'] = vector_name_similarity

            # verifica se a similaridade é maior que 40%
            if item['similarity'] > 0.4:
                search_result.append(item)
        else:
            # Se não houver texto de busca, considera-se a similaridade como 1 para manter o item na lista
            search_result.append(item)

            # Ordena os resultados pela similaridade, do maior para o menor
    search_result.sort(key=lambda x: x['similarity'], reverse=True)
    search_result = search_result[:10]

    return search_result

def sync_minerals(max):
    minerals = extract_list(max)
    for mineral_name, mineral_url in minerals.items():
        print('Syncing mineral:', mineral_name)
        properties = extract_item(mineral_url)
        print('Extracted Info:', properties)

        # Cria um novo dicionário para as propriedades convertidas
        converted_properties = {}
        for key, value in properties.items():
            # Converte cada chave para minúsculas e substitui espaços por underscores
            converted_key = key.replace(' ', '_').lower()
            converted_properties[converted_key] = value

        mineral_document = {
            "name": mineral_name,
            "url": mineral_url,
            **converted_properties
        }
        save_minerals(mineral_document)
        
    return True
