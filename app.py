from flask import Flask, render_template, request, redirect
import requests
import sqlite3

app = Flask(__name__)

API_KEY = "cc706f96354e40c3bfea70e3d29b762"

# Create DB
def init_db():
    conn = sqlite3.connect("comments.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        news_title TEXT,
        comment TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    query = request.args.get("q")
    category = request.args.get("category")

    if query:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"
    elif category:
        url = f"https://newsapi.org/v2/top-headlines?country=ng&category={category}&apiKey={API_KEY}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country=ng&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()
    print(data) # DEBUG
    articles = data.get("articles", [])

    # Save comment
    if request.method == "POST":
        title = request.form.get("title")
        comment = request.form.get("comment")

        conn = sqlite3.connect("comments.db")
        c = conn.cursor()
        c.execute("INSERT INTO comments (news_title, comment) VALUES (?, ?)", (title, comment))
        conn.commit()
        conn.close()

        return redirect("/")

    # Load comments
    conn = sqlite3.connect("comments.db")
    c = conn.cursor()
    c.execute("SELECT * FROM comments")
    comments = c.fetchall()
    conn.close()

    return render_template("index.html", articles=articles, comments=comments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


