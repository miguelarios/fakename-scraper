"""Core scraping logic for fakenamegenerator.com."""

import time

import requests
from bs4 import BeautifulSoup


def scrape_identity(gender="random", nameset="us", country="us"):
    """Scrape a single identity from fakenamegenerator.com."""
    url = f"https://www.fakenamegenerator.com/gen-random-{nameset}-{country}.php"
    if gender in ("male", "female"):
        url += f"?gen={gender[0].upper()}{gender[1:]}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    info = soup.select_one(".info")
    if not info:
        raise ValueError("Could not find identity data on page. Site may have changed layout.")

    identity = {}

    name_el = info.select_one(".address h3")
    if name_el:
        identity["name"] = name_el.text.strip()

    adr_el = info.select_one(".adr")
    if adr_el:
        identity["address"] = adr_el.get_text(separator="\n").strip()

    for dl in info.select("dl.dl-horizontal"):
        dt = dl.select_one("dt")
        dd = dl.select_one("dd")
        if dt and dd:
            key = dt.text.strip()
            adtl = dd.select_one(".adtl")
            if adtl:
                adtl.decompose()
            value = dd.get_text(separator=" ").strip()
            if key != "QR Code":
                identity[key] = value

    return identity


def scrape_multiple(count=5, gender="random", nameset="us", country="us", delay=2.0):
    """Scrape multiple identities with a delay between requests."""
    identities = []
    for i in range(count):
        print(f"Scraping identity {i + 1}/{count}...", flush=True)
        try:
            identity = scrape_identity(gender=gender, nameset=nameset, country=country)
            identities.append(identity)
        except Exception as e:
            print(f"  Error: {e}")
        if i < count - 1:
            time.sleep(delay)
    return identities
