import os
import json
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[에러] users.json 로드 실패: {e}")
            return []
    return []

def save_users(users):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        print("[💾] 저장됨: users.json")
    except Exception as e:
        print(f"[에러] users.json 저장 실패: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    users = load_users()
    if request.method == "POST":
        user = request.form["user"].strip()
        chat_id = request.form["chat_id"].strip()
        token = request.form["telegram_token"].strip()
        keyword = request.form["keyword"].strip()

        if not (user and chat_id and token and keyword):
            return "모든 항목을 입력해야 합니다.", 400

        existing = next((u for u in users if u["chat_id"] == chat_id), None)
        if existing:
            if keyword not in existing["keywords"]:
                existing["keywords"].append(keyword)
        else:
            users.append({
                "name": user,
                "chat_id": chat_id,
                "telegram_token": token,
                "keywords": [keyword]
            })

        save_users(users)
        return redirect("/")

    return render_template("index.html", users=users)

@app.route("/delete", methods=["POST"])
def delete_keyword():
    users = load_users()
    user = request.form["user"]
    keyword = request.form["keyword"]

    for u in users:
        if u["name"] == user and keyword in u["keywords"]:
            u["keywords"].remove(keyword)

    save_users(users)
    return redirect("/")

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


