from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cloud2_db_user:DXkIdIuZKlCY1vxs7rJTY25VbbaSltpK@dpg-d5cgpfhr0fns739mt5tg-a.oregon-postgres.render.com/cloud2_db"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT,
            mesaj TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        data = request.get_json() or {}
        isim = data.get("isim")
        mesaj = data.get("mesaj")

        if isim and mesaj:
            cur.execute(
                "INSERT INTO ziyaretciler (isim, mesaj) VALUES (%s, %s)",
                (isim, mesaj)
            )
            conn.commit()

    cur.execute(
        "SELECT isim, mesaj FROM ziyaretciler ORDER BY id DESC LIMIT 10"
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([{"isim": r[0], "mesaj": r[1]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
