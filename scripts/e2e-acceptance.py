import sys, time, subprocess, http.server, socketserver, threading, os
from playwright.sync_api import sync_playwright

ROOT = "/private/tmp/rvc-nassau-address/site"
PORT = 8791

os.chdir(ROOT)
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{PORT}/index.html"

CASES = [
    ("1 College Pl, Rockville Centre, NY", "nassau-found"),
    ("235 Lido Blvd, Long Beach, NY",      "nassau-found"),
    ("22 Horse Hollow Rd, Locust Valley, NY", "nassau-found"),
    ("158 Laurel Ave, Northport, NY",      "suffolk-fallback"),
]

def read_state(page):
    return page.evaluate("""() => {
      const g = document.getElementById('moneyGeo');
      const cards = document.getElementById('kitCards');
      const firstCardName = cards && cards.style.display!=='none' ? (cards.querySelector('a') ? cards.querySelector('a').textContent : null) : null;
      return {
        bannerShown: g && g.style.display!=='none',
        banner: g ? g.textContent : '',
        mvStar: (document.getElementById('mvStar')||{}).textContent,
        mvTransfer: (document.getElementById('mvTransfer')||{}).textContent,
        mvSale: (document.getElementById('mvSale')||{}).textContent,
        mvSaleGeo: (document.getElementById('mvSaleGeo')||{}).textContent,
        starFlash: (document.getElementById('mrowStar')||{className:''}).className.includes('geo-flash'),
        cardsShown: cards && cards.style.display!=='none',
        firstCardName: firstCardName,
        btn: (document.getElementById('kitBuild')||{}).textContent
      };
    }""")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()

    # default page (no interaction)
    pg.goto(base, wait_until="load")
    time.sleep(1.0)
    dflt = read_state(pg)
    print("DEFAULT (no user interaction):")
    print(f"  banner shown={dflt['bannerShown']}  mvStar={dflt['mvStar']}  mvTransfer={dflt['mvTransfer']}  mvSaleGeo={dflt['mvSaleGeo']}")
    print(f"  button label='{dflt['btn']}'")
    print()

    for addr, kind in CASES:
        pg.goto(base, wait_until="load")
        pg.wait_for_selector("#kitBuild")
        pg.fill("#kitAddr", addr)
        pg.click("#kitBuild")
        # wait for banner to appear (money refresh) up to 15s
        try:
            pg.wait_for_function("() => { const g=document.getElementById('moneyGeo'); return g && g.style.display!=='none'; }", timeout=15000)
        except Exception:
            pass
        # give cards + fetch a moment
        time.sleep(1.5)
        st = read_state(pg)
        print(f"=== {addr}  [{kind}] ===")
        print(f"  banner: {st['banner']}")
        print(f"  mvStar={st['mvStar']}  mvTransfer={st['mvTransfer']}  mvSale={st['mvSale']}  mvSaleGeo={st['mvSaleGeo']}")
        print(f"  starFlash={st['starFlash']}  cardsShown={st['cardsShown']}  firstCard='{st['firstCardName']}'  btn='{st['btn']}'")
        print()

    b.close()
httpd.shutdown()
