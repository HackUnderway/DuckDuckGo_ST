#!/usr/bin/python
# -*- coding: utf-8 -*-

# By: Hack Underway

import requests
import argparse

def buscar_en_duckduckgo(query, lang):
    """
    Realiza una búsqueda en DuckDuckGo usando la API Instant Answer y procesa los resultados.
    """
    url = 'https://api.duckduckgo.com/'
    params = {
        'q': query,
        'format': 'json',  # La API responde en JSON
        'no_html': 1,      # Elimina HTML de las respuestas
        'skip_disambig': 1,  # Omitir desambiguaciones
        'kl': f'{lang}'    # Filtro por idioma
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        data = response.json()
        procesar_resultados(query, data)
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    except ValueError:
        print("Error procesando la respuesta JSON.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def procesar_resultados(query, data):
    """
    Procesa los datos recibidos de DuckDuckGo y muestra los resultados de búsqueda.
    """
    if 'AbstractText' in data and data['AbstractText']:
        print(f"\nRespuesta de DuckDuckGo para '{query}':\n")
        print(data['AbstractText'])
    elif 'RelatedTopics' in data and data['RelatedTopics']:
        print(f"\nTemas relacionados para '{query}':\n")
        for topic in data['RelatedTopics'][:5]:  # Mostrar hasta 5 resultados
            if 'Text' in topic:
                topic_text = topic['Text']
                topic_url = topic.get('FirstURL', 'No URL disponible')
                print(f"- {topic_text}\n  Enlace: {topic_url}")
    else:
        print(f"No se encontraron resultados relevantes para '{query}'.")

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Herramienta para realizar búsquedas en DuckDuckGo 🦆.\n\n"
            "Ejemplo de uso:\n"
            "  python3 osint.py 'hacker' -l es-es\n\n"
            "Opciones:\n"
            "- QUERY: Término de búsqueda.\n"
            "- -l, --lang: Especifica el idioma de los resultados (por defecto: us-en).\n"
            "- -v, --version: Muestra la versión de la herramienta."
        ),
        formatter_class=argparse.RawTextHelpFormatter  # Permite un formato de texto crudo para la descripción
    )
    parser.add_argument('search', metavar='QUERY', type=str, nargs='?', help='Término de búsqueda para OSINT')
    parser.add_argument('-v', '--version', action='store_true', help='Muestra la versión de la herramienta')
    parser.add_argument('-l', '--lang', type=str, default='us-en', help='Idioma de los resultados (ejemplo: es-es, us-en)')

    args = parser.parse_args()

    if args.version:
        print("DuckduckGO_ST v1.0")
    elif args.search:
        print(f"Buscando información sobre: {args.search} en idioma {args.lang}")
        buscar_en_duckduckgo(args.search, args.lang)  # Llamar a la función de búsqueda
    else:
        print("No se proporcionó ningún término de búsqueda. Usa -h para ver las opciones.")

if __name__ == "__main__":
    main()
