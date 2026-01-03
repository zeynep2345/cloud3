from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

API_URL = "https://cloud3-6a4n.onrender.com/ziyaretciler"

HTML = """
<!doctype html>
<html>
<head>
    <title>Mikro Hizmetli Selam</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
        input { padding: 8px; margin: 5px; }
        button { padding: 8px 12px; }
        li { background: white; margin: 5px auto; width: 250px; padding: 8px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam</h1>

    <form method="POST">
        <input name="isim" placeholder="İsim" required>
        <input name="mesaj" placeholder="Mesaj" required>
        <button type="submit">Gönder</button>
    </form>

    <h3>Ziyaretçiler</h3>
    <ul>
        {% for z in isimler %}
            <li><b>{{ z.isim }}</b>: {{ z.mesaj }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        requests.post(API_URL, json={
            "isim": request.form["isim"],
            "mesaj": request.form["mesaj"]
        })
        return redirect("/")

    try:
        resp = requests.get(API_URL, timeout=5)
        isimler = resp.json()
    except:
        isimler = []

    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
