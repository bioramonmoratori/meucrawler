# Meu primeiro crawler

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from queue import Queue

def crawl(start_url, max_depth=2):
    visited_links = set()
    queue = Queue()
    
    # Adiciona a URL inicial à fila com profundidade 0
    queue.put((start_url, 0))

    while not queue.empty():
        current_url, depth = queue.get()

        # Verifica se a URL já foi visitada
        if current_url in visited_links:
            continue

        try:
            # Faz a solicitação HTTP
            response = requests.get(current_url)
            if response.status_code != 200:
                # Ignora URLs que não retornam código 200 (OK)
                continue

            # Adiciona a URL atual ao conjunto de URLs visitadas
            visited_links.add(current_url)

            # Processa a página HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"Depth: {depth}, URL: {current_url}")

            # Extrai e adiciona links de posts encontrados à fila
            if depth < max_depth:
                for link in soup.find_all('a', {'data-testid': 'post-title'}, href=True):
                    print(link.text)
                    next_url = urljoin(current_url, link['href'])
                    queue.put((next_url, depth + 1))

        except Exception as e:
            print(f"Error processing {current_url}: {e}")

if __name__ == "__main__":
    start_url = "https://www.reddit.com/search/?q=duvida&type=link&cId=d1e406e0-f655-4634-9edc-601183f72c05&iId=b3278d8d-7ece-4fc2-8bf0-d35eb78cd632"
    crawl(start_url)
