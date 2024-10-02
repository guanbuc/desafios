# -*- encoding: utf-8 -*-


import db
from flask import Flask, render_template, request


app = Flask(__name__)

DB = db.Database()

dados = None

@app.route('/', methods=["GET", "POST"])
def principal():
    stmt = 'SELECT c.Name cliente, \
                   p.Name projeto, \
                   a.Descricao, \
                   p.DataInicio, \
                   p.DataFim \
            FROM Clientes c, \
                 Projetos p, \
                 Atividades a \
            WHERE c.Id = p.ClientesId \
             AND  p.Id  = a.ProjetosId'

    DB.DdlExecute()
    result = DB.DqlExecute(stmt)

    return render_template("index.html", result=result)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    registros = []
    if request.method == "POST":
        if request.form.get("cliente") \
                and request.form.get("projeto") \
                and request.form.get("descricao")\
                and request.form.get("dtinicio") \
                and request.form.get("dtfim"):
            registros.append({"cliente": request.form.get("cliente") \
                                 , "projeto": request.form.get("projeto") \
                                 , "descricao": request.form.get("descricao") \
                                 , "dtinicio": request.form.get("dtinicio") \
                                 , "dtfim": request.form.get("dtfim")})
            DB.DdlExecute()
            DB.DmlExecute(registros)

    return render_template("cadastro.html", registros=registros)