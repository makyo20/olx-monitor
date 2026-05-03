import asyncio
import logging
import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config import BOT_TOKEN, CHAT_ID, INTERVAL_MINUTES
from storage import init_db, mark_seen_batch
from scraper import scrape_all
from notifier import send_alerts, send_startup_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("monitor.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("main")


def check_config() -> bool:
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN no encontrado. Configura el archivo .env")
        return False
    if not CHAT_ID:
        logger.error("CHAT_ID no encontrado. Configura el archivo .env")
        return False
    return True


def job() -> None:
    logger.info("=== Iniciando ciclo de revisión — %s ===", datetime.now().strftime("%H:%M:%S"))
    try:
        new_listings = scrape_all()
        if new_listings:
            send_alerts(new_listings)
            mark_seen_batch(new_listings)
            logger.info("✅ %d nuevas vagas notificadas y guardadas", len(new_listings))
        else:
            logger.info("Sin novedades esta vez.")
    except Exception as e:
        logger.error("Error en el ciclo de revisión: %s", e)


def main() -> None:
    if not check_config():
        sys.exit(1)

    logger.info("Inicializando base de datos...")
    init_db()

    logger.info("Enviando mensaje de inicio a Telegram...")
    asyncio.run(send_startup_message())

    logger.info("Ejecutando primera revisión ahora...")
    job()

    scheduler = BlockingScheduler(timezone="America/Sao_Paulo")
    scheduler.add_job(
        job,
        trigger=IntervalTrigger(minutes=INTERVAL_MINUTES),
        id="olx_monitor",
        name="Monitor OLX Vagas",
        misfire_grace_time=60,
    )

    logger.info("Scheduler iniciado — revisando cada %d minutos. Ctrl+C para parar.", INTERVAL_MINUTES)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Monitor detenido por el usuario.")


if __name__ == "__main__":
    main()
