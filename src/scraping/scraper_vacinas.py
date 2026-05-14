import requests
import re
import json
import os
import time
from bs4 import BeautifulSoup

# Dados na memória enquanto o bot roda
# Começa vazio e é preenchido na primeira consulta
_cache = {}

# Endereço do site que vamos acessar
URL = 'https://www.gov.br/saude/pt-br/vacinacao/calendario'

# Onde o arquivo JSON vai ser salvo (dentro da pasta scraping/)
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'cache_vacinas.json')

# Quantas horas o JSON é válido antes de atualizar
CACHE_HORAS = 48

# Cabeçalho que simula um navegador real
# Sem isso, alguns sites bloqueiam o acesso
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}

# Cada perfil tem um título diferente na página do Ministério da Saúde
# Usamos esse texto para encontrar a seção certa no HTML
PERFIS_TITULOS = {
    'crianca':     'Criança (0 a 9 anos',
    'adolescente': 'Adolescente (10 a 19 anos',
    'adulto':      'Adulto (',
    'idoso':       'Idoso (',
    'gestante':    'Gestante (a gestante'
}


# -------------------------------------------------------
# CACHE — salvar e carregar os dados no arquivo JSON
# -------------------------------------------------------

def _cache_valido():
    # Verifica se o arquivo JSON existe e ainda está dentro do prazo de 48h
    # Retorna True (válido) ou False (precisa atualizar)

    if not os.path.exists(CACHE_FILE):
        return False  # arquivo não existe ainda

    segundos_desde_criacao = time.time() - os.path.getmtime(CACHE_FILE)
    limite_em_segundos = CACHE_HORAS * 3600  # 48h convertido para segundos

    return segundos_desde_criacao < limite_em_segundos


def _salvar_cache(dados):
    # Recebe o dicionário com todos os dados e salva no arquivo JSON
    # ensure_ascii=False → mantém acentos (ã, é, ç...)
    # indent=2 → deixa o arquivo legível com indentação
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print("Cache salvo em JSON!")


def _carregar_cache():
    # Lê o arquivo JSON e converte de volta para dicionário Python
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    print("Cache carregado com sucesso!")
    return dados


# -------------------------------------------------------
# SCRAPING — acessar o site e coletar os dados
# -------------------------------------------------------

def _fazer_scraping():
    # Acessa o site do Ministério da Saúde e coleta os dados de todos os perfis
    print("Buscando dados no site do Ministério da Saúde...")

    response = requests.get(URL, timeout=30, headers=HEADERS)

    # Se o site não respondeu corretamente, lança um erro
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar o site: HTTP {response.status_code}")

    # Transforma o HTML da página em algo que podemos navegar
    soup = BeautifulSoup(response.text, 'html.parser')
    resultado = {}

    # Para cada perfil, chama a função que extrai as vacinas
    for perfil, titulo in PERFIS_TITULOS.items():
        resultado[perfil] = _extrair_perfil(soup, titulo)
        print(f"Perfil '{perfil}': {len(resultado[perfil])} fases encontradas")

    return resultado


def _extrair_perfil(soup, titulo_perfil):
    # Recebe a página inteira e o título do perfil
    # Devolve um dicionário com as fases e vacinas daquele perfil
    fases = {}

    # Procura no HTML a tag que contém o título do perfil
    titulo_encontrado = None
    for tag in soup.find_all(['strong', 'b']):
        if titulo_perfil in tag.get_text():
            titulo_encontrado = tag
            break

    # Se não achou o título, avisa e retorna vazio
    if not titulo_encontrado:
        print(f"Aviso: '{titulo_perfil}' não encontrado na página")
        return fases

    # Sobe na estrutura do HTML para pegar o bloco que contém as fases
    bloco_pai = titulo_encontrado.find_parent(['p', 'div', 'section'])
    if not bloco_pai:
        return fases

    # A lista de fases fica logo após o bloco do perfil
    lista_fases = bloco_pai.find_next_sibling('ul')
    if not lista_fases:
        lista_fases = bloco_pai.find_next('ul')
    if not lista_fases:
        return fases

    # Percorre cada fase (ex: "Ao nascer", "2 meses", "9 a 14 anos"...)
    for item_fase in lista_fases.find_all('li', recursive=False):

        # Pega o nome da fase — é o primeiro texto dentro do item
        nome_fase = ''
        for filho in item_fase.children:
            if hasattr(filho, 'get_text'):
                texto = filho.get_text(strip=True)
            else:
                texto = str(filho).strip()
            if texto:
                nome_fase = texto
                break

        if not nome_fase:
            continue  # pula se não achou nome

        # Dentro de cada fase há uma sublista com as vacinas
        lista_vacinas = item_fase.find('ul')
        if not lista_vacinas:
            continue  # pula se não tem vacinas nessa fase

        vacinas_encontradas = []

        # Percorre cada vacina da fase
        for item_vacina in lista_vacinas.find_all('li', recursive=False):
            # Pega todo o texto da vacina em uma linha só
            texto = item_vacina.get_text(separator=' ', strip=True)

            # Nome: tudo antes do primeiro '('
            # Ex: "Hepatite B (1 dose)..." → "Hepatite B"
            nome = texto.split('(')[0].strip()
            nome = re.sub(r'^vacinas?\s+', '', nome, flags=re.IGNORECASE).strip()

            # Dose: texto dentro do primeiro parênteses
            # Ex: "Hepatite B (1 dose)..." → "1 dose"
            dose = ''
            if '(' in texto:
                dose = texto.split('(')[1].split(')')[0].strip()

            # Doenças prevenidas: texto após o marcador
            # Ex: "Doenças evitadas: hepatite B, hepatite D"
            previne = ''
            for marcador in ['Doenças evitadas:', 'Doença evitada:']:
                if marcador in texto:
                    previne = texto.split(marcador)[-1].strip()
                    if 'Obs.:' in previne:
                        previne = previne.split('Obs.:')[0].strip()
                    previne = ' '.join(previne.split())
                    break

            # Só adiciona se tiver nome
            if nome:
                vacinas_encontradas.append({
                    'vacina': nome.capitalize(),       # primeira letra maiúscula
                    'dose':   ' '.join(dose.split()),  # remove espaços extras
                    'evita':  previne
                })

        # Só salva a fase se tiver pelo menos uma vacina
        if vacinas_encontradas:
            fases[nome_fase] = vacinas_encontradas

    return fases


# -------------------------------------------------------
# FUNÇÕES PÚBLICAS — usadas pelos outros arquivos
# -------------------------------------------------------

def busca_vacinas(perfil=None):
    global _cache

    # Se o _cache está vazio, tenta carregar os dados
    if not _cache:
        if _cache_valido():
            _cache = _carregar_cache()  # rápido: lê o JSON salvo
        else:
            _cache = _fazer_scraping()  # lento: acessa o site
            _salvar_cache(_cache)       # salva para usar nas próximas vezes

    # Se passou um perfil, retorna só os dados dele
    # Ex: busca_vacinas('idoso') → retorna só as fases do idoso
    if perfil:
        return _cache.get(perfil, {})  # {} = vazio se o perfil não existir

    return _cache  # sem perfil → retorna tudo


def _normalizar(texto):
    # Deixa o texto em minúsculas e remove espaços extras
    # Usado para comparar textos sem se preocupar com maiúsculas
    # Ex: "  A partir DOS 60 anos  " → "a partir dos 60 anos"
    return ' '.join(texto.lower().split())


def buscar_fase(perfil, fase_busca):
    # Busca as vacinas de uma fase dentro de um perfil
    # Tenta de 3 formas diferentes para ser flexível
    dados = busca_vacinas(perfil)
    fase_norm = _normalizar(fase_busca)

    # Tentativa 1: texto exatamente igual (ignorando maiúsculas e espaços)
    for chave, vacinas in dados.items():
        if _normalizar(chave) == fase_norm:
            return vacinas

    # Tentativa 2: um texto contém o outro
    # Ex: "60 anos" está dentro de "a partir dos 60 anos"
    for chave, vacinas in dados.items():
        chave_norm = _normalizar(chave)
        if fase_norm in chave_norm or chave_norm in fase_norm:
            return vacinas

    # Tentativa 3: compara só os números
    # Ex: busca "60" → bate com "A partir dos 60 anos"
    # Útil se o site mudar o texto mas manter os números
    numeros_busca = re.findall(r'\d+', fase_busca)
    if numeros_busca:
        for chave, vacinas in dados.items():
            numeros_chave = re.findall(r'\d+', chave)
            if numeros_busca == numeros_chave:
                return vacinas

    # Nenhuma tentativa funcionou → retorna lista vazia
    return []