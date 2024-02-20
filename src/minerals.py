import numpy as np

import requests

from bs4 import BeautifulSoup

from bson import ObjectId

from config import get_mongo_collection

from src.embbedings import calculate_cosine_similarity, generate_embedding

def extract_item(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    content_div = soup.find('div', class_='mw-content-ltr mw-parser-output')
    paragraph_content = ''
    
    image_td = soup.find('td', class_='infobox-image')
    image_url = ''
    image_caption = ''

    if content_div:
        first_h2 = content_div.find('h2')
        if first_h2:
            next_p = first_h2.find_next_sibling('p')
            if next_p:
                paragraph_content = next_p.get_text(strip=True)
    
    if image_td:
        image_tag = image_td.find('img')
        if image_tag and 'src' in image_tag.attrs:
            image_url = f"https:{image_tag['src']}"
        caption_div = image_td.find('div', class_='infobox-caption')
        if caption_div:
            image_caption = caption_div.get_text(strip=True)

    return paragraph_content, image_url, image_caption

def extract_list(max):
    url = 'https://en.wikipedia.org/wiki/List_of_minerals'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    minerals = {}
    # Alteração aqui: usando find_all para pegar todas as divs
    minerals_divs = soup.find_all('div', class_='div-col')
    
    # Iterando por cada div encontrada
    for div in minerals_divs:
        mineral_links = div.find_all('li')
        
        # Ajuste para garantir que não ultrapasse o máximo definido
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
    vector_description = generate_embedding(document['description'])
    document['vector_name'] = vector_name.tolist()
    document['vector_description'] = vector_description.tolist()

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
            # get loop item similiarity
            item_vector_name = np.array(item.get('vector_name', False))
            item_vector_description = np.array(item.get('vector_description', False))

            # compare item and searched embedding
            vector_name_similarity = calculate_cosine_similarity(search_embedding, item_vector_name)
            vector_description_similarity = calculate_cosine_similarity(search_embedding, item_vector_description)

            # set similarity in searched item
            item['name_similarity'] = vector_name_similarity
            item['description_similarity'] = vector_description_similarity

            # order index
            item['similarity'] = vector_name_similarity

            # if similarity > float(0.1): search_result.append(item)
        else:
            item['similarity'] = 1
            
        # sheck threshold before append 
        item['vector_name'] = True
        item['vector_description'] = True
        search_result.append(item)

    # sort search result
    search_result.sort(key=lambda x: x['similarity'], reverse=True)
    
    return search_result

def sync_minerals(max):
    minerals = extract_list(max)
    for mineral_name, mineral_url in minerals.items():
        print('Syncing mineral:', mineral_name)
        extracted_info, image_url, image_caption = extract_item(mineral_url)
        print('Extracted Info:', extracted_info)
        # Prepara o documento para inserir no MongoDB
        mineral_document = {
            "name": mineral_name,
            "url": mineral_url,
            "description": extracted_info,
            "image_url": image_url,  
            "image_caption": image_caption  
        }
        save_minerals(mineral_document)
        
    return True
