import os
import pandas as pd
from datetime import datetime
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURAÇÕES E VARIÁVEIS GLOBAIS ---
TOKEN = os.getenv("TELEGRAM_TOKEN") 
NOME_ARQUIVO_EXCEL = "Faturamento_2020a2024_SternaMDF.xlsx" # <- Verifique se o nome bate com o seu
NOME_COLUNA_DATA = "Dia"

# Configura o logging para vermos informações úteis no terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Carrega os dados do Excel UMA VEZ quando o bot inicia
# e os armazena em uma variável global para acesso rápido.
DADOS_FATURAMENTO_GLOBAL = None

def carregar_dados():
    """Carrega e prepara os dados da planilha Excel."""
    global DADOS_FATURAMENTO_GLOBAL
    try:
        df = pd.read_excel(NOME_ARQUIVO_EXCEL, engine='openpyxl')
        df[NOME_COLUNA_DATA] = pd.to_datetime(df[NOME_COLUNA_DATA], errors='coerce')
        df.dropna(subset=[NOME_COLUNA_DATA], inplace=True)
        DADOS_FATURAMENTO_GLOBAL = df
        logging.info(f"Arquivo '{NOME_ARQUIVO_EXCEL}' carregado e processado com sucesso.")
    except Exception as e:
        logging.error(f"Falha crítica ao carregar o arquivo Excel: {e}")
        DADOS_FATURAMENTO_GLOBAL = None

def buscar_faturamento_por_data(data_pesquisa):
    """Busca no DataFrame global por uma data específica."""
    if DADOS_FATURAMENTO_GLOBAL is None:
        return None
    
    # Compara apenas a parte da data (ignora horas/minutos/segundos)
    resultado = DADOS_FATURAMENTO_GLOBAL[DADOS_FATURAMENTO_GLOBAL[NOME_COLUNA_DATA].dt.date == data_pesquisa.date()]
    return resultado

# --- FUNÇÕES DO BOT (HANDLERS) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia uma mensagem de boas-vindas quando o usuário envia /start."""
    mensagem = (
        "Olá! Bem-vindo ao Bot de Consulta de Faturamento.\n\n"
        "Basta me enviar uma data no formato **DD/MM/AAAA** e eu te retornarei as informações."
    )
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def buscar_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa as mensagens de texto que o usuário envia."""
    texto_usuario = update.message.text
    logging.info(f"Recebida mensagem do usuário: {texto_usuario}")

    try:
        # Tenta converter o texto do usuário em uma data
        data_pesquisa = datetime.strptime(texto_usuario, "%d/%m/%Y")
        
        # Realiza a busca
        resultado = buscar_faturamento_por_data(data_pesquisa)
        
        if resultado is not None and not resultado.empty:
            # Formata a resposta para ser bem legível
            # .to_string() mostra todas as colunas sem cortar o texto
            resposta = resultado.to_string(index=False)
            mensagem_final = f"🗓️ **Dados para {texto_usuario}**:\n\n```\n{resposta}\n```"
        else:
            mensagem_final = f"😕 Nenhum dado encontrado para a data *{texto_usuario}*."

    except ValueError:
        mensagem_final = "Formato de data inválido. 😕\nPor favor, use o formato **DD/MM/AAAA**."
    
    # Envia a resposta final para o usuário
    await update.message.reply_text(mensagem_final, parse_mode='Markdown')


# --- FUNÇÃO PRINCIPAL QUE INICIA O BOT ---

def main():
    """Inicia e executa o bot."""
    # Carrega os dados da planilha antes de o bot começar a receber mensagens
    carregar_dados()
    
    if DADOS_FATURAMENTO_GLOBAL is None:
        print("Não foi possível carregar os dados do Excel. O bot não será iniciado.")
        return

    # Cria a aplicação do bot
    application = Application.builder().token(TOKEN).build()

    # Adiciona os "escutadores" de comandos e mensagens
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_data_handler))

    print(">>> Bot iniciado com sucesso! Pressione Ctrl+C para parar. <<<")
    
    # Inicia o bot. Ele ficará rodando e esperando por mensagens.
    application.run_polling()

if __name__ == "__main__":
    main()