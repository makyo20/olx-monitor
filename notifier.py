import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError

from config import BOT_TOKEN, CHAT_ID

logger = logging.getLogger(__name__)


def _format_message(listing: dict) -> str:
    return (
        "🔔 *Nova vaga encontrada!*\n\n"
        f"📌 *{listing['title']}*\n"
        f"🔑 Keyword: `{listing['keyword']}`\n"
        f"🔗 [Ver anúncio]({listing['url']})"
    )


async def _send_one(bot: Bot, listing: dict) -> None:
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=_format_message(listing),
            parse_mode="Markdown",
            disable_web_page_preview=False,
        )
    except TelegramError as e:
        logger.error("Error enviando alerta para '%s': %s", listing.get("title"), e)


async def send_alerts_async(listings: list[dict]) -> None:
    if not listings:
        return
    bot = Bot(token=BOT_TOKEN)
    async with bot:
        tasks = [_send_one(bot, listing) for listing in listings]
        await asyncio.gather(*tasks)
    logger.info("%d alertas enviadas por Telegram", len(listings))


def send_alerts(listings: list[dict]) -> None:
    """Wrapper sincrónico para llamar desde el scheduler."""
    if not BOT_TOKEN or not CHAT_ID:
        logger.error("BOT_TOKEN o CHAT_ID no configurados en .env")
        return
    asyncio.run(send_alerts_async(listings))


async def send_startup_message() -> None:
    """Mensaje de inicio al arrancar el programa."""
    bot = Bot(token=BOT_TOKEN)
    async with bot:
        try:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=(
                    "✅ *Monitor OLX iniciado!*\n\n"
                    "Revisando vagas en Curitiba/Pinhais cada 5 minutos.\n"
                    "Keywords: vaga, vaga curitiba, vaga pinhais, ajudante, auxiliar"
                ),
                parse_mode="Markdown",
            )
        except TelegramError as e:
            logger.error("Error enviando mensaje de inicio: %s", e)
