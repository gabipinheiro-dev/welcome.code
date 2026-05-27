import requests
import json

import requests

# Célula 2: Busca de Postos Oficial e Segura
def buscar_postos_proximos(lat, lon, raio_metros=3000):
    url_osm = "https://overpass-api.de/api/interpreter"

    # Query que busca clínicas, hospitais e postos de saúde
    overpass_query = f'[out:json][timeout:25];(node["amenity"="clinic"](around:{raio_metros},{lat},{lon});node["healthcare"="centre"](around:{raio_metros},{lat},{lon});node["amenity"="hospital"](around:{raio_metros},{lat},{lon}););out body;'

    params = {'data': overpass_query}
    headers = {
        'User-Agent': 'BotFATEC_SJC_Vacinacao_v6/1.0 (fatecsjc.edu.br)',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url_osm, params=params, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"[Overpass] Erro HTTP {response.status_code}")
            return []

        data = response.json()
        elements = data.get('elements', [])
        print(f"[Overpass] Sucesso! Encontrados {len(elements)} estabelecimentos de saúde.")

        postos_encontrados = []
        for element in elements:
            tags = element.get('tags', {})
            nome = tags.get('name', "Unidade de Saúde / Posto")
            rua = tags.get('addr:street', '')
            numero = tags.get('addr:housenumber', '')

            if rua:
                endereco = f"{rua}, {numero}".strip(", ")
            else:
                endereco = "Endereço disponível no mapa"

            link_mapa = f"https://www.google.com/maps?q={element['lat']},{element['lon']}"

            postos_encontrados.append({
                'nome': nome,
                'endereco': endereco,
                'link': link_mapa
            })
        return postos_encontrados
    except Exception as e:
        print(f"[Overpass] Erro crítico na busca: {e}")
        return []
    
    # Célula 3: Testando com coordenadas reais (Exemplo: Região da casa da Gabrielle)
MINHA_LAT = -23.258372
MINHA_LON = -45.880977

print(f"Procurando postos num raio de 3km a partir de: {MINHA_LAT}, {MINHA_LON}...\n")

resultados = buscar_postos_proximos(MINHA_LAT, MINHA_LON)

# Verificamos se veio algum posto
if not resultados:
    print("Nenhum posto encontrado nessa região ou o servidor demorou para responder.")
else:
    print(f"Sucesso! Encontramos {len(resultados)} locais de saúde.\n")
    print("Mostrando os 5 primeiros mais próximos:\n")

    for indice, posto in enumerate(resultados[:5], start=1):
        print(f"{indice}. 🏥 {posto['nome']}")
        print(f"   📍 Endereço: {posto['endereco']}")
        print(f"   🗺️ Link para rota: {posto['link']}")
        print("-" * 50)

        # Célula 4: Instalando a biblioteca do Telegram e configurando o Bot
!pip install pyTelegramBotAPI

import telebot
from telebot import types

TOKEN_TELEGRAM = "8627564867:AAHqseyt7eCVH1YZaAA9HhKgtHvSi8M0S-o"

bot = telebot.TeleBot(TOKEN_TELEGRAM)
print("Bot configurado com sucesso e pronto para receber comandos!")

# Célula 5: Código do Telegram Completo e Integrado (Sem Comandos Obrigatórios)
from telebot import types

# Função para criar o teclado fixo que vai aparecer para o usuário
def obter_teclado_permanente():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    botao_gps = types.KeyboardButton(text="📍 Enviar minha Localização Atual (Celular)", request_location=True)
    keyboard.add(botao_gps)
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def mensagem_boas_vindas(message):
    bot.send_message(
        message.chat.id,
        "👋 Olá! Seja bem-vindo ao buscador de Postos de Saúde.\n\n"
        "Aqui você pode descobrir o posto mais próximo de você de duas formas:\n"
        "📱 *No Celular:* Clique no botão azul aqui embaixo para enviar seu GPS.\n"
        "💻 *No Computador ou Celular:* Escreva diretamente o seu endereço ou CEP aqui no chat (Ex: _Rua Frutal, São José dos Campos_ ou _12233-596_).",
        reply_markup=obter_teclado_permanente(),
        parse_mode="Markdown"
    )

# 2. TRATAMENTO DE LOCALIZAÇÃO VIA GPS (Celular)
@bot.message_handler(content_types=['location'])
def receber_localizacao_gps(message):
    lat = message.location.latitude
    lon = message.location.longitude
    processar_e_responder_postos(message.chat.id, lat, lon, "sua localização atual")

# 3. TRATAMENTO DE TEXTO LIVRE E CEP
@bot.message_handler(content_types=['text'])
def ouvir_texto_livre(message):
    if message.text.startswith('/'):
        return

    texto_digitado = message.text.strip()

    # Validação simples: se o texto for muito curto
    if len(texto_digitado) < 4:
        bot.send_message(
            message.chat.id,
            "Olá! Para achar os postos, por favor, digite o seu endereço completo (Rua, Cidade) ou o seu CEP.",
            reply_markup=obter_teclado_permanente()
        )
        return

    bot.send_message(message.chat.id, f"🔍 Entendido! Buscando postos próximos a: '{texto_digitado}'...")

    # Chama a Célula 6 (ViaCEP + OpenStreetMap)
    lat, lon, nome_local = buscar_coordenadas_por_texto(texto_digitado)

    if lat and lon:
        processar_e_responder_postos(message.chat.id, lat, lon, nome_local)
    else:
        bot.send_message(
            message.chat.id,
            "❌ Não consegui encontrar esse endereço.\n\n"
            "Tente digitar de forma mais simples. Exemplo:\n"
            "👉 _Rua Frutal, São José dos Campos_\n"
            "👉 _12232-200_",
            reply_markup=obter_teclado_permanente(),
            parse_mode="Markdown"
        )

# 4. FUNÇÃO AUXILIAR QUE BUSCA OS POSTOS (CHAMA A CÉLULA 2) E RESPONDE O USUÁRIO
def processar_e_responder_postos(chat_id, lat, lon, nome_local):
    # Chama a Célula 2
    postos = buscar_postos_proximos(lat, lon)

    # Se a lista vier vazia, avisa o usuário com clareza
    if not postos:
        bot.send_message(
            chat_id,
            f"📍 Encontrei a região de:\n_{nome_local}_\n\n"
            "⚠️ Porém, não encontrei nenhum posto de saúde cadastrado num raio de 3km desse ponto no OpenStreetMap.\n\n"
            "Tente testar com outro endereço ou um CEP mais central!",
            reply_markup=obter_teclado_permanente(),
            parse_mode="Markdown"
        )
        return

    resposta = f"🏥 *Postos mais próximos de:*\n_{nome_local}_\n\n"
    for indice, posto in enumerate(postos[:5], start=1):
        resposta += f"*{indice}. {posto['nome']}*\n"
        resposta += f"📍 {posto['endereco']}\n"
        resposta += f"🔗 [Ver Rota no Google Maps]({posto['link']})\n\n"

    bot.send_message(
        chat_id,
        resposta,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=obter_teclado_permanente()
    )

# 🚀 INICIALIZAÇÃO DO BOT
print("Bot 100% automático e simplificado iniciado!")
while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        import time
        print(f"Erro no polling: {e}. Reiniciando em 5 segundos...")
        time.sleep(5)

        import requests
import re
from urllib.parse import quote

# Célula 6: Geocodificação Híbrida com Super Dicionário de Abreviações
def buscar_coordenadas_por_texto(texto_endereco):
    """
    Transforma texto livre ou CEP em coordenadas, tratando exaustivamente abreviações brasileiras.
    """
    busca = texto_endereco.strip().lower()

    # 1. IDENTIFICAÇÃO DE CEP
    apenas_numeros = re.sub(r'[^0-9]', '', busca)

    if len(apenas_numeros) == 8:
        print(f"[ViaCEP] Detectado formato de CEP: {apenas_numeros}. Buscando dados...")
        try:
            viacep_url = f"https://viacep.com.br/ws/{apenas_numeros}/json/"
            viacep_response = requests.get(viacep_url, timeout=10)

            if viacep_response.status_code == 200:
                cep_data = viacep_response.json()

                if "erro" not in cep_data:
                    rua = cep_data.get('logradouro', '')
                    cidade = cep_data.get('localidade', '')
                    estado = cep_data.get('uf', '')

                    busca_tratada = f"{rua}, {cidade} - {estado}"
                    print(f"[ViaCEP] CEP traduzido para: '{busca_tratada}'")
                else:
                    busca_tratada = busca
            else:
                busca_tratada = busca
        except Exception as e:
            busca_tratada = busca

    else:
        # 🚨 DICIONÁRIO DE ABREVIAÇÕES: Mapeia tudo o que o usuário pode digitar de forma encurtada
        substituicoes = {
            'av': 'avenida', 'av.': 'avenida',
            'r': 'rua', 'r.': 'rua',
            'pça': 'praça', 'pça.': 'praça', 'praca': 'praça',
            'al': 'alameda', 'al.': 'alameda',
            'dr': 'doutor', 'dr.': 'doutor',
            'dra': 'doutora', 'dra.': 'doutora',
            'prof': 'professor', 'prof.': 'professor',
            'sjc': 'são josé dos campos', 'sp': 'são paulo'
        }

        # Limpa pontuações grudadas nas palavras para não atrapalhar a busca
        busca_limpa = re.sub(r'([a-zA-Z]+)\.', r'\1. ', busca)
        palavras = busca_limpa.split()

        # Faz a substituição inteligente palavra por palavra
        for i, palavra in enumerate(palavras):
            palavra_limpa = palavra.replace('.', '')
            if palavra_limpa in substituicoes:
                palavras[i] = substituicoes[palavra_limpa]
            elif palavra in substituicoes:
                palavras[i] = substituicoes[palavra]

        busca_tratada = " ".join(palavras)
        print(f"[Abreviações] Texto original: '{busca}' -> Tratado: '{busca_tratada}'")

    # 2. CONSULTA AO OPENSTREETMAP
    url_osm = "https://nominatim.openstreetmap.org/search"
    busca_segura = quote(busca_tratada)
    url_final = f"{url_osm}?q={busca_segura}&format=json&limit=1&countrycodes=br&addressdetails=1"

    headers = {
        'User-Agent': 'AplicativoBotVacinaEstudantilFATEC_SJC_v6.0_Contato_Projeto(fatecsjc.edu.br)',
        'Accept': 'application/json',
        'Accept-Language': 'pt-BR,pt;q=0.9'
    }

    try:
        response = requests.get(url_final, headers=headers, timeout=15)

        if response.status_code == 403:
            url_reserva = f"https://nominatim.openstreetmap.fr/search?q={busca_segura}&format=json&limit=1&countrycodes=br&addressdetails=1"
            response = requests.get(url_reserva, headers=headers, timeout=15)

        if response.status_code != 200:
            return None, None, None

        data = response.json()

        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])

            address = data[0].get('address', {})
            rua_encontrada = address.get('road', address.get('pedestrian', ''))
            cidade_encontrada = address.get('city', address.get('town', address.get('suburb', '')))

            if rua_encontrada and cidade_encontrada:
                nome_formatado = f"{rua_encontrada}, {cidade_encontrada}"
            else:
                nome_formatado = data[0]['display_name'].split(',')[0]

            return lat, lon, nome_formatado

        return None, None, None

    except Exception as e:
        print(f"[OSM] Erro na geocodificação final: {e}")
        return None, None, None