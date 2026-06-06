import os
from whoosh.index import open_dir
from funciones import obtener_resultados_booleanos, obtener_resultados_coseno

ix = open_dir("indexdir")
with ix.searcher() as searcher:
    documentos = list(searcher.all_stored_fields())

print("--- SISTEMA DE RECUPERACIÓN DE LA INFORMACIÓN ---")
print("1. Buscar con modelo Booleano")
print("2. Buscar con modelo TF-IDF y similitud de Coseno")
print("3. Salir")

while True:
    opcion = input("\nElige una opción (1-3): ").strip()
    
    if opcion == "1":
        query = input("\nIntroduce la consulta booleana (ej: ciencia AND ficción AND NOT romance): ")
        res = obtener_resultados_booleanos(query)
        if not res:
            print("\nNo se encontraron películas.")
        else:
            print(f"\nSe encontraron {len(res)} películas:")
            for doc in documentos:
                if int(doc['id']) in res:
                    print(f"- {doc['titulo']} ({doc['genero']}) - Idioma: {doc['idioma']}")
                    
    elif opcion == "2":
        query = input("\nIntroduce los términos de búsqueda (ej: fantasía familiar animación): ")
        res = obtener_resultados_coseno(query, documentos)
        if not res:
            print("\nNo se encontraron resultados.")
        else:
            print(f"\nSe encontraron {len(res)} películas (ordenadas por relevancia):")
            for i, doc_id in enumerate(res, 1):
                for doc in documentos:
                    if int(doc['id']) == doc_id:
                        print(f"{i}. {doc['titulo']} ({doc['genero']}) - Idioma: {doc['idioma']}")
                        break
                        
    elif opcion == "3":
        print("\n¡Hasta pronto!\n")
        break
        
    else:
        print("\nOpción no válida.")
