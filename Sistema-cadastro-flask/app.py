from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="empresa"
    )

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        # aqui conecta com o banco de dados
        conexao = conectar()
        
        # cria um 'cursor', que funciona como um controle remoto para enviar comandos SQL
        cursor = conexao.cursor()
        
        # aqui colocamos na tabela os valores
        cursor.execute("SELECT * FROM funcionarios WHERE email = %s AND senha = %s", (email, senha))
        
        #O fetchone() tenta pegar 1 (um) resultado da consulta acima
        # Se encontrar alguém, a variável 'user' terá os dados. Se não, será 'None'
        user = cursor.fetchone()
        
        # fecha o 'controle remoto' (cursor) para liberar memória do servidor cursor.close()
        cursor.close()
        
        #Fecha a 'porta' (conexão). isso é essencial! Se não fechar,
        # o banco trava depois de alguns acessos por excesso de conexões abertas.
        #conexao.close()
        conexao.close()

        #aqui se tiver usuario correto email|senha ele vai pro painel, senao ele da mensagem de login invalido
        if user: 
            return redirect("/painel")
        else:
            return "Login Inválido! Verifique email e senha."

    return render_template("login.html")

@app.route("/cadastro", methods = ["GET", "POST"])
def cadastro():
    if request.method == "POST":
        # Pega os dados do formulário
        nome = request.form["nome"]
        email = request.form["email"]
        idade = request.form["idade"]
        telefone = request.form["telefone"]
        sexo = request.form["sexo"]
        funcao = request.form["funcao"]
        senha = request.form["senha"]

        # CONECTA E SALVA (Tudo isso precisa estar dentro do IF)
        conexao = conectar()
        cursor = conexao.cursor()
        
        # Verifique se o nome da tabela no seu banco é 'funcionarios' (no plural)
        sql = "INSERT INTO funcionarios (nome, email, idade, telefone, sexo, funcao, senha) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores = (nome, email, idade, telefone, sexo, funcao, senha)
        
        # Envia o comando para o banco de dados, encaixando os valores nos seus devidos lugares.
        cursor.execute(sql, valores)
        
        # o COMANDO MAIS IMPORTANTE: O commit() salva as alterações permanentemente.
        # sem essa linha, o MySQL recebe os dados, mas não os grava no banco de dado (o cadastro 'some').
        conexao.commit()
        
         # fecha o 'controle remoto' (cursor) para liberar memória do servidor cursor.close()
        cursor.close()
        
        # fecha a 'porta' (conexão) com o banco de dados
        conexao.close()
        
        return redirect("/") # Volta para o login após cadastrar
    
    # Se for apenas abrindo a página (GET), mostra o formulário
    return render_template("cadastro.html")

@app.route("/painel")
def painel():
    return render_template("painel.html")

@app.route("/cliente", methods = ["GET", "POST"])
def cliente():
    if request.method == "POST":
        empresa = request.form["empresa"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        endereco = request.form["endereco"]
        estado = request.form["estado"]
        pedido = request.form["pedido"]
        quantidade = request.form["quantidade"]

        conexao = conectar()
        cursor = conexao.cursor()

        sql = "INSERT INTO cliente (empresa, email, telefone, endereco, estado, pedido, quantidade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores = (empresa, email, telefone, endereco, estado, pedido, quantidade)

        cursor.execute(sql, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect("/painel")
    
    return render_template("cliente.html")


@app.route("/fornecedor", methods = ["GET", "POST"])
def fornecedor():
    if request.method == "POST":
        empresa = request.form["empresa"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        endereco = request.form["endereco"]
        estado = request.form["estado"]
        pedido = request.form["pedido"]
        quantidade = request.form["quantidade"]
        
        conexao = conectar()
        cursor = conexao.cursor()

        sql = "INSERT INTO fornecedor (empresa, email, telefone, endereco, estado, pedido, quantidade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores = (empresa, email, telefone, endereco, estado, pedido, quantidade)

        cursor.execute(sql, valores)
        conexao.commit()

        cursor.close()
        conexao.close()
        
        return redirect("/painel")
    
    return render_template("fornecedor.html")
        

if __name__ == "__main__":
    app.run(debug=True)