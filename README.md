Bot de Consulta de Faturamento para Telegram
📄 Descrição
Este é um bot para Telegram desenvolvido em Python que serve como uma interface inteligente para consultar dados de faturamento diário a partir de uma planilha Excel. O bot foi projetado para entender tanto datas específicas quanto consultas em linguagem natural para feriados e períodos (meses), tornando a obtenção de dados rápida e intuitiva.

O projeto é um exemplo completo de um ciclo de desenvolvimento, desde a leitura e processamento de dados com pandas, passando pela criação de um bot interativo com python-telegram-bot, até o gerenciamento seguro de chaves de API com variáveis de ambiente.

✨ Funcionalidades
Consulta por Data Específica: Retorna os dados de faturamento ao receber uma data no formato DD/MM/AAAA.

Consulta por Feriados: Entende nomes de feriados nacionais brasileiros (ex: "natal 2023", "tiradentes 2024") e calcula a data correta para a busca.

Consulta por Mês/Ano: Entende solicitações como "fevereiro 2024" e retorna os dados agregados para o mês inteiro.

Consulta por Período Explícito: Processa requisições como "de 01/01/2024 a 15/01/2024".

Processamento de Linguagem Natural: Utiliza um sistema de mapeamento de palavras-chave e normalização de texto para entender as solicitações de forma flexível.

Gerenciamento Seguro de Segredos: Utiliza o padrão da indústria de variáveis de ambiente (.env para desenvolvimento local) para o token da API, garantindo que informações sensíveis não sejam expostas no código-fonte.

📂 Estrutura do Projeto
A estrutura de arquivos do projeto está organizada da seguinte forma:

bot_faturamento_python/
│
├── venv/                   # Pasta do ambiente virtual isolado do Python
├── .env                    # Arquivo de configuração local (NÃO É ENVIADO AO GIT)
├── .gitignore              # Arquivo que define o que o Git deve ignorar
├── Faturamento.xlsx        # Planilha com os dados de faturamento (Exemplo de nome)
├── bot.py                  # O código-fonte principal da aplicação
└── requirements.txt        # Lista de todas as dependências do projeto

🛠️ Tecnologias Utilizadas
Linguagem: Python 3

Bibliotecas Principais:

python-telegram-bot: Framework para interagir com a API do Telegram.

pandas: Para leitura, manipulação e análise dos dados da planilha Excel.

openpyxl & xlrd: Motores utilizados pelo pandas para ler diferentes formatos de arquivos Excel.

holidays: Para calcular com precisão as datas de feriados nacionais brasileiros.

python-dotenv: Para carregar variáveis de ambiente de um arquivo .env localmente.

🚀 Instalação e Configuração
Siga estes passos para configurar e executar o projeto localmente.

1. Pré-requisitos
Python (versão 3.9 ou superior)

Git (opcional, para controle de versão)

2. Passos de Instalação
Clone ou baixe os arquivos para uma pasta local. Abra um terminal nessa pasta e siga os comandos:

# Criar o ambiente virtual (só precisa ser feito uma vez)
python -m venv venv

# Ativar o ambiente virtual (precisa ser feito toda vez que for trabalhar no projeto)
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Instalar todas as dependências necessárias
pip install -r requirements.txt

3. Arquivos de Configuração
Planilha de Dados:

Coloque seu arquivo Excel na pasta raiz do projeto.

Abra o arquivo bot.py e ajuste a variável NOME_ARQUIVO_EXCEL para corresponder exatamente ao nome do seu arquivo.

Verifique também se o nome na variável NOME_COLUNA_DATA corresponde ao cabeçalho da coluna de datas na sua planilha.

Token do Bot:

Crie um arquivo chamado .env na pasta raiz do projeto.

Dentro deste arquivo, adicione a seguinte linha, substituindo pelo seu token real obtido com o @BotFather:

TELEGRAM_TOKEN="SEU_TOKEN_AQUI"

O arquivo .gitignore já está configurado para impedir que este arquivo .env seja enviado para o GitHub.

▶️ Executando o Bot
Com o ambiente virtual ativo ((venv)) e os arquivos configurados, inicie o bot com o seguinte comando no terminal:

python bot.py

Você verá a mensagem >>> Bot inteligente iniciado com sucesso! <<<. Para parar o bot, pressione Ctrl+C.

🤖 Como Usar o Bot
Abra uma conversa com seu bot no Telegram e envie uma mensagem.

Exemplos de Comandos:

31/12/2024

natal 2023

proclamação da república 2024

semana do carnaval 2023

fevereiro de 2024

de 01/05/2024 a 10/05/2024

📐 Arquitetura do Código
O script bot.py é dividido em seções lógicas:

Configurações Globais: Define constantes como nomes de arquivos, colunas e os dicionários MAPEAMENTO_EVENTOS e MAPEAMENTO_MESES, que "traduzem" as solicitações do usuário.

Funções de Manipulação de Dados:

carregar_dados(): Lê o arquivo Excel, limpa os dados (converte colunas de moeda e números para o formato correto) e armazena em memória para acesso rápido.

buscar_faturamento_por_data() e buscar_faturamento_por_periodo(): Funções otimizadas para consultar os dados em memória a partir de uma data ou intervalo.

processar_evento_texto(): O cérebro da interpretação de linguagem natural. Ele testa a mensagem do usuário contra múltiplos padrões (período explícito, mês/ano, feriados) para determinar a intenção.

Lógica do Bot (Handlers):

start(): Responde ao comando /start.

message_handler(): O handler principal que recebe o texto do usuário. Ele primeiro tenta interpretar a mensagem como uma data DD/MM/AAAA. Se falhar, chama a processar_evento_texto() para uma análise mais profunda.

main(): A função principal que inicializa o bot e começa a "escutar" por mensagens.

❓ Troubleshooting / Problemas Comuns
FileNotFoundError: Verifique se o nome do arquivo Excel na variável NOME_ARQUIVO_EXCEL no código é exatamente igual ao nome do arquivo na pasta.

Bot não inicia ou dá erro de Token: Verifique se o arquivo .env existe e se o token dentro dele está correto e válido.

Comandos não funcionam: Certifique-se de que o ambiente virtual (venv) está ativo no terminal onde você executou o bot.

📄 Licença
Este projeto está sob a licença MIT.