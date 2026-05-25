import threading                   # Para rodar tarefas pesadas sem travar o bot
import botoes_formulario           # Arquivo com os botões que aparecem no Telegram
import scraping.scraper_vacinas as vacinas_scraper  # Busca informações das vacinas no site

# Um "armário" para guardar os dados de cada usuário enquanto ele usa o bot
usuarios = {}


# Função que descobre a faixa etária com base na idade
def determinar_faixa_etaria(idade):
    if idade < 10:
        return 'crianca'         # Menos de 10 anos → criança
    elif idade < 20:
        return 'adolescente'     # De 10 a 19 anos → adolescente
    elif idade < 60:
        return 'adulto'          # De 20 a 59 anos → adulto
    else:
        return 'idoso'           # 60 anos ou mais → idoso


# Função que diz qual fase do calendário uma criança tem com base nos meses
def fase_por_meses(meses):
    # Mapa com as idades específicas em meses e suas fases
    MAPA_MESES = {
        0: 'Ao nascer',
        2: '2 meses',
        3: '3 meses',
        4: '4 meses',
        5: '5 meses',
        6: '6 meses',
        9: '9 meses',
        12: '12 meses',
        15: '15 meses',
        24: '24 meses'
    }

    # Se tem entre 6 e 8 meses, a fase é "6 a 8 meses"
    if 6 < meses <= 8:
        return '6 a 8 meses'

    # Senão, pega a fase direto do mapa
    return MAPA_MESES.get(meses)


# Função que retorna a fase do calendário para idades maiores (anos)
def fase_por_idade(idade):
    if idade <= 4:
        return '4 anos'
    elif idade <= 14:
        return '9 a 14 anos'
    elif idade <= 24:
        return '10 a 24 anos'
    elif idade <= 59:
        return '25 a 59 anos'
    else:
        return 'A partir dos 60 anos'  # Corrigido: "dos" não "de"


# Função para atualizar os dados de um usuário no armário
def atualizar_usuario(user_id, dados):
    # Se o usuário ainda não existe no armário, cria um espaço pra ele
    if user_id not in usuarios:
        usuarios[user_id] = {}
    # Atualiza os dados dele com as novas informações
    usuarios[user_id].update(dados)


# Função para pegar os dados de um usuário
def obter_usuario(user_id):
    return usuarios.get(user_id, {})  # Retorna os dados ou um dicionário vazio se não existir


# Função para remover os dados de um usuário do armário (quando termina a conversa)
def remover_usuario(user_id):
    if user_id in usuarios:
        del usuarios[user_id]


# Função que começa a conversa com o usuário
def iniciar_conversa(bot, user_id):
    # Registra que o usuário está na etapa de informar o nome
    atualizar_usuario(user_id, {'etapa': 'nome'})

    # Mensagem de boas-vindas com botão "Saiba Mais"
    texto = (
        '✨ 🤖 *Bem-vindo ao HealthyBot!* ✨\n\n'
        "👋 Oi! Eu sou o *HealthyBot* 😊\n\n"
        "Vou te ajudar a encontrar seu Calendário de Vacinação 💉\n\n"
        "Para começar, qual é o seu nome?\n\n"
    )

    # Envia a mensagem com estilo Markdown e o botão "Saiba Mais"
    bot.send_message(user_id, texto, parse_mode='Markdown', reply_markup=botoes_formulario.menu_inicial())


# Função que trata respostas escritas pelo usuário
def processar_resposta(bot, msg):
    # Pega o ID do usuário e o texto digitado
    user_id = msg.chat.id
    texto = msg.text.strip()
    # Pega os dados salvos desse usuário
    u = obter_usuario(user_id)

    # Se não tem dados, pede pra reiniciar
    if not u:
        bot.send_message(user_id, "👋 Digite 'Oi' para iniciar uma consulta.")
        return

    # Verifica em qual etapa da conversa o usuário está
    etapa = u.get('etapa')

    # Etapa: pediu o nome
    if etapa == 'nome':
        atualizar_usuario(user_id, {'nome': texto.title(), 'etapa': 'tipo_pessoa'})
        bot.send_message(
            user_id,
            f"📌 Legal {texto.title()}, para quem é a consulta?",
            reply_markup=botoes_formulario.tipo_pessoa()
        )

    # Etapa: perguntou se é pra si ou outra pessoa
    elif etapa == 'tipo_pessoa':
        bot.send_message(user_id, "👆 Use os botões para responder.", reply_markup=botoes_formulario.tipo_pessoa())

    # Etapa: perguntou se é bebê
    elif etapa == 'bebe_check':
        bot.send_message(user_id, "👆 Use os botões para responder.", reply_markup=botoes_formulario.bebe())

    # Etapa: perguntou se é gestante
    elif etapa == 'gestante':
        bot.send_message(user_id, "👆 Use os botões para responder.", reply_markup=botoes_formulario.gestante())

    # Etapa: pediu a idade em anos
    elif etapa == 'idade':
        # Verifica se o texto é número
        if not texto.isdigit():
            bot.send_message(user_id, "❗ Por favor, digite apenas números.")
            return

        idade = int(texto)

        # Verifica se a idade é válida
        if idade < 0 or idade > 150:
            bot.send_message(user_id, "❗ Digite uma idade válida (0 a 150 anos).")
            return

        # Bebês até 2 anos
        if idade <= 2:
            meses = 0 if idade == 0 else (12 if idade == 1 else 24)
            atualizar_usuario(user_id, {'meses': meses})
            _enviar_em_thread(bot, user_id, 'bebe')
        else:
            # Guarda a idade do usuário
            atualizar_usuario(user_id, {'idade': idade})

            # Se a pessoa tem 12 anos ou mais, perguntamos sobre gestação
            # (isso inclui adolescentes a partir de 12 anos)
            if idade >= 12:
                # Marca a etapa como gestante para que o clique no botão seja tratado
                atualizar_usuario(user_id, {'etapa': 'gestante'})
                bot.send_message(user_id, "📌 A pessoa está gestante ou planejando gestação?",
                    reply_markup=botoes_formulario.gestante())
            else:
                # Menos de 12 anos (mas > 2): segue fluxo normal por faixa
                faixa = determinar_faixa_etaria(idade)
                _enviar_em_thread(bot, user_id, faixa)

    # Etapa: pediu a idade em meses (para bebês)
    elif etapa == 'idade_meses':
        # Verifica se o texto é número
        if not texto.isdigit():
            bot.send_message(user_id, "❗ Por favor, digite apenas números.")
            return

        meses = int(texto)

        # Verifica se está dentro do limite
        if meses < 0 or meses > 24:
            bot.send_message(user_id,
                    "❗ Digite uma idade entre 0 e 24 meses.\n"
                    "Para crianças acima de 2 anos, digite 'Oi' e reinicie informando a idade em anos.")
            return

        atualizar_usuario(user_id, {'meses': meses})
        _enviar_em_thread(bot, user_id, 'bebe')


# Função que trata cliques nos botões de "Para mim" ou "Outra pessoa"
def processar_tipo_pessoa(bot, call):
    uid = call.message.chat.id
    if call.data == "user":
        atualizar_usuario(uid, {'etapa': 'idade'})
        bot.send_message(uid, "Certo! Me diga a sua idade (em anos):")
    else:
        atualizar_usuario(uid, {'etapa': 'bebe_check'})
        bot.send_message(uid, "👶 É um bebê (até 2 anos)?", reply_markup=botoes_formulario.bebe())


# Função que trata cliques nos botões de "Bebe/Não Bebê"
def processar_bebe(bot, call):
    uid = call.message.chat.id
    if call.data == "bebe":
        atualizar_usuario(uid, {'etapa': 'idade_meses'})
        bot.send_message(uid, "Quantos meses o bebê tem? (0 a 24 meses)")
    else:
        atualizar_usuario(uid, {'etapa': 'idade'})
        bot.send_message(uid, "Qual a idade da pessoa (em anos)?")


# Função que trata cliques nos botões de "Gestante/Não Gestante"
def processar_gestante(bot, call):
    user_id = call.message.chat.id

    # Se a pessoa respondeu que É gestante, usamos a faixa "gestante"
    if call.data == "gestante":
        faixa = "gestante"
    else:
        # Se respondeu "não", tentamos recuperar a idade já salva
        u = obter_usuario(user_id)
        idade = u.get('idade')

        if idade is not None:
            # Converte a idade em faixa correta (ex: 12-19 -> 'adolescente')
            faixa = determinar_faixa_etaria(idade)
        else:
            # Fallback conservador caso não haja a idade salva
            faixa = "adulto"

    _enviar_em_thread(bot, user_id, faixa)


# Função auxiliar para rodar uma tarefa pesada (como buscar vacinas) sem travar o bot
def _enviar_em_thread(bot, user_id, faixa):
    t = threading.Thread(target=_enviar_vacinas_em_background, args=(bot, user_id, faixa), daemon=True)
    t.start()


# Função que formata uma vacina bonitinho para exibir
def _formatar_vacina(vacina, dose, previne):
    linhas = [f"💉 *{vacina}*"]
    if dose:
        linhas.append(f"📋 Dose: {dose}")
    if previne:
        linhas.append(f"🛡️ Previne: {previne}")
    return '\n'.join(linhas)


# Função principal que busca e envia as vacinas recomendadas
def _enviar_vacinas_em_background(bot, user_id, faixa):
    try:
        u = obter_usuario(user_id)
        nome = u.get('nome', 'Usuário')

        # Avisa que está buscando
        bot.send_message(user_id, f"Perfeito, {nome}! 👍\n\n⏳ Buscando vacinas recomendadas...")

        # Define a faixa correta
        faixa_final = 'crianca' if faixa == 'bebe' else faixa
        atualizar_usuario(user_id, {'faixa': faixa_final})

        # Para gestantes
        if faixa == "gestante":
            fases = [
                "Ao saber da gravidez",
                "A partir da 20ª semana gestacional",
                "A partir da 28ª semana gestacional"
            ]
        elif faixa == "bebe":
            # Para bebês, define a fase com base nos meses
            meses = u.get('meses', 0)
            fase = fase_por_meses(meses)

            # Se não achou a fase exata, sugere uma próxima
            if not fase:
                fases_proximas = {
                    1: '2 meses', 7: '6 meses', 8: '9 meses',
                    10: '9 meses', 11: '12 meses', 13: '12 meses',
                    14: '15 meses', 16: '15 meses', 17: '15 meses',
                    18: '15 meses', 19: '15 meses', 20: '15 meses',
                    21: '24 meses', 22: '24 meses', 23: '24 meses'
                }
                fase = fases_proximas.get(meses)
                if fase:
                    bot.send_message(user_id,
                    f"ℹ️ Mostrando vacinas para a fase mais próxima: *{fase}*",
                    parse_mode='Markdown')
            fases = [fase] if fase else []
        else:
            # Para adultos, adolescentes, idosos...
            idade = u.get('idade', 0)
            fase = fase_por_idade(idade)
            fases = [fase] if fase else []

        # Se não encontrou fase válida, pede o calendário completo
        if not fases or not fases[0]:
            bot.send_message(user_id,
                    "⚠️ Não consegui determinar a fase no calendário oficial.\n\n"
                    "💡 Acesse o calendário completo:",
                    reply_markup=botoes_formulario.mais_informacoes())
            return

        # Monta a lista de vacinas
        linhas = []
        for fase_busca in fases:
            if not fase_busca:
                continue
            vacinas = vacinas_scraper.buscar_fase(faixa_final, fase_busca)
            for v in vacinas:
                vacina = v.get('vacina', '')
                dose = v.get('dose', '')
                previne = v.get('evita', '')
                if vacina:
                    linhas.append(_formatar_vacina(vacina, dose, previne))

        # Se achou vacinas, envia elas
        if linhas:
            texto_vacinas = "\n\n".join(linhas)
            mensagem = (
                f"💉 *Vacinas recomendadas:*\n\n{texto_vacinas}\n\n"
                "💡 *Deseja o Calendário Oficial completo?*"
            )
            bot.send_message(user_id, mensagem, parse_mode='Markdown',
                    reply_markup=botoes_formulario.mais_informacoes())
        else:
            # Se não achou, oferece o calendário oficial
            bot.send_message(user_id,
                    "⚠️ Não encontrei vacinas específicas para esta fase.\n\n"
                    "📄 Consulte o calendário oficial completo:",
                    reply_markup=botoes_formulario.mais_informacoes())

    except Exception as e:
        # Em caso de erro, avisa o usuário
        print(f"Erro ao buscar vacinas para o usuário {user_id}: {e}")
        bot.send_message(user_id, "😓 Ops! Algo deu errado.\n\nDigite 'Oi' para recomeçar.")