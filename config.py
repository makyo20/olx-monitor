import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")

KEYWORDS = [
    # Trabajo
    "vaga",
    "vaga curitiba",
    "vaga pinhais",
    "ajudante",
    "auxiliar",
    "emprego pinhais",
    "contrata pinhais",
    "serviço pinhais",
    "oportunidade pinhais",
    # Vivienda
    "alugo casa",
    "quarto pinhais",
    "alugo quarto pinhais",
    "kitnet pinhais",
    "república pinhais",
    "casa pinhais",
    "alugo curitiba uberaba",
]

OLX_BASE_URL = "https://pr.olx.com.br/curitiba-e-regiao"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

REQUEST_TIMEOUT = 15        # segundos
DELAY_BETWEEN_REQUESTS = 3  # segundos entre keywords
INTERVAL_MINUTES = 5        # intervalo de revisión
DB_PATH = "olx_seen.db"
