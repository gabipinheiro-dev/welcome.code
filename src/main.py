import os               # Para acessar variáveis de ambiente (como o token)
import time             # Para pausas e controle de tempo
import threading        # Para executar tarefas pesadas sem travar o bot

import telebot          # Biblioteca principal do bot
from dotenv import load_dotenv   # Para ler o arquivo .env

# Arquivo com funções do formulário de perguntas/respostas
from formulario import (
    iniciar_conversa,
    processar_resposta,
    processar_gestante,
    processar_tipo_pessoa,
    processar_bebe,
    obter_usuario,
    remover_usuario
)

# Arquivos que fazem scraping (buscam informações online)
import scraping.scraper_pdf as scraper_pdf
import scraping.scraper_vacinas as scraper_vacinas


# Lê o token do arquivo .env (é onde você coloca seu token secreto)
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Verifica se o token existe. Se não existir, dá um aviso e fecha o programa.
if not TOKEN or not TOKEN.strip():
    print("❌ TELEGRAM_TOKEN não encontrado no arquivo .env")
    print("💡 Crie o arquivo .env com: TELEGRAM_TOKEN=seu_token_aqui")
    exit(1)

# Cria o objeto do bot com o token lido
# threaded=True permite atender várias pessoas ao mesmo tempo
bot = telebot.TeleBot(TOKEN.strip(), threaded=True, num_threads=10)

# Remove qualquer webhook antigo para garantir que estamos usando polling
bot.remove_webhook()

# Lista de palavras que reiniciam a conversa
saudacoes = ['oi', 'olá', 'ola', 'eae', 'opa', 'bom dia', 'boa tarde', 'boa noite','blz', 'fala', 'opa']


# Função segura para responder ao clique nos botões inline
def responder_callback_seguro(call):
    # Confirma pro Telegram que o clique foi recebido (tira o ícone de carregando)
    # Usamos try/except para evitar erros caso o botão tenha expirado
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass


# ---- Comandos de texto ----

# Quando alguém digita /start, inicia a conversa
@bot.message_handler(commands=['start'])
def start(msg):
    iniciar_conversa(bot, msg.chat.id)


# Quando alguém digita /reiniciar, limpa a sessão e começa de novo
@bot.message_handler(commands=['reiniciar'])
def reiniciar(msg):
    remover_usuario(msg.chat.id)
    iniciar_conversa(bot, msg.chat.id)


# Função que trata mensagens normais (não são comandos)
@bot.message_handler(func=lambda msg: True)
def responder(msg):
    # Ignora se a mensagem não tem texto
    if not msg.text:
        return

    texto = msg.text.lower().strip()

    # Se for alguma saudação, reinicia a conversa
    if any(s in texto for s in saudacoes):
        iniciar_conversa(bot, msg.chat.id)
        return

    # Caso contrário, continua a conversa normalmente
    processar_resposta(bot, msg)


# ---- Handlers dos botões ----

# Botão "Saiba Mais"
@bot.callback_query_handler(func=lambda call: call.data == "saiba_mais")
def saiba_mais_callback(call):
    responder_callback_seguro(call)

    texto = (
        "🤖 *Sobre o HealthyBot*\n\n"
        "Consulta realizada através do site oficial do *Ministério da Saúde*:\n"
        "https://www.gov.br/saude/pt-br/vacinacao\n\n"
        "✅ *Informação oficial na palma da sua mão!*\n"
        "• Consulta por faixa etária\n"
        "• Orientações para gestantes\n"
        "• Exibição de calendários oficiais\n\n"
        "Pode digitar seu nome para continuarmos! 👇"
    )

    try:
        bot.send_message(call.message.chat.id, texto, parse_mode='Markdown', disable_web_page_preview=True)
    except Exception:
        bot.send_message(call.message.chat.id, texto)


# Botões "Para mim" ou "Outra pessoa"
@bot.callback_query_handler(func=lambda call: call.data in ["user", "outra_pessoa"])
def tipo_pessoa_callback(call):
    responder_callback_seguro(call)
    processar_tipo_pessoa(bot, call)


# Botões relacionados a bebês
@bot.callback_query_handler(func=lambda call: call.data.startswith(("bebe", "nao_bebe")))
def bebe_callback(call):
    responder_callback_seguro(call)
    processar_bebe(bot, call)


# Botões relacionados a gestantes
@bot.callback_query_handler(func=lambda call: call.data.startswith(("gestante", "nao_gestante")))
def gestante_callback(call):
    responder_callback_seguro(call)
    processar_gestante(bot, call)


# Botão "Ver Calendário Oficial"
@bot.callback_query_handler(func=lambda call: call.data == "mais_info")
def mais_info_callback(call):
    responder_callback_seguro(call)

    user_id = call.message.chat.id
    usuario = obter_usuario(user_id)

    # Verifica se ainda há dados do usuário
    if not usuario:
        bot.send_message(user_id, "⚠️ Sua sessão expirou.\n\nDigite 'Oi' para iniciar.")
        return

    faixa = usuario.get('faixa')
    if not faixa:
        bot.send_message(user_id, "⚠️ Não identifiquei sua faixa etária.\n\nDigite 'Oi' para reiniciar.")
        return

    # Mensagem de espera enquanto baixa o PDF
    msg_espera = bot.send_message(
        user_id,
        "⏳ Gerando as imagens do calendário oficial...\nAguarde, isso pode levar até 30 segundos."
    )

    # Função interna para fazer o trabalho pesado sem travar o bot
    def _processar():
        try:
            # Baixa o PDF e envia como fotos
            scraper_pdf.enviar_paginas_como_foto(bot, user_id, faixa)

            # Apaga a mensagem de espera
            try:
                bot.delete_message(user_id, msg_espera.message_id)
            except Exception:
                pass

            bot.send_message(user_id, "✅ Espero ter ajudado! 😊\n\nSe precisar, envie um 'Oi' 💙")
            remover_usuario(user_id)

        except Exception as erro:
            print(f"❌ Erro ao enviar PDF para o usuário {user_id}: {erro}")

            try:
                bot.delete_message(user_id, msg_espera.message_id)
            except Exception:
                pass

            bot.send_message(user_id, "❌ Problema ao gerar o calendário.\n\nDigite 'Oi' para recomeçar.")

    # Executa essa função em segundo plano (sem travar outras pessoas)
    threading.Thread(target=_processar, daemon=True).start()


# ---- Inicialização do Bot ----

if __name__ == "__main__":
    # Antes de começar a escutar mensagens, carrega os dados do site para agilizar
    try:
        scraper_vacinas.busca_vacinas()
        print("🟢 Cache carregado com sucesso!")
    except Exception as erro:
        print(f"🟡 Aviso: não foi possível pré-carregar o cache: {erro}")

    print("🚀 Bot online!")

    # Loop infinito para manter o bot ligado sempre escutando novas mensagens
    while True:
        try:
            # Começa a escutar mensagens continuamente
            bot.polling(none_stop=True, skip_pending=True, interval=0, timeout=60)#timeou é o temo que leva para verificar novamente até reinicar outro ciclo
        except KeyboardInterrupt:# Aqui se der CTRL+C ele para, da um kill no programa
            print("\n👋 Bot encerrado manualmente.")
            break
        except telebot.apihelper.ApiTelegramException as erro:
            # Erro 409 acontece quando duas instâncias estão rodando por exxemplo. Erro que vem diretamento do próprio Telegram
            if getattr(erro, "error_code", None) == 409:
                print("⚠️ Erro 409: outra instância do bot está rodando. Reconectando em 15s...")
                bot.stop_polling()
                time.sleep(15)
            else:
                print(f"📡 Erro do Telegram: {erro}")
                time.sleep(5)
        except Exception as erro:
            print(f"💥 Erro inesperado: {erro}")
            time.sleep(5)