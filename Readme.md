<p align="center">
      <img src="https://github.com/turbodeliveryapi/welcome.code/blob/main/docs/img/Logo%20da%20Equipe" width="200">
      <h2 align="center"> Platypus Dev</h2>

# **API 1º Semestre ADS**

Olá! Esse é um projeto inicialiazado por alunos do 1º semestre do curso de Análise e Desenvolvimento de Sistemas, da Fatec de São José dos Campos. O objetivo desse projeto é construir um BOT no Telegram que responda à pergunta de diversos públicos a respeito de vacinas e saúde, baseado em dados do site oficial do Governo do Brasil. Esses são os primeiros comandos injetados no BOT para ações básicas e cruciais para a entrega da primeira SPRINT dessa API. Feito no Google Colab com ajuda do site 'pytelegrambotapi'.

## **Desafio**

O desafio do produto consiste em desenvolver um bot interativo que, ao ser acionado pelo usuário, apresente de forma clara diferentes opções de faixas etárias por meio de botões, ao selecionar uma dessas opções, o bot deve mandar arquivo em PDF contendo informações detalhadas sobre as vacinas recomendadas para a faixa etária escolhida, trazendo organização e fácil acesso ao conteúdo relevante para cada perfil de usuário.

---

## **Backlog do produto**

| Rank | Prioridade | User story | Estimativa | Sprint |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| 1 | Muito alto | Como um idoso, desejo me integrar mais sobre minhas vacinas  necessárias para melhorar minha qualidade de vida de acordo com minha idade | 20 | 1 |
| 2 | Alto | Como uma mãe, desejo saber quais vacinas meu recém nascido precisa tomar para o desenvolvimento de imunidade | 13 | 1 |
| 3 | Alto | Como um enfermeiro, desejo me integrar sobre as vacinas necessárias dos meus pacientes para ter mais conhecimento | 13 | 1 |
| 4 | Alto | Como um neto, desejo saber sobre as vacinas pendentes do meu avô para cuidar melhor dele | 13 | 1 |
| 5 | Muito alto | Como uma pessoa que se preocupa com a saúde, desejo me integrar mais sobre minhas vacinas pendentes e necessárias para melhorar minha qualidade de vida de acordo com minha idade | 20 | 2 |
| 6 | Baixo | Como um cidadão, desejo ter conhecimento sobre os postos de saúde de minha cidade | 13 | 3 |
| 7 | Muito alto | Como um homem muito alérgico à certas medicações , desejo ter conhecimento das vacinas própias para minha comorbidade e seus efeitos colaterais. | 20 | 3 |
| 8 | Baixo | Como uma pessoa com dificuldade de locomoção, desejo ter conhecimento das alternativas para vacinação em casa | 8 | 3 |


## DoR - Definition of Ready
* User Stories com critérios de aceitação
* Subtarefas divididas
* Entendimento claro da tarefa


## DoD - Definition of Done
* Código implementado
* Critérios de aceitação atendidos
* Testado manualmente
* Código organizado

## 

## **Cronograma das Sprints**

| Sprint | Período | MVP | Link para Documentação | Link para Vídeo no Youtube do Incremento Entregue |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| 1 | 16/03/2026 a 05/04/2026 | [Sprint 1](./mvp/sprint-01/README.md) | <h4 align="center"> <a href="https://apiequipequet.atlassian.net/jira/software/projects/EQ/summary?atlOrigin=eyJpIjoiMzYyMTdjMDkyYzQzNDg3ZWE0YzNhMTllMGI2ZDRhNDYiLCJwIjoiaiJ9"><img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white"/></a>  </h4> | <h4 align="center"> <a href="https://youtube.com/shorts/D4LPyznxHVM?si=k8T46wLOupl0c_CJ"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"/></a>  </h4> |
| 2 | 12/04/2026 a 03/05/2026 | [Sprint 2](./mvp/sprint-02/README.md) | <h4 align="center"> <a href="https://apiequipequet.atlassian.net/jira/software/projects/EQ/boards/67/backlog?atlOrigin=eyJpIjoiZmFlYmUxM2U0YTMxNDdmYWI0NmU3NmQ3ZjliNmQzODEiLCJwIjoiaiJ9"><img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white"/></a>  </h4>  | <h4 align="center"> <a href="https://youtube.com/shorts/jpJRoByxvrA?si=xk6s2tt8edtmkZUo"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white"/></a>  </h4> |
| 3 | - | - | - | - |

## **Tecnologias utilizadas**

<h4 align="center">
 <a href="https://colab.research.google.com/"><img src="https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white">
 <a href="https://www.atlassian.com/software/jira"><img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white"/></a>
 <a href="https://github.com/"><img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/></a>
 <a href="https://web.telegram.org/"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/></a>
 <a href="https://railway.com"><img src="https://img.shields.io/badge/Railway-131415?style=for-the-badge&logo=railway&logoColor=white"></a>
</h4>

---

## **Manual do usuário**

### **Pré-requisitos**
- Instalar o telegram
- Ter um número de telefone


### **Como usar o Bot**
- Iniciar o Bot com comando de /start
- Escolha a opção desejado através dos botões
- Escolha a faixa etária que desejar
- Bot estregará PDF com vacinas que a faixa etária deve tomar

---

## **Manual de Instalação**

### **Pré-requisitos**
- Git (<a href="https://git-scm.com/install/">Download</a>)
- Python 3.10+ (<a href="https://www.python.org/downloads/">Download</a>)
- Bot Telegram (<a href="https://desktop.telegram.org">Download</a>)

### **Ambientes**
Para rodar este projeto, pode-se escolher entre o ambiente de nuvem ou local:

**Para execução local:**
 - Conta no Google Colab (<a href="https://colab.research.google.com/">Site</a>)
 - Editor de código de sua preferência (VS Code por exemplo)
   
**Para execução em nuvem**
 - Conta no Railway (<a href="https://railway.com">Site</a>)

### **1. Criar um bot no Telegram**
- Já com sua conta no Telegram, procure por @BOtFather.
- Em sua conversa, mande o comando /newbot:
  ```bash
  /newbot
  ```
- Escolha um nome e username para seu bot.
- Guarde o API TOKEN. Essa chave que permite que o bot receba as instruções dos arquivos.
- Caso o TOKEN fique público, o bot pode sofrer alterações de qualquer pessoa.


### **2. Baixar os arquivos do branch deploy**
O branch deploy é a versão estável e otimizada para o funcionamento do bot.

Pode-se clonar apenas o branch deploy (melhor para Ambiente em Nuvem):
```bash
git clone -b deploy [https://github.com/turbodeliveryapi/welcome.code](https://github.com/turbodeliveryapi/welcome.code)
 Uma alternativa, é vc criar um fork apenas desse branch.
```
 Também pode-se fazer um fork apenas do branch deploy.
Ou baixar o ZIP contendo os arquivos (melhor para Ambiente Local):
```md
[Arquivo ZIP](https://github.com/turbodeliveryapi/welcome.code/archive/refs/heads/deploy.zip)
```
 Crie uma pasta para armazenar os arquivos.


### **3. Configuração do Ambiente**

#### **3.1. Ambiente Local**
Ideal para testes rápidos e desenvolvimento. O bot só funcionará enquanto o seu computador (ou a aba do navegador) estiver com o código rodando.

**Instruções**

##### **Google Colab**
- Acesse o Google Colab e crie um **Novo notebook**.
- Na primeira célula, digite e rode (apertar o ícone de Play) para intalar a biblioteca da linguagem Python.
  ```python
  !pip install python-telegram-bot
  ```
- Depois, cole os códigos dos arquivos em novas células.
- Para inserir o TOKEN  de forma segura, no menu lateral esquerdo, clique no ícone de Chave (Secrets).
 - Adicione um novo segredo com o nome TELEGRAM_TOKEN e cole o seu TOKEN do BotFather no valor.
 - Ative a opção "Notebook access"
 - Para rodar, clique novamente no Play. Caso necessário, aperte p Play de todas as células.
 - O bot ficara ativo enquanto a célula continuar rodando.

##### **Editor de Código**
Para fins de instrução, usaremos o VC Code como editor de código. Mas em caso de preferência de outro, siga os mesmos passos no editor de sua escolha.
- Abra a pasta do seu projeto no VS Code.
- Depois, crie um novo terminal. Pode-se usar o atalho **Ctrl+Shift+'**.
- No terminal, instale as bibliotecas python-telegram-bot e python-dotenv:
  ```bash
  pip install python-telegram-bot python-dotenv
  ```
- Após instalar as bibliotecas, crie um arquivo .env na mesma pasta e coloque o TOKEN:
  ```Plaintxt
  TELEGRAM_TOKEN=insira_seu_token
  ```
- Execute o **arquivo main.py**. Pelo Play ou pelo terminal:
  ```bash
  python main.py
  ```
- No fim do teminal, deve ser devolvido:
  ```
  🤖 Healthybot em operação!
  ```

#### **3.2. Ambiente em Nuvem**
O ambiente em nuvem permite que o bot sempre fique ativo independentemente de onde o código estiver hospedado. Sua limitação é que é necessário sempre subir no repositório as alterações feitas para que ele possa executar-las.

**Instruções**
- Para o ambiente em nuvem, deve-se clonar o branch deploy ou criar um repositório pessoal e fazer upload dos arquivos. Caso tenha optado pelo frok, isso não é preciso.
- Depois vincular seu Github com o Railway
- Para executar o código, precisa-se criar um projeto e vinculado com o repositório onde está os arquivos do bot
   - Certifique-se que o repositório é seu, caso contrário, ele não aparecerá na lista de repositórios para criar o projeto
- Após terminar de criar o projeto, clique nele para abrir o Menu e entre na aba Variáveis
- Nela, clique em Add+ e dê o nome **TELEGRAM_TOKEN** e insira em seu valor o TOKEN do seu bot
- Por fim, faça o Deploy do projeto
- Para se certificar que o bot já está funcionando, na projeto depe aparecer **Online**

### **4. Iniciando o bot**
- Para iniciar o bot, basta manda no campo de mensagem  o comando /start:
  ```bash
  /start
  ```
- O bot deve responder as interações seguintes.
  
---

## **Equipe**

<div align="center">
  <table>
    <tr>
      <th>Membro</th>
      <th>Função</th>
      <th>Github</th>
      <th>Linkedin</th>
    </tr>
    <tr>
      <td>Quétsia</td>
      <td>Product Owner</td>
      <td><a href="https://github.com/quetsiaksilva"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/quétsia-silva-b0906327a?utm_source=share_via&utm_content=profile&utm_medium=member_android"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Eloá</td>
      <td>Scrum Master</td>
      <td><a href="https://github.com/eloagaldino"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/elo%C3%A1-galdino-samaniego-487b1a376/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>João Vitor</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/joaonataliogit?tab=overview&from=2026-03-01&to=2026-03-31"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/jo%C3%A3o-natalio-89a36728b/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Gabrielle</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/gabipinheiro-dev"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/gabrielle-pinheiro-09b4943b2?utm_source=share_via&utm_content=profile&utm_medium=member_ios"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>José Carlos Sousa</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/JcSousaa"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/jcqsousa/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Marcos</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/marcosgalvaov"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/marcos-guilherme-galvao/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Ana Paula Ramos</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/anapaularamos26"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/ana-paula-ramos-de-sousa-241699307/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    <tr>
      <td>Isabele</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/Codin058"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/isabele-camargo-portela-20385a3bb?utm_source=share_via&utm_content=profile&utm_medium=member_android"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Julia Castro</td>
      <td>Desenvolvedor</td>
      <td><a href="https://github.com/Julia-Castro-ADS"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/julia-castro-97a8a93a0/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
  </table>
</div>
