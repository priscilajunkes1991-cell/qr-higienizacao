from flask import Flask, request, render_template_string, redirect
import sqlite3
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def conectar():
    return sqlite3.connect("dados.db")


with conectar() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS equipamentos (
        id INTEGER PRIMARY KEY,
        higienizacao TEXT,
        proxima TEXT,
        intervalo INTEGER,
        sala TEXT,
        observacao TEXT,
        foto TEXT
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
max-width:420px;
margin:auto;
}

.logo{
width:220px;
display:block;
margin:auto;
margin-bottom:20px;
}

input, textarea, button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:10px;
}

input, textarea{
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
padding:15px;
margin-top:15px;
border-radius:10px;
}

.foto{
width:100%;
border-radius:10px;
margin-top:15px;
}

</style>

</head>

<body>

<div class="card">

<img src="/static/logo.png" class="logo">

<h2>Equipamento {{id}}</h2>

<form method="POST" enctype="multipart/form-data">

<label>Nome da Sala</label>
<input type="text" name="sala" placeholder="Ex: Recepção">

<label>Data da Higienização</label>
<input type="date" name="higienizacao" required>

<label>Intervalo em Dias</label>
<input type="number" name="intervalo" required>

<label>Observação Técnica</label>
<textarea name="observacao" rows="4"
placeholder="Ex: Equipamento com vazamento"></textarea>

<label>Foto do Equipamento</label>
<input type="file" name="foto">

<button type="submit">Salvar</button>

</form>

{% if dados %}

<div class="info">

<p>📍 Sala: {{dados[3]}}</p>
<p>🧼 Última: {{dados[0]}}</p>
<p>📅 Próxima: {{dados[1]}}</p>
<p>⏱ Intervalo: {{dados[2]}} dias</p>
<p>🛠 Observação: {{dados[4]}}</p>

</div>

{% if dados[5] %}

<img src="/static/uploads/{{dados[5]}}" class="foto">

{% endif %}

{% endif %}

</div>

</body>
</html>
"""


@app.route("/equipamento/<int:id>", methods=["GET", "POST"])
def equipamento(id):

    conn = conectar()

    if request.method == "POST":

        sala = request.form["sala"]
        hig = request.form["higienizacao"]
        intervalo = int(request.form["intervalo"])
        observacao = request.form["observacao"]

        data_base = datetime.strptime(hig, "%Y-%m-%d")
        proxima = data_base + timedelta(days=intervalo)

        foto = request.files.get("foto")
        nome_foto = None

        if foto and foto.filename != "":
            nome_foto = secure_filename(f"equip_{id}_{foto.filename}")
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_foto)
            foto.save(caminho)

        conn.execute("""
        INSERT OR REPLACE INTO equipamentos
        (id, higienizacao, proxima, intervalo, sala, observacao, foto)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            id,
            hig,
            proxima.strftime("%Y-%m-%d"),
            intervalo,
            sala,
            observacao,
            nome_foto
        ))

        conn.commit()

        return redirect(f"/equipamento/{id}")

    dados = conn.execute("""
    SELECT higienizacao, proxima, intervalo,
    sala, observacao, foto
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