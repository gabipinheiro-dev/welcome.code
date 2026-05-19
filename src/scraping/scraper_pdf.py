import fitz        # Biblioteca PyMuPDF para manipular PDFs
import requests    # Para baixar o PDF da internet
import io          # Para tratar o PDF em memória (sem salvar no disco)

# Cache para não baixar o mesmo PDF várias vezes na mesma sessão
_pdf_cache = {}

# Links diretos para os arquivos PDF no site do Ministério da Saúde
LINKS_PDF = {
    'gestante':    'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-gestante',
    'crianca':     'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-crianca',
    'adolescente': 'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adolescentes-jovens',
    'adulto':      'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-adulto',
    'idoso':       'https://www.gov.br/saude/pt-br/vacinacao/arquivos/calendario-nacional-de-vacinacao-idoso'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def _baixar_pdf(perfil):
    #Baixa o PDF do perfil solicitado ou recupera do cache interno.
    if perfil in _pdf_cache:
        return _pdf_cache[perfil]

    url = LINKS_PDF.get(perfil)
    if not url:
        return None

    print(f"📥 Baixando PDF oficial: {perfil}...")
    resposta = requests.get(url, timeout=30, headers=HEADERS, allow_redirects=True)

    if resposta.status_code != 200:
        raise Exception(f"Erro ao baixar PDF: Status {resposta.status_code}")

    conteudo = resposta.content
    
    # Validação simples para garantir que  é realmente um PDF
    if not conteudo.startswith(b'%PDF'):
        raise Exception("O link não retornou um arquivo PDF válido.")

    _pdf_cache[perfil] = conteudo
    return conteudo

def enviar_paginas_como_foto(bot, chat_id, perfil):
    #Lê o PDF, transforma cada página em imagem e envia para o chat.
    url_reserva = LINKS_PDF.get(perfil, "https://www.gov.br/saude/pt-br/vacinacao")
    
    try:
        pdf_bytes = _baixar_pdf(perfil)
        if not pdf_bytes:
            bot.send_message(chat_id, "⚠️ O link deste calendário não foi encontrado.")
            return

        # Abre o PDF diretamente da memória (BytesIO)
        doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
        total_pg = len(doc)

        for num in range(total_pg):
            try:
                pagina = doc.load_page(num)
                
                # 'Matrix(2, 2)' dobra a resolução da imagem para que os textos fiquem legíveis
                pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))
                
                # Converte para formato JPEG reconhecido pelo Telegram
                img_data = io.BytesIO(pix.tobytes("jpeg"))
                img_data.name = f"calendario_{perfil}_p{num+1}.jpg"

                bot.send_photo(
                    chat_id, 
                    img_data, 
                    caption=f"📄 Calendário {perfil.capitalize()} - Pág. {num+1}/{total_pg}"
                )
            except Exception as e_pg:
                print(f"Erro na página {num+1}: {e_pg}")

        doc.close()

    except Exception as e:
        print(f"Erro ao processar PDF ({perfil}): {e}")
        # Caso o download ou processamento falhe, envia o link direto como alternativa
        texto_erro = (
            "❌ Não consegui gerar as imagens do calendário agora.\n\n"
            f"🔗 Mas você pode acessar o arquivo oficial aqui:\n{url_reserva}"
        )
        bot.send_message(chat_id, texto_erro, disable_web_page_preview=False)