import requests
import re
import json
import os
import time
from bs4 import BeautifulSoup

# Dados na memória enquanto o bot roda
_cache = {}

# URL do calendário do Ministério da Saúde
URL = 'https://www.gov.br/saude/pt-br/vacinacao/calendario'

# Arquivo de cache (junto ao scraper)
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'cache_vacinas.json')
CACHE_HORAS = 48

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}

PERFIS_TITULOS = {
    'crianca':     'Criança (0 a 9 anos',
    'adolescente': 'Adolescente (10 a 19 anos',
    'adulto':      'Adulto (',
    'idoso':       'Idoso (',
    'gestante':    'Gestante (a gestante'
}

# -----------------------
# Funções de cache
# -----------------------
def _cache_valido():
    if not os.path.exists(CACHE_FILE):
        return False
    segundos_desde_criacao = time.time() - os.path.getmtime(CACHE_FILE)
    return segundos_desde_criacao < (CACHE_HORAS * 3600)

def _salvar_cache(dados):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def _carregar_cache():
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# -----------------------
# SCRAPING
# -----------------------
def _fazer_scraping():
    print("Buscando dados no site do Ministério da Saúde...")
    response = requests.get(URL, timeout=30, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar o site: HTTP {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    resultado = {}

    for perfil, titulo in PERFIS_TITULOS.items():
        resultado[perfil] = _extrair_perfil(soup, titulo)
        print(f"Perfil '{perfil}': {len(resultado[perfil])} fases encontradas")

    return resultado


def _extrair_perfil(soup, titulo_perfil):
    fases = {}

    # Localiza o título do perfil no HTML
    titulo_encontrado = None
    for tag in soup.find_all(['strong', 'b']):
        if titulo_perfil in tag.get_text():
            titulo_encontrado = tag
            break

    if not titulo_encontrado:
        # Não encontrado: devolve vazio
        return fases

    bloco_pai = titulo_encontrado.find_parent(['p', 'div', 'section'])
    if not bloco_pai:
        return fases

    lista_fases = bloco_pai.find_next_sibling('ul') or bloco_pai.find_next('ul')
    if not lista_fases:
        return fases

    for item_fase in lista_fases.find_all('li', recursive=False):
        # --- Nome da fase (ex: "Ao nascer", "9 a 14 anos", "A partir da 28ª semana gestacional")
        nome_fase = ''
        for filho in item_fase.children:
            if hasattr(filho, 'get_text'):
                texto = filho.get_text(strip=True)
            else:
                texto = str(filho).strip()
            if texto:
                # Normalização mínima do nome da fase
                texto = texto.replace('\u00A0', ' ')
                texto = ' '.join(texto.split())
                texto = re.sub(r'^[\s\-\u2022]+', '', texto)  # remove leading bullets/spaces/traços
                nome_fase = texto
                break

        if not nome_fase:
            continue

        # Sublista com as vacinas (UL dentro do LI)
        lista_vacinas = item_fase.find('ul')
        if not lista_vacinas:
            continue

        vacinas_encontradas = []

        for item_vacina in lista_vacinas.find_all('li', recursive=False):
            # Pega todo o texto em uma linha única
            texto = item_vacina.get_text(separator=' ', strip=True)

            # ======= ALTERAÇÕES DE LIMPEZA E NORMALIZAÇÃO (MINIMAS) =======
            # 1) Remove NBSP que às vezes quebra a formatação
            texto = texto.replace('\u00A0', ' ')

            # 2) Normaliza espaços
            texto = ' '.join(texto.split())

            # Nome da vacina: parte antes do primeiro '(' (se existir)
            nome = texto.split('(')[0].strip()
            nome = re.sub(r'^vacinas?\s+', '', nome, flags=re.IGNORECASE).strip()

            # Dose: conteúdo dentro do primeiro parênteses (se houver e fechar)
            dose = ''
            if '(' in texto and ')' in texto:
                dose = texto.split('(')[1].split(')')[0].strip()
                dose = ' '.join(dose.split())

            # Previna: busca por marcadores (case-insensitive)
            previne = ''
            lower_text = texto.lower()
            for marcador in ['doenças evitadas:', 'doença evitada:']:
                if marcador in lower_text:
                    # pega substring após o marcador (usando o índice no lower_text para respeitar posição)
                    idx = lower_text.find(marcador) + len(marcador)
                    previne = texto[idx:].strip()

                    # Remove qualquer bloco de "Obs.:" que venha após o previne
                    lower_prev = previne.lower()
                    if 'obs.:' in lower_prev:
                        previne = previne[:lower_prev.find('obs.:')].strip()

                    # Corrige espaços estranhos antes de vírgulas e garante uma vírgula seguida de espaço
                    previne = re.sub(r'\s+,', ',', previne)
                    previne = re.sub(r',\s*', ', ', previne)

                    # Normaliza espaços extras
                    previne = ' '.join(previne.split())
                    break
            # ======= FIM DAS ALTERAÇÕES =======

            # Adiciona se tiver nome
            if nome:
                vacinas_encontradas.append({
                    'vacina': nome.strip().capitalize(),
                    'dose': dose,
                    'evita': previne
                })

        if vacinas_encontradas:
            fases[nome_fase] = vacinas_encontradas

    return fases

# -----------------------
# Funções públicas
# -----------------------
def busca_vacinas(perfil=None):
    global _cache
    if not _cache:
        if _cache_valido():
            _cache = _carregar_cache()
        else:
            _cache = _fazer_scraping()
            _salvar_cache(_cache)
    return _cache.get(perfil, _cache) if perfil else _cache


def _normalizar(texto):
    return ' '.join(texto.lower().split())


def buscar_fase(perfil, fase_busca):
    dados = busca_vacinas(perfil)
    fase_norm = _normalizar(fase_busca)

    # 1) igualdade após normalizar
    for chave, vacinas in dados.items():
        if _normalizar(chave) == fase_norm:
            return vacinas

    # 2) containment (mais flexível)
    for chave, vacinas in dados.items():
        chave_norm = _normalizar(chave)
        if fase_norm in chave_norm or chave_norm in fase_norm:
            return vacinas

    # 3) tentativa por números (ex: "28")
    numeros_busca = re.findall(r'\d+', fase_busca)
    if numeros_busca:
        for chave, vacinas in dados.items():
            numeros_chave = re.findall(r'\d+', chave)
            if numeros_busca == numeros_chave:
                return vacinas

    return []