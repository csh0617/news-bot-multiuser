from flask import Flask, request, render_template, redirect
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    if request.method == "POST":
        new_entry = {
            "user": request.form["user"],
            "chat_id": request.form["chat_id"],
            "telegram_token": request.form["telegram_token"],
            "keywords": [request.form["keyword"]]
        }

        for u in users:
            if u["user"] == new_entry["user"] and u["chat_id"] == new_entry["chat_id"]:
                if request.form["keyword"] not in u["keywords"]:
                    u["keywords"].append(request.form["keyword"])
                break
        else:
            users.append(new_entry)

        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    return render_template("index.html", users=users)

@app.route("/delete", methods=["POST"])
def delete():
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    for u in users:
        if u["user"] == request.form["user"]:
            u["keywords"] = [k for k in u["keywords"] if k != request.form["keyword"]]
            break

    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    return redirect("/")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    if request.method == "POST":
        config["interval"] = int(request.form["interval"])
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    return render_template("settings.html", config=config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
