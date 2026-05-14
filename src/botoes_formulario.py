from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


# Função que cria um botão "Saiba Mais" na tela inicial
def saiba_mais():
    # Criamos um novo teclado inline
    teclado = InlineKeyboardMarkup()
    
    # Adicionado botão com texto "ℹ️ Saiba Mais"
    # Quando clicado, manda "saiba_mais" como resposta ao programa principal
    teclado.add(InlineKeyboardButton("ℹ️ Saiba Mais", callback_data="saiba_mais"))
    
    # Devolvemos o teclado pronto
    return teclado


# Função que pergunta se a vacinação é para o próprio usuário ou outra pessoa
def tipo_pessoa():
    # Novo teclado vazio
    teclado = InlineKeyboardMarkup()
    
    # Adicionamos dois botões lado a lado:
    # - Um diz "Para mim", que envia "user"
    # - Outro diz "Outra pessoa", que envia "outra_pessoa"
    teclado.row(
        InlineKeyboardButton("👤 Para mim", callback_data="user"),
        InlineKeyboardButton("👥 Outra pessoa", callback_data="outra_pessoa")
    )
    
    return teclado


# Função que pergunta se o usuário é gestante
def gestante():
    # Só aparece se a pessoa for adulta
    teclado = InlineKeyboardMarkup()
    
    # Dois botões:
    # - "Sim, gestante" envia "gestante"
    # - "Não" envia "nao_gestante"
    teclado.row(
        InlineKeyboardButton("🤰 Sim, gestante", callback_data="gestante"),
        InlineKeyboardButton("❌ Não", callback_data="nao_gestante")
    )
    
    return teclado


# Função que pergunta se é um bebê (menos de 1 ano)
def bebe():
    # Se for bebê, vamos perguntar a idade em meses depois
    teclado = InlineKeyboardMarkup()
    
    # Opções:
    # - "Sim, bebê" envia "bebe"
    # - "Não" envia "nao_bebe"
    teclado.row(
        InlineKeyboardButton("👶 Sim, bebê", callback_data="bebe"),
        InlineKeyboardButton("🧒 Não", callback_data="nao_bebe")
    )
    
    return teclado


# Função que mostra o botão para ver o calendário oficial no final
def mais_informacoes():
    # Teclado novo
    teclado = InlineKeyboardMarkup()
    
    # Botão envia "mais_info"
    teclado.add(InlineKeyboardButton("📄 Ver Calendário Oficial", callback_data="mais_info"))
    
    return teclado