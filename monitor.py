import requests
from bs4 import BeautifulSoup
import os
import json

URL ="https://noticias.cancaonova.com/"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

STATE_FILE = "noticias_vistas.json"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

# Baixa o site
html = requests.get(URL, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

noticias = []

# Vatican News: links das notícias costumam estar em <a>
for a in soup.find_all("a", href=True):
    titulo = a.get_text(strip=True)
    link = a["href"]

    if not titulo:
        continue

    if link.startswith("/"):
        link = "https://www.vaticannews.va" + link

    if "vaticannews.va" in link:
        noticias.append({
            "titulo": titulo,
            "link": link
        })

# Remove duplicados
unicas = {n["link"]: n for n in noticias}.values()

# Carrega estado anterior
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        vistos = json.load(f)
else:
    vistos = []

links_vistos = {n["link"] for n in vistos}

novas = [n for n in unicas if n["link"] not in links_vistos]

# Salva estado atualizado
with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(list(unicas), f, ensure_ascii=False, indent=2)

# Envia somente as novas
for n in novas:
    mensagem = (
        "📰 *Nova notícia no Vatican News:*\n\n"
        f"{n['titulo']}\n\n"
        f"🔗 {n['link']}"
    )
    enviar(mensagem)