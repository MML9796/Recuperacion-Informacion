import os
import re
import nltk
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from whoosh.index import open_dir
from whoosh import qparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

# Configurar para español
stop_words = set(stopwords.words('spanish'))
stemmer = SnowballStemmer('spanish')

def elimina_no_alfanumerico(tokens):
    return [re.sub(r'[^\w]', '', token)
            for token in tokens
            if re.search(r'\w', token)]

def elimina_stopwords(tokens):
    return [token for token in tokens if token not in stop_words]

def aplica_stemmer(tokens):
    return [stemmer.stem(token) for token in tokens]

def procesar_texto(texto):
    texto = texto.lower()
    # Tokenizar
    tokens = word_tokenize(texto)
    tokens = elimina_no_alfanumerico(tokens)
    tokens = elimina_stopwords(tokens)
    tokens = aplica_stemmer(tokens)
    
    return " ".join(tokens)

def procesar_query_booleana(query_str):
    """
    Procesa la consulta manteniendo los operadores lógicos booleanos intactos,
    pero aplicando el stemmer y eliminación de stopwords a los términos de búsqueda.
    """
    # Separar paréntesis para tratarlos como tokens independientes
    query_str = query_str.replace('(', ' ( ').replace(')', ' ) ')
    tokens = query_str.split()
    
    procesados = []
    for t in tokens:
        if t in ['AND', 'OR', 'NOT', '(', ')']:
            procesados.append(t)
        else:
            t_proc = procesar_texto(t)
            if t_proc:
                procesados.append(t_proc)
            
    return " ".join(procesados)

def obtener_resultados_booleanos(query_str, index_dir="indexdir"):
    ix = open_dir(index_dir)
    query_procesada = procesar_query_booleana(query_str)
    retrieved_ids = set()
    with ix.searcher() as searcher:
        parser = qparser.QueryParser("contenido", ix.schema)
        query = parser.parse(query_procesada)
        results = searcher.search(query, limit=None) # limit=None para devolver todos
        for r in results:
            retrieved_ids.add(int(r['id']))
    return retrieved_ids

def obtener_resultados_coseno(query_str, documentos):
    query_procesada = procesar_texto(query_str)
    textos = [doc['contenido'] for doc in documentos]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(textos)
    query_vector = vectorizer.transform([query_procesada])
    
    similitudes = cosine_similarity(query_vector, tfidf_matrix).flatten()
    indices_ordenados = np.argsort(similitudes)[::-1]
    
    ranked_ids = []
    for idx in indices_ordenados:
        score = similitudes[idx]
        if score > 0.00:
            doc = documentos[idx]
            ranked_ids.append(int(doc['id']))
    return ranked_ids
