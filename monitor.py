import requests
from bs4 import BeautifulSoup
import os
import hashlib

URL = "https://noticias.cancaonova.com/"

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem
    }
    requests.post(url, data=payload)

# Baixa o site
html = requests.get(URL, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

# Pega títulos (h3 funciona bem no Vatican News)
titulos = [
    h.text.strip()
    for h in soup.find_all("h3")
    if h.text.strip()
]

conteudo = "\n".join(titulos)

# Gera hash do conteúdo
hash_atual = hashlib.sha256(conteudo.encode()).hexdigest()

hash_antigo = ""
if os.path.exists("hash.txt"):
    with open("hash.txt", "r") as f:
        hash_antigo = f.read()

# Se mudou
if hash_atual != hash_antigo:
    with open("hash.txt", "w") as f:
        f.write(hash_atual)

    # Descobre títulos novos
    antigos = set(hash_antigo.split("\n"))
    novos = titulos[:5]  # pega os primeiros (mais recentes)

    mensagem = "📰 *Novas publicações no Vatican News:*\n\n"
    for t in novos:
        mensagem += f"• {t}\n"

    mensagem += f"\n🔗 {URL}"

    enviar_telegram(mensagem)
