import re
import time
import logging
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from config import OLX_BASE_URL, HEADERS, REQUEST_TIMEOUT, DELAY_BETWEEN_REQUESTS, KEYWORDS
from storage import is_new

logger = logging.getLogger(__name__)


def _extract_id_from_url(url: str) -> str:
    """Extrae el ID numérico del final del URL de OLX."""
    match = re.search(r"-(\d+)(?:\?.*)?$", url)
    if match:
        return match.group(1)
    return url.split("/")[-1].split("?")[0]


def _parse_listings(html: str, keyword: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    listings = []

    # OLX Brasil — selectores principales (pueden variar con actualizaciones)
    # Intentamos múltiples estrategias
    cards = (
        soup.select("section[data-ds-component='DS-AdCard']")
        or soup.select("li[data-testid='ad-list-item']")
        or soup.select("li.sc-1fcmfeb-2")
        or soup.select("div[data-lurker-detail='list'] li")
    )

    if not cards:
        # Fallback: buscar todos los <a> que parezcan anuncios
        cards = soup.select("a[href*='/d/']")
        for card in cards:
            href = card.get("href", "")
            if not href or "/d/" not in href:
                continue
            title = card.get_text(strip=True)[:120]
            listing_id = _extract_id_from_url(href)
            if listing_id:
                listings.append({"id": listing_id, "title": title, "url": href, "keyword": keyword})
        return listings

    for card in cards:
        link_tag = card.find("a", href=True)
        if not link_tag:
            continue

        href = link_tag.get("href", "")
        if not href or "/d/" not in href:
            continue

        # Título: h2, h3, o el texto del link
        title_tag = card.find("h2") or card.find("h3") or link_tag
        title = title_tag.get_text(strip=True)[:120] if title_tag else ""

        listing_id = _extract_id_from_url(href)
        if not listing_id:
            continue

        listings.append({
            "id": listing_id,
            "title": title,
            "url": href if href.startswith("http") else f"https://www.olx.com.br{href}",
            "keyword": keyword,
        })

    return listings


def scrape_keyword(keyword: str) -> list[dict]:
    """Scrapes OLX para una keyword. Retorna lista de anuncios encontrados."""
    params = urlencode({"q": keyword})
    url = f"{OLX_BASE_URL}?{params}"

    try:
        with httpx.Client(headers=HEADERS, timeout=REQUEST_TIMEOUT, follow_redirects=True) as client:
            response = client.get(url)

        if response.status_code == 429:
            logger.warning("Rate limit (429) para keyword '%s'. Esperando 30s...", keyword)
            time.sleep(30)
            with httpx.Client(headers=HEADERS, timeout=REQUEST_TIMEOUT, follow_redirects=True) as client:
                response = client.get(url)

        response.raise_for_status()
        listings = _parse_listings(response.text, keyword)
        logger.info("Keyword '%s': %d anuncios encontrados en OLX", keyword, len(listings))
        return listings

    except httpx.TimeoutException:
        logger.error("Timeout al scrapear keyword '%s'", keyword)
        return []
    except httpx.HTTPStatusError as e:
        logger.error("HTTP %s al scrapear keyword '%s'", e.response.status_code, keyword)
        return []
    except Exception as e:
        logger.error("Error inesperado con keyword '%s': %s", keyword, e)
        return []


def scrape_all() -> list[dict]:
    """
    Scrapes todas las keywords, deduplica y retorna solo anuncios nuevos.
    """
    seen_ids: set[str] = set()
    all_new: list[dict] = []

    for i, keyword in enumerate(KEYWORDS):
        listings = scrape_keyword(keyword)

        for listing in listings:
            lid = listing["id"]
            if lid in seen_ids:
                continue
            seen_ids.add(lid)
            if is_new(lid):
                all_new.append(listing)

        if i < len(KEYWORDS) - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)

    logger.info("Total anuncios NUEVOS encontrados: %d", len(all_new))
    return all_new
