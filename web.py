from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

# ✅ users.json 파일 없으면 자동 생성
if not os.path.exists("users.json"):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def load_users():
    with open("users.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    users = load_users()
    if request.method == "POST":
        name = request.form["user"]
        chat_id = request.form["chat_id"]
        token = request.form["telegram_token"]
        keyword = request.form["keyword"]

        for user in users:
            if user["name"] == name and user["chat_id"] == chat_id:
                if keyword not in user["keywords"]:
                    user["keywords"].append(keyword)
                save_users(users)
                return redirect("/")

        users.append({
            "name": name,
            "chat_id": chat_id,
            "telegram_token": token,
            "keywords": [keyword]
        })
        save_users(users)
        return redirect("/")
    return render_template("index.html", users=users)

@app.route("/delete", methods=["POST"])
def delete():
    user_name = request.form["user"]
    keyword = request.form["keyword"]

    users = load_users()
    for user in users:
        if user["name"] == user_name and keyword in user["keywords"]:
            user["keywords"].remove(keyword)
    save_users(users)
    return redirect("/")

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

