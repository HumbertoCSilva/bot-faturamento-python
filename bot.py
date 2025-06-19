# ===================================================================
# ==                 BLOCO DE IMPORTS (TODOS JUNTOS)               ==
# ===================================================================
import pandas as pd
from datetime import datetime, timedelta
import logging
import re
import holidays
import unicodedata
import os
import calendar
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===================================================================
# ==          CONFIGURAÇÃO E CARREGAMENTO DE DADOS                 ==
# ===================================================================

# Carrega as variáveis do arquivo .env (para rodar localmente)
load_dotenv() 

# --- CONFIGURAÇÕES GLOBAIS ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
NOME_ARQUIVO_EXCEL = "Faturamento_2020a2024_SternaMDF.xlsx" 
NOME_COLUNA_DATA = "Dia"
DADOS_FATURAMENTO_GLOBAL = None

# Mapeamento de palavras-chave para os nomes oficiais da biblioteca 'holidays'
MAPEAMENTO_EVENTOS = {
    "carnaval": "Carnival", "dia dos namorados": "Dia dos Namorados", "natal": "Christmas",
    "ano novo": "New Year's Day", "tiradentes": "Tiradentes' Day", "dia do trabalho": "Labour Day",
    "independencia": "Independence Day", "nossa senhora aparecida": "Our Lady of Aparecida",
    "finados": "All Souls' Day", "proclamacao da republica": "Republic Proclamation Day",
    "corpus christi": "Corpus Christi", "sexta-feira santa": "Good Friday",
    "paixao de cristo": "Good Friday", "pascoa": "Easter Sunday"
}

MAPEAMENTO_MESES = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5,
    "junho": 6, "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10,
    "novembro": 11, "dezembro": 12
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- FUNÇÕES DE MANIPULAÇÃO DE DADOS ---

def carregar_dados():
    """Carrega, limpa e prepara os dados da planilha Excel."""
    global DADOS_FATURAMENTO_GLOBAL
    try:
        df = pd.read_excel(NOME_ARQUIVO_EXCEL, engine='openpyxl')
        logging.info(f"Arquivo '{NOME_ARQUIVO_EXCEL}' lido com sucesso. Iniciando limpeza...")

        # --- LIMPEZA E CONVERSÃO DE COLUNAS ---
        coluna_receitas = 'Receitas Totais Líquidas'
        coluna_pessoas = 'Pessoas Atendidas'

        # 1. Converte a coluna de data
        df[NOME_COLUNA_DATA] = pd.to_datetime(df[NOME_COLUNA_DATA], errors='coerce')

        # 2. Limpa a coluna de receita e converte para número (float)
        if coluna_receitas in df.columns:
            df[coluna_receitas] = (df[coluna_receitas]
                                   .astype(str)
                                   .str.replace('R$', '', regex=False)
                                   .str.replace('.', '', regex=False)
                                   .str.replace(',', '.', regex=False)
                                   .str.strip())
            df[coluna_receitas] = pd.to_numeric(df[coluna_receitas], errors='coerce')

        # 3. Converte a coluna de pessoas para número
        if coluna_pessoas in df.columns:
            df[coluna_pessoas] = pd.to_numeric(df[coluna_pessoas], errors='coerce')

        # 4. Remove linhas onde a conversão de data ou valores pode ter falhado
        df.dropna(subset=[NOME_COLUNA_DATA, coluna_receitas, coluna_pessoas], inplace=True)
        
        # Converte a coluna de pessoas para inteiro após limpeza
        if coluna_pessoas in df.columns:
            df[coluna_pessoas] = df[coluna_pessoas].astype(int)

        DADOS_FATURAMENTO_GLOBAL = df
        logging.info("Limpeza e processamento dos dados concluídos com sucesso.")

    except Exception as e:
        logging.error(f"Falha crítica ao carregar ou limpar o arquivo Excel: {e}")

def buscar_faturamento_por_data(data_pesquisa):
    if DADOS_FATURAMENTO_GLOBAL is None: return None
    data_para_comparar = data_pesquisa.date() if isinstance(data_pesquisa, datetime) else data_pesquisa
    resultado = DADOS_FATURAMENTO_GLOBAL[DADOS_FATURAMENTO_GLOBAL[NOME_COLUNA_DATA].dt.date == data_para_comparar]
    return resultado

def buscar_faturamento_por_periodo(data_inicio, data_fim):
    if DADOS_FATURAMENTO_GLOBAL is None: return None
    inicio_para_comparar = data_inicio.date() if isinstance(data_inicio, datetime) else data_inicio
    fim_para_comparar = data_fim.date() if isinstance(data_fim, datetime) else data_fim
    mask = (DADOS_FATURAMENTO_GLOBAL[NOME_COLUNA_DATA].dt.date >= inicio_para_comparar) & (DADOS_FATURAMENTO_GLOBAL[NOME_COLUNA_DATA].dt.date <= fim_para_comparar)
    return DADOS_FATURAMENTO_GLOBAL.loc[mask]

def normalizar_texto(texto):
    texto = texto.lower()
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def processar_evento_texto(texto):
    texto_normalizado = normalizar_texto(texto)
    match_ano = re.search(r'\d{4}', texto_normalizado)
    ano = int(match_ano.group()) if match_ano else datetime.now().year
    
    match_periodo = re.search(r'(\d{1,2}/\d{1,2}/\d{4})\s*a\s*(\d{1,2}/\d{1,2}/\d{4})', texto_normalizado)
    if 'de' in texto_normalizado and 'a' in texto_normalizado and match_periodo:
        data_inicio_str, data_fim_str = match_periodo.groups()
        try:
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
            dados_periodo = buscar_faturamento_por_periodo(data_inicio, data_fim)
            return {"periodo": dados_periodo, "nome_evento": f"Período de {data_inicio_str} a {data_fim_str}"}
        except ValueError:
            pass 

    for nome_mes, num_mes in MAPEAMENTO_MESES.items():
        if nome_mes in texto_normalizado:
            try:
                _, ultimo_dia = calendar.monthrange(ano, num_mes)
                data_inicio = datetime(ano, num_mes, 1)
                data_fim = datetime(ano, num_mes, ultimo_dia)
                dados_periodo = buscar_faturamento_por_periodo(data_inicio, data_fim)
                return {"periodo": dados_periodo, "nome_evento": f"Mês de {nome_mes.capitalize()} de {ano}"}
            except ValueError:
                return {"erro": f"Mês ou ano inválido: {nome_mes} de {ano}"}

    br_holidays = holidays.country_holidays('BR', years=ano)
    evento_encontrado = None
    for palavra_chave, nome_oficial in MAPEAMENTO_EVENTOS.items():
        if palavra_chave in texto_normalizado:
            evento_encontrado = nome_oficial
            break
            
    if evento_encontrado:
        data_evento = br_holidays.get(evento_encontrado)
        if evento_encontrado == "Dia dos Namorados":
            data_evento = datetime(ano, 6, 12)
        
        if not data_evento:
            return {"erro": f"Não foi possível encontrar o feriado '{evento_encontrado}' para o ano {ano}."}
        
        if "semana" in texto_normalizado and "carnaval" in texto_normalizado:
            data_inicio = data_evento - timedelta(days=3)
            data_fim = data_evento + timedelta(days=1)
            dados_periodo = buscar_faturamento_por_periodo(data_inicio, data_fim)
            return {"periodo": dados_periodo, "nome_evento": f"Semana do Carnaval {ano}"}

        dados_feriado = buscar_faturamento_por_data(data_evento)
        return {"data_unica": dados_feriado, "nome_evento": f"{evento_encontrado} {ano}"}

    return {"erro": "Não entendi o comando. Por favor, use um dos formatos conhecidos."}

# ===================================================================
# ==                     LÓGICA DO BOT TELEGRAM                    ==
# ===================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = (
        "Olá! Sou o Bot de Consulta de Faturamento.\n\n"
        "Você pode me enviar:\n"
        "1. Uma data específica: `DD/MM/AAAA`\n"
        "2. Um evento e ano: `carnaval 2024`, `natal 2023`\n"
        "3. Um mês e ano: `fevereiro 2024`\n"
        "4. Um período: `de 01/01/2024 a 15/01/2024`"
    )
    await update.message.reply_text(mensagem, parse_mode='Markdown')

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    logging.info(f"Recebida mensagem: {texto_usuario}")
    
    mensagem_final = ""
    try:
        data_pesquisa = datetime.strptime(texto_usuario, "%d/%m/%Y")
        resultado = buscar_faturamento_por_data(data_pesquisa)
        if resultado is not None and not resultado.empty:
            resposta = resultado.to_string(index=False)
            mensagem_final = f"🗓️ **Dados para {texto_usuario}**:\n\n```\n{resposta}\n```"
        else:
            mensagem_final = f"😕 Nenhum dado encontrado para a data *{texto_usuario}*."
    except ValueError:
        resultado_evento = processar_evento_texto(texto_usuario)
        
        if "erro" in resultado_evento:
            mensagem_final = resultado_evento["erro"]
        
        elif "data_unica" in resultado_evento:
            dados = resultado_evento["data_unica"]
            nome_evento = resultado_evento["nome_evento"]
            if dados is not None and not dados.empty:
                resposta = dados.to_string(index=False)
                mensagem_final = f"🗓️ **Dados para {nome_evento}**:\n\n```\n{resposta}\n```"
            else:
                mensagem_final = f"😕 Nenhum dado encontrado para *{nome_evento}*."

        elif "periodo" in resultado_evento:
            dados = resultado_evento["periodo"]
            nome_evento = resultado_evento["nome_evento"]
            if dados is not None and not dados.empty:
                # Usa as colunas corretas para os cálculos
                total_faturado = dados['Receitas Totais Líquidas'].sum()
                total_pessoas = dados['Pessoas Atendidas'].sum()
                resposta_detalhada = dados.to_string(index=False)
                
                mensagem_final = (
                    f"🗓️ **Resumo para {nome_evento}**:\n\n"
                    f"  - Faturamento Total: **R$ {total_faturado:,.2f}**\n"
                    f"  - Pessoas Atendidas: **{total_pessoas}**\n\n"
                    f"**Detalhes:**\n```\n{resposta_detalhada}\n```"
                )
            else:
                mensagem_final = f"😕 Nenhum dado encontrado para o período da *{nome_evento}*."

    await update.message.reply_text(mensagem_final, parse_mode='Markdown')

# ===================================================================
# ==                   PONTO DE ENTRADA DA APLICAÇÃO               ==
# ===================================================================

def main():
    """Inicia e executa o bot."""
    carregar_dados()
    if DADOS_FATURAMENTO_GLOBAL is None:
        print("Bot não iniciado devido a erro no carregamento dos dados.")
        return

    print("Iniciando o bot do Telegram...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print(">>> Bot inteligente iniciado com sucesso! Pressione Ctrl+C para parar. <<<")
    application.run_polling()

if __name__ == "__main__":
    main()