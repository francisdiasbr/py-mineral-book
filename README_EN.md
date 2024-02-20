# 🔮 Mineral-book

*This code is a complete solution for extracting, processing, storing, and searching for information about minerals in a semantic way. It illustrates the application of NLP techniques and semantic search on real datasets, providing a foundation for recommendation systems, enhanced search, and text analysis.*

This project is part of a system that interacts with Wikipedia. It:

- Extracts information about minerals;
- Processes this information using Natural Language Processing (NLP) techniques to generate embeddings (vector representations), and uses these data both for storage and for semantic search in a MongoDB database.

## Main Functions:

`extract_list(max)`: This function accesses the list of minerals on Wikipedia and extracts the names and URLs of up to max minerals. The names and URLs are stored in a dictionary for later use.

`extract_item(url)`: Given the URL of a Wikipedia page, this function extracts the text from the first paragraph after the first level 2 header (`<h2>`). It is used to obtain a summarized description of a specific mineral.

`save_minerals(document)`: This function is responsible for saving the information of a mineral in MongoDB. It generates embeddings for the mineral's name and description using the function generate_embedding, and then saves or updates the entry in the database using the mineral's name as the key.

`search_minerals(filters={}, search_text='')`: This function searches for minerals in MongoDB using conventional filters and/or semantic text search. For semantic searches, it generates an embedding of the search text, compares this embedding with the stored embeddings of the minerals (calculating cosine similarity), and returns the results ordered by similarity.

`sync_minerals(max)`: This function organizes the process of synchronizing minerals from Wikipedia with the database, described as:

- For each mineral in the list obtained by the extract_list function, it extracts the description using extract_item, prepares a document with this information and the generated embeddings, and saves this document in MongoDB through the save_minerals function.

## External Components and Techniques:

`Embeddings (Vector Representations)`: The system uses embeddings to semantically represent the names and descriptions of minerals. These embeddings are high-dimensional vectors that capture the context and meaning of words, allowing for semantic searches based on textual content similarity.

`Cosine Similarity`: To compare embeddings and perform semantic searches, the system uses cosine similarity. This metric measures the cosine of the angle between two vectors in multidimensional space, being an effective way of determining how similar two documents are in terms of their semantic content.

`MongoDB`: The system uses MongoDB, a NoSQL database, to store the data of minerals, including their names, URLs, textual descriptions, and their embeddings. MongoDB is chosen for its flexibility in handling documents and complex data structures, like vectors.

## How to Use

### Install the local environment (once)
python3 -m venv venv

### Activate the local environment
source venv/bin/activate

### Install the requirements
pip install -r requirements.txt

### Run
python app.py





