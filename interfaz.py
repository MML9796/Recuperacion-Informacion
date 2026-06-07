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
            coincidentes = [doc for doc in documentos if int(doc['id']) in res]
            print(f"\nSe encontraron {len(coincidentes)} películas:")
            for i, doc in enumerate(coincidentes, 1):
                print(f"{i}. {doc['titulo']} ({doc['genero']}) - Idioma: {doc['idioma']}")
            
            while True:
                op = input("\nSelecciona el número de película para ver detalles (o Enter para volver): ").strip()
                if op == "":
                    break
                if op.isdigit() and 1 <= int(op) <= len(coincidentes):
                    peli = coincidentes[int(op) - 1]
                    print("\n" + "-"*50)
                    print(f"Título: {peli['titulo']}")
                    print(f"Género: {peli['genero']}")
                    print(f"Idioma: {peli['idioma']}")
                    print(f"Sinopsis: {peli['sinopsis']}")
                    print(f"Reseña de usuarios: {peli['reseña']}")
                    print("-"*50)
                else:
                    print("Opción incorrecta.")
                    
    elif opcion == "2":
        query = input("\nIntroduce los términos de búsqueda (ej: fantasía familiar animación): ")
        res = obtener_resultados_coseno(query, documentos)
        if not res:
            print("\nNo se encontraron resultados.")
        else:
            coincidentes = []
            for doc_id in res:
                for doc in documentos:
                    if int(doc['id']) == doc_id:
                        coincidentes.append(doc)
                        break
            
            print(f"\nSe encontraron {len(coincidentes)} películas (ordenadas por relevancia):")
            for i, doc in enumerate(coincidentes, 1):
                print(f"{i}. {doc['titulo']} ({doc['genero']}) - Idioma: {doc['idioma']}")
            
            while True:
                op = input("\nSelecciona el número de película para ver detalles (o Enter para volver): ").strip()
                if op == "":
                    break
                if op.isdigit() and 1 <= int(op) <= len(coincidentes):
                    peli = coincidentes[int(op) - 1]
                    print("\n" + "-"*50)
                    print(f"Título: {peli['titulo']}")
                    print(f"Género: {peli['genero']}")
                    print(f"Idioma: {peli['idioma']}")
                    print(f"Sinopsis: {peli['sinopsis']}")
                    print(f"Reseña de usuarios: {peli['reseña']}")
                    print("-"*50)
                else:
                    print("Opción incorrecta.")
                        
    elif opcion == "3":
        print("\n¡Hasta pronto!\n")
        break
        
    else:
        print("\nOpción no válida.")
