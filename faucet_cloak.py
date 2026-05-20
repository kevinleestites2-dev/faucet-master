"""
FaucetCloak — Autonomous Traffic Engine
Drives stealth visits to all faucet sites using CloakBrowser.
Each visit = unique fingerprint, human-like behavior, Adsterra popunder triggered.
"""

import asyncio
import random
import logging
from cloakbrowser import launch
from cloakbrowser.human import (
    patch_page_async,
    async_human_idle,
    async_human_scroll_into_view,
    async_human_move,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("FaucetCloak")

# ── TARGETS ──────────────────────────────────────────────────────────────────
FAUCET_SITES = [
    "https://maticdrop-1.onrender.com",
    "https://maticdrop-2.onrender.com",
    "https://maticdrop-3.onrender.com",
    "https://maticdrop-4.onrender.com",
    "https://maticdrop-5.onrender.com",
]

# ── CONFIG ────────────────────────────────────────────────────────────────────
VISITS_PER_SITE = 200          # visits per site per run
DWELL_MIN = 15                 # min seconds on page (triggers popunder)
DWELL_MAX = 45                 # max seconds on page
CONCURRENCY = 3                # parallel browsers at once
HEADLESS = True

# ── USER AGENTS (rotating pool) ───────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
]

# ── VIEWPORTS ─────────────────────────────────────────────────────────────────
VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1366, "height": 768},
    {"width": 1280, "height": 800},
    {"width": 390,  "height": 844},   # iPhone
    {"width": 412,  "height": 915},   # Android
]

# ── REFERRERS ─────────────────────────────────────────────────────────────────
REFERRERS = [
    "https://www.google.com/search?q=free+matic+faucet",
    "https://www.google.com/search?q=polygon+faucet+2024",
    "https://t.co/",
    "https://reddit.com/r/CryptoCurrency",
    "https://twitter.com/",
    "",  # direct
]


async def visit_site(url: str, visit_num: int):
    """Single stealth visit to a faucet site."""
    ua = random.choice(USER_AGENTS)
    vp = random.choice(VIEWPORTS)
    ref = random.choice(REFERRERS)
    dwell = random.uniform(DWELL_MIN, DWELL_MAX)

    try:
        browser = launch(
            headless=HEADLESS,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context = browser.new_context(
            user_agent=ua,
            viewport=vp,
            locale=random.choice(["en-US", "en-GB", "en-CA", "es-US"]),
            timezone_id=random.choice([
                "America/New_York", "America/Chicago",
                "America/Los_Angeles", "America/Denver",
                "Europe/London", "Europe/Berlin",
            ]),
            extra_http_headers={"Referer": ref} if ref else {},
        )
        page = context.new_page()
        await patch_page_async(page)

        log.info(f"[Visit {visit_num}] → {url} | UA: {ua[:40]}...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Human-like behavior — scroll, idle, move mouse
        await async_human_idle(page, min_ms=1000, max_ms=3000)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
        await async_human_idle(page, min_ms=2000, max_ms=5000)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        await async_human_idle(page, min_ms=1000, max_ms=2000)

        # Dwell on page (popunder fires here)
        await asyncio.sleep(dwell)

        log.info(f"[Visit {visit_num}] ✅ Done — dwelled {dwell:.1f}s")

    except Exception as e:
        log.warning(f"[Visit {visit_num}] ⚠️ Error: {e}")
    finally:
        try:
            browser.close()
        except:
            pass


async def run_site(url: str, total_visits: int):
    """Drive N visits to a single site with concurrency control."""
    sem = asyncio.Semaphore(CONCURRENCY)

    async def bounded_visit(i):
        async with sem:
            await visit_site(url, i)

    tasks = [bounded_visit(i + 1) for i in range(total_visits)]
    await asyncio.gather(*tasks)


async def main():
    log.info("🔱 FaucetCloak — Autonomous Traffic Engine ONLINE")
    log.info(f"Targets: {len(FAUCET_SITES)} sites × {VISITS_PER_SITE} visits = {len(FAUCET_SITES) * VISITS_PER_SITE} total visits")

    for site in FAUCET_SITES:
        log.info(f"\n{'='*60}")
        log.info(f"🎯 Targeting: {site}")
        log.info(f"{'='*60}")
        await run_site(site, VISITS_PER_SITE)

    log.info("\n🔱 All sites hit. FaucetCloak cycle complete.")


if __name__ == "__main__":
    asyncio.run(main())
