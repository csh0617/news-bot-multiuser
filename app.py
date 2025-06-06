import json
import time
import requests
from bs4 import BeautifulSoup

def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[에러] users.json 로드 실패: {e}")
        return []

def search_news(keyword):
    print(f"[🔍] 뉴스 검색: '{keyword}'")
    url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select(".news_tit")
        results = []
        for link in links[:3]:  # 상위 3개만 추출
            title = link.get("title")
            href = link.get("href")
            results.append({"title": title, "link": href})
        return results
    except Exception as e:
        print(f"[에러] 뉴스 검색 실패: {e}")
        return []

def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        response = requests.post(url, data={"chat_id": chat_id, "text": text})
        print(f"[📤] 전송됨: {text[:20]}... / 상태: {response.status_code}")
        if response.status_code != 200:
            print(f"[❌] 전송 실패 내용: {response.text}")
    except Exception as e:
        print(f"[에러] 전송 중 오류 발생: {e}")

print("[*] 뉴스 전송 백그라운드 워커 시작됨")

while True:
    print("\n[🔁] 루프 시작 ====================")
    users = load_users()
    for user in users:
        print(f"[👤] 사용자: {user['name']} ({user['chat_id']})")
        for kw in user["keywords"]:
            articles = search_news(kw)
            if not articles:
                print(f"[😢] '{kw}' 관련 뉴스 없음")
            for article in articles:
                send_message(user["telegram_token"], user["chat_id"], f"📰 {article['title']}\n🔗 {article['link']}")
    time.sleep(600)  # 10분마다 반복
