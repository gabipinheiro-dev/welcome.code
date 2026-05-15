from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Teclados inline usados pelo bot (mantive o nome botoes_formulario.py conforme sua árvore)

def saiba_mais():
    teclado = InlineKeyboardMarkup()
    teclado.add(InlineKeyboardButton("ℹ️ Saiba Mais", callback_data="saiba_mais"))
    return teclado


def tipo_pessoa():
    teclado = InlineKeyboardMarkup()
    teclado.row(
        InlineKeyboardButton("👤 Para mim", callback_data="user"),
        InlineKeyboardButton("👥 Outra pessoa", callback_data="outra_pessoa")
    )
    return teclado


def gestante():
    # Pergunta se a pessoa está gestante.
    
    teclado = InlineKeyboardMarkup()
    teclado.row(
        InlineKeyboardButton("🤰 Sim, gestante", callback_data="gestante"),
        InlineKeyboardButton("🚫 Não", callback_data="nao_se_aplica")
    )
    return teclado


def bebe():
    teclado = InlineKeyboardMarkup()
    teclado.row(
        InlineKeyboardButton("👶 Sim, bebê", callback_data="bebe"),
        InlineKeyboardButton("🧒 Não", callback_data="nao_bebe")
    )
    return teclado


def mais_informacoes():
    teclado = InlineKeyboardMarkup()
    teclado.add(InlineKeyboardButton("📄 Ver Calendário Oficial", callback_data="mais_info"))
    return teclado