import requests
import hashlib
import os

URL = "https://www.vaticannews.va/pt.htmlhttps://www.vaticannews.va/pt.html"

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

html = requests.get(URL).text
hash_atual = hashlib.sha256(html.encode()).hexdigest()

try:
    with open("hash.txt") as f:
        hash_antigo = f.read()
except FileNotFoundError:
    hash_antigo = ""

if hash_atual != hash_antigo:
    enviar("🚨 O site foi atualizado!")
    with open("hash.txt", "w") as f:
        f.write(hash_atual)
