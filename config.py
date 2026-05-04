import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")

OLX_BASE_URL_CURITIBA = "https://pr.olx.com.br/curitiba-e-regiao"
OLX_BASE_URL_PARANA   = "https://pr.olx.com.br"

# Cada entrada: {"keyword": "...", "base_url": "..."}
SEARCH_CONFIGS = [
    # --- Trabajo (Curitiba/Pinhais) ---
    {"keyword": "vaga curitiba",       "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "vaga pinhais",        "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "ajudante",            "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "auxiliar",            "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "emprego pinhais",     "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "contrata pinhais",    "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "serviço pinhais",     "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "oportunidade pinhais","base_url": OLX_BASE_URL_CURITIBA},
    # --- Trabajo (todo Paraná) ---
    {"keyword": "vaga",                "base_url": OLX_BASE_URL_PARANA},
    # --- Vivienda (Curitiba/Pinhais) ---
    {"keyword": "alugo casa",          "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "quarto pinhais",      "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "alugo quarto pinhais","base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "kitnet pinhais",      "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "república pinhais",   "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "casa pinhais",        "base_url": OLX_BASE_URL_CURITIBA},
    {"keyword": "alugo curitiba uberaba","base_url": OLX_BASE_URL_CURITIBA},
]

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
