
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "medcontrol-chave-local"


# Conexão com o banco de dados
def conectar_banco():
    conexao = sqlite3.connect("medcontrol.db")
    conexao.row_factory = sqlite3.Row
    return conexao


# Criar tabela de pacientes
def criar_banco():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            telefone TEXT,
            email TEXT
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            medico TEXT NOT NULL,
            status TEXT DEFAULT 'Agendada',
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
    """)

    # Atualizar bancos antigos que ainda não possuem email
    colunas = [
        coluna["name"]
        for coluna in conexao.execute(
            "PRAGMA table_info(pacientes)"
        ).fetchall()
    ]

    if "email" not in colunas:
        conexao.execute(
            "ALTER TABLE pacientes ADD COLUMN email TEXT"
        )

    conexao.commit()
    conexao.close()


# Página inicial
@app.route("/")
def inicio():
    conexao = conectar_banco()

    total_pacientes = conexao.execute(
        "SELECT COUNT(*) FROM pacientes"
    ).fetchone()[0]

    hoje = date.today().strftime("%Y-%m-%d")

    consultas_hoje = conexao.execute(
        """
        SELECT COUNT(*) FROM consultas
        WHERE data = ? AND status != 'Cancelada'
        """,
        (hoje,)
    ).fetchone()[0]

    # Buscar as próximas 5 consultas
    proximas_consultas = conexao.execute("""
        SELECT consultas.*, pacientes.nome AS paciente_nome
        FROM consultas
        JOIN pacientes ON consultas.paciente_id = pacientes.id
        WHERE consultas.data >= ?
        AND consultas.status != 'Cancelada'
        ORDER BY consultas.data, consultas.horario
        LIMIT 5
    """, (hoje,)).fetchall()

    conexao.close()

    return render_template(
        "index.html",
        total_pacientes=total_pacientes,
        consultas_hoje=consultas_hoje,
        proximas_consultas=proximas_consultas
    )



# Listar pacientes
@app.route("/pacientes")
def pacientes():
    conexao = conectar_banco()

    lista = conexao.execute(
        "SELECT * FROM pacientes ORDER BY nome"
    ).fetchall()

    conexao.close()

    # Busca linear de pacientes pelo nome
    pesquisa = request.args.get("pesquisa", "").strip()

    if pesquisa:
        resultados = []

        for paciente in lista:
            if pesquisa.lower() in paciente["nome"].lower():
                resultados.append(paciente)

        lista = resultados

    return render_template(
        "pacientes.html",
        pacientes=lista,
        pesquisa=pesquisa
    )



# Cadastrar paciente
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        idade = request.form.get("idade", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not idade:
            flash("Preencha o nome e a idade.")
            return redirect(url_for("cadastrar"))

        try:
            idade = int(idade)

            if idade < 0:
                raise ValueError

        except ValueError:
            flash("Informe uma idade válida.")
            return redirect(url_for("cadastrar"))

        conexao = conectar_banco()

        conexao.execute(
            """
            INSERT INTO pacientes
            (nome, idade, telefone, email)
            VALUES (?, ?, ?, ?)
            """,
            (nome, idade, telefone, email)
        )

        conexao.commit()
        conexao.close()

        flash("Paciente cadastrado com sucesso!")

        return redirect(url_for("pacientes"))

    return render_template("cadastrar.html")


# Excluir paciente
@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM pacientes WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    flash("Cadastro excluído.")

    return redirect(url_for("pacientes"))


# Cancelar consulta
@app.route("/cancelar_consulta/<int:id>", methods=["POST"])
def cancelar_consulta(id):
    conexao = conectar_banco()

    conexao.execute(
        "UPDATE consultas SET status = 'Cancelada' WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    flash("Consulta cancelada com sucesso!")

    return redirect(url_for("consultas"))


# Página de consultas
@app.route("/consultas", methods=["GET", "POST"])
def consultas():

    conexao = conectar_banco()

    if request.method == "POST":
        paciente_id = request.form.get("paciente_id")
        data = request.form.get("data")
        horario = request.form.get("horario")
        medico = request.form.get("medico", "").strip()

        if paciente_id and data and horario and medico:
            conexao.execute("""
                INSERT INTO consultas
                (paciente_id, data, horario, medico)
                VALUES (?, ?, ?, ?)
            """, (paciente_id, data, horario, medico))

            conexao.commit()
            flash("Consulta agendada com sucesso!")
        else:
            flash("Preencha todos os campos.")

        conexao.close()
        return redirect(url_for("consultas"))

    lista_pacientes = conexao.execute("""
        SELECT id, nome FROM pacientes ORDER BY nome
    """).fetchall()

    lista_consultas = conexao.execute("""
        SELECT consultas.*, pacientes.nome AS paciente_nome
        FROM consultas
        JOIN pacientes ON consultas.paciente_id = pacientes.id
        ORDER BY consultas.data, consultas.horario
    """).fetchall()

    conexao.close()

    return render_template(
        "consultas.html",
        pacientes=lista_pacientes,
        consultas=lista_consultas
    )


# API de pacientes
@app.route("/api/pacientes")
def api_pacientes():
    conexao = conectar_banco()

    lista = conexao.execute(
        "SELECT * FROM pacientes ORDER BY nome"
    ).fetchall()

    conexao.close()

    pacientes = []

    for paciente in lista:
        pacientes.append({
            "id": paciente["id"],
            "nome": paciente["nome"],
            "idade": paciente["idade"],
            "telefone": paciente["telefone"],
            "email": paciente["email"]
        })

    return {
        "total": len(pacientes),
        "pacientes": pacientes
    }

criar_banco()

if __name__ == "__main__":
    app.run(debug=False)





