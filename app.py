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
        foto TEXT,
        observacao TEXT
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

input,button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:10px;
}

input{
background:#334155;
    app.run(host="0.0.0.0", port=5000)