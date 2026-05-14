# - 'fitz' é usada para abrir e manipular arquivos PDF.
# - 'requests' serve para fazer download de arquivos da internet.
# - 'io' ajuda a trabalhar com dados em memória, sem salvar no disco.

import fitz
import requests
import io

# Aqui criamos um temporário chamado '_pdf_cache'.
# Ele guarda os PDFs já baixados para não precisarmos baixar de novo.
_pdf_cache = {}

# Um dicionário (lista com nomes) que contém links dos calendários por perfil:
LINKS_PDF = {
    'gestante':    'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-gestante',
    'crianca':     'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-crianca',
    'adolescente': 'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adolescentes-jovens',
    'adulto':      'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adulto',
    'idoso':       'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-idoso'
}

# Configurações adicionais para simular um navegador ao acessar sites:
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


# Função para baixar o PDF de um determinado perfil (como criança, adulto etc.)
def _baixar_pdf(perfil):
    # Primeiro verifica se o PDF desse perfil já foi baixado antes
    if perfil in _pdf_cache:
        return _pdf_cache[perfil]  # Retorna o PDF salvo no armário

    # Pega o link do PDF correspondente ao perfil
    url = LINKS_PDF.get(perfil)
    if not url:
        return None  # Se não encontrar, retorna nada

    print(f"🌐 Baixando PDF do perfil '{perfil}'...")

    # Faz o pedido para baixar o arquivo da internet
    resposta = requests.get(url, timeout=30, headers=HEADERS, allow_redirects=True)

    # Verifica se funcionou (status 200 significa sucesso)
    if resposta.status_code != 200:
        raise Exception(f"❗ Erro HTTP {resposta.status_code} ao tentar baixar.")

    conteudo_do_pdf = resposta.content  # Conteúdo binário do PDF

    # Checa se realmente é um PDF (todo PDF começa com "%PDF")
    if len(conteudo_do_pdf) < 4 or conteudo_do_pdf[:4] != b'%PDF':
        raise Exception("❌ O conteúdo baixado não parece ser um PDF válido.")

    # Guarda o PDF no armário para uso futuro
    _pdf_cache[perfil] = conteudo_do_pdf
    print(f"💾 PDF '{perfil}' guardado no cache.")
    return conteudo_do_pdf


# Função que envia todas as páginas do PDF como imagens pelo Telegram
def enviar_paginas_como_foto(bot, chat_id, perfil):
    # Tenta pegar o link do PDF baseado no perfil solicitado
    url = LINKS_PDF.get(perfil)
    if not url:
        bot.send_message(chat_id, "⚠️ Calendário indisponível para este perfil.")
        return

    try:
        # Baixa o PDF usando a função anterior
        pdf_bytes = _baixar_pdf(perfil)

        # Abre o PDF diretamente da memória
        doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
        total_paginas = len(doc)  # Conta quantas páginas tem

        # Para cada página do PDF...
        for numero_da_pagina in range(total_paginas):
            try:
                # Carrega a página atual
                pagina = doc.load_page(numero_da_pagina)

                # Converte a página em imagem com qualidade maior (Matrix aumenta a resolução)
                imagem = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))

                # Transforma a imagem num formato que pode ser enviado
                img_io = io.BytesIO(imagem.tobytes("jpeg"))

                # Define um nome para a imagem
                img_io.name = f'calendario_{perfil}_pg{numero_da_pagina + 1}.jpg'

                # Envia a imagem pelo Telegram
                bot.send_photo(
                    chat_id,
                    img_io,
                    caption=f"📄 Calendário {perfil.capitalize()} - Página {numero_da_pagina + 1}/{total_paginas}"
                )
            except Exception as erro_na_pagina:
                print(f"Erro na página {numero_da_pagina + 1}: {erro_na_pagina}")
                bot.send_message(chat_id, f"⚠️ Problema na página {numero_da_pagina + 1}")

        doc.close()  # Fecha o documento após terminar

    except requests.exceptions.Timeout:
        bot.send_message(chat_id, "⏳ Tempo esgotado ao tentar acessar o site. Tente mais tarde.")

    except requests.exceptions.RequestException as erro_rede:
        print(f"Problema de conexão ({perfil}): {erro_rede}")
        bot.send_message(chat_id, "❌ Não consegui acessar o site do Ministério da Saúde.")

    except Exception as erro_geral:
        print(f"Falha geral ao processar o PDF ({perfil}): {erro_geral}")
        bot.send_message(chat_id, f"❌ Erro ao carregar o calendário.\n\n🔗 Veja aqui:\n{url}")