from flask import Flask, request, render_template_string, redirect
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def conectar():
    return sqlite3.connect("dados.db")

with conectar() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS equipamentos (
        id INTEGER PRIMARY KEY,
        higienizacao TEXT,
        proxima TEXT,
        intervalo INTEGER
    )
    """)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

body{
background:#0f172a;
font-family:Arial;
color:white;
padding:20px;
}

.card{
background:#1e293b;
padding:20px;
border-radius:15px;
max-width:400px;
margin:auto;
}

input,button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:10px;
}

input{
background:#334155;
color:white;
}

button{
background:#22c55e;
color:white;
font-weight:bold;
cursor:pointer;
}

.info{
background:#020617;
padding:10px;
margin-top:15px;
border-radius:10px;
}

</style>
</head>

<body>

<div class="card">

<h2>Equipamento {{id}}</h2>

<form method="POST">

<label>Data da Higienização</label>
<input type="date" name="higienizacao" required>

<label>Intervalo em Dias</label>
<input type="number" name="intervalo" required>

<button type="submit">Salvar</button>

</form>

{% if dados %}

<div class="info">
<p>🧼 Última: {{dados[0]}}</p>
<p>📅 Próxima: {{dados[1]}}</p>
<p>⏱ Intervalo: {{dados[2]}} dias</p>
</div>

{% endif %}

</div>

</body>
</html>
"""

@app.route("/equipamento/<int:id>", methods=["GET", "POST"])

def equipamento(id):

    conn = conectar()

    if request.method == "POST":

        hig = request.form["higienizacao"]
        intervalo = int(request.form["intervalo"])

        data_base = datetime.strptime(hig, "%Y-%m-%d")

        proxima = data_base + timedelta(days=intervalo)

        conn.execute("""

        INSERT INTO equipamentos
        (id, higienizacao, proxima, intervalo)

        VALUES (?, ?, ?, ?)

        ON CONFLICT(id) DO UPDATE SET

        higienizacao=excluded.higienizacao,
        proxima=excluded.proxima,
        intervalo=excluded.intervalo

        """, (
            id,
            hig,
            proxima.strftime("%Y-%m-%d"),
            intervalo
        ))

        conn.commit()

        return redirect(f"/equipamento/{id}")

    dados = conn.execute("""

    SELECT higienizacao, proxima, intervalo

    FROM equipamentos

    WHERE id=?

    """, (id,)).fetchone()

    conn.close()

    return render_template_string(
        HTML,
        id=id,
        dados=dados
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)