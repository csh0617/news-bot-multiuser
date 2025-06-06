import time
import json
import requests
from bs4 import BeautifulSoup

def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)

def search_news(keyword):
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select(".news_tit")
    results = []
    for link in links[:3]:
        title = link.get("title")
        href = link.get("href")
        results.append(f"{title}\n{href}")
    return results

def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def main():
    while True:
        try:
            users = load_users()
            for user in users:
                for kw in user["keywords"]:
                    articles = search_news(kw)
                    for article in articles:
                        send_message(user["telegram_token"], user["chat_id"], f"🔍 [{kw}]\n{article}")
        except Exception as e:
            print("Error:", e)
        with open("config.json", "r", encoding="utf-8") as f:
            interval = json.load(f).get("interval", 1800)
        time.sleep(interval)

if __name__ == "__main__":
    main()
