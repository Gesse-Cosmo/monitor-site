import requests
from bs4 import BeautifulSoup
import os
import json

# ======================
# CONFIGURAÇÃO
# ======================
URL = "https://www.vaticannews.va/pt.html"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

STATE_FILE = "noticias_vistas.json"

# ======================
# FUNÇÃO TELEGRAM
# ======================
def enviar(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg
        },
        timeout=20
    )

# ======================
# DOWNLOAD DA PÁGINA
# ======================
html = requests.get(URL, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

# ======================
# COLETA DE NOTÍCIAS
# ======================
noticias = []

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

# Remove duplicados pelo link
unicas = list({n["link"]: n for n in noticias}.values())

# ======================
# CONTROLE DE ESTADO
# ======================
primeira_execucao = not os.path.exists(STATE_FILE)

if not primeira_execucao:
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        vistos = json.load(f)
else:
    vistos = []

links_vistos = {n["link"] for n in vistos}

novas = [n for n in unicas if n["link"] not in links_vistos]

# Salva estado atualizado SEMPRE
with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(unicas, f, ensure_ascii=False, indent=2)

# ======================
# ENVIO DE ALERTAS
# ======================
if primeira_execucao:
    print("Primeira execução detectada — estado salvo, nenhuma notificação enviada.")
    exit(0)

for n in novas:
    mensagem = (
        "📰 Nova notícia no Vatican News:\n\n"
        f"{n['titulo']}\n\n"
        f"🔗 {n['link']}"
    )
    enviar(mensagem)