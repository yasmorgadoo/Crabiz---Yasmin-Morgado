# Importações das bibliotecas e classes necessárias
from flask import Flask, render_template, request, jsonify, session, redirect
from usuario import Usuario
from chat import Chat
from mensagem import Mensagem
from contato import Contato 

# Criação de uma instância da aplicação Flask
app = Flask(__name__)

# Definição de uma chave secreta para a sessão
app.secret_key = "batatinhafrita123"

# Rota GET para o index ou cadastro
@app.route("/")
@app.route("/cadastro_via_form")
def pag_cadastro():
    return render_template("cadastro_via_form.html")

# Rota POST para o cadastro, recebe dados do formulário
@app.route("/cadastro_via_form", methods=["POST"])
def post_cadastro():
    # Obtém os dados do formulário
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    senha = request.form["senha"]

    # Instancia um objeto usuário
    usuario = Usuario()
    
    # Cadastra o usuário e retorna se foi bem-sucedido ou não
    if usuario.cadastrar(nome, telefone, senha) == True:
        # Define os dados do usuário na sessão
        session['usuario_logado'] = {"nome":usuario.nome,
                                     "telefone":usuario.telefone}
        return redirect("/login")
    else:
        # Limpa a sessão em caso de erro no cadastro
        session.clear()
        return "Erro ao cadastrar"

# Rota GET para outra página de cadastro, realiza o cadastro via requisição AJAX
@app.route("/cadastrar_via_ajax")
def pag_cadastro_ajax():
    return render_template("cadastro_via_ajax.html")

# Rota POST para o cadastro via AJAX
@app.route("/cadastrar_via_ajax", methods=["POST"])
def post_cadastro_ajax():
    # Obtém os dados enviados via AJAX
    dados = request.get_json()
    
    nome = dados["nome"]
    telefone = dados["telefone"]
    senha = dados["senha"]
    
    # Instancia um objeto usuário
    usuario = Usuario()
    
    # Cadastra o usuário e retorna se foi bem-sucedido ou não
    if usuario.cadastrar(nome, telefone, senha) == True:
        return redirect("/login")
    else:
        return jsonify({'mensagem':'ERRO'}), 500
    
# Rota GET para a tela de login
@app.route("/login")
def pag_login():
    return render_template("login.html")

# Rota POST para verificar o login do usuário
@app.route("/login", methods=["POST"])
def pag_login_post():
    telefone = request.form["telefone"]
    senha = request.form["senha"]
    
    usuario = Usuario()
    
    usuario.logar(telefone,senha)
    
    if usuario.logado == True:
        # Define os dados do usuário na sessão se o login for bem-sucedido
        session['usuario_logado'] = {"nome":usuario.nome,
                                     "telefone":usuario.telefone}
        return redirect("/chat")
    else:
        # Redireciona de volta para a página de login se o login falhar
        return redirect("/login")

# Rota GET para a página do chat, só é acessível se o usuário estiver logado
@app.route("/chat")
def pag_chat():
    if "usuario_logado" in session:
        return render_template("chat.html")
    else:
        return redirect("/cadastro_via_form")

# Rota GET para retornar os usuários cadastrados em formato JSON
@app.route("/retorna_usuarios")
def retorna_usuarios():
    # Obtém os dados do usuário logado na sessão
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    
    # Instancia um objeto Chat
    chat = Chat(nome_usuario,telefone_usuario)
    
    # Obtém a lista de contatos
    contatos = chat.retornar_contatos()
    
    # Retorna a lista de contatos em formato JSON
    return jsonify(contatos), 200

# Rota GET para retornar as mensagens de um determinado destinatário em formato JSON
@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    # Obtém os dados do usuário logado na sessão
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    # Instancia um objeto Chat
    chat = Chat(nome_usuario,telefone_usuario)

    # Cria um objeto Contato para representar o destinatário das mensagens
    contato_destinatario = Contato("", tel_destinatario)

    # Obtém a lista de mensagens do destinatário especificado
    lista_de_mensagens = chat.verificar_mensagem(0, contato_destinatario)

    # Retorna a lista de mensagens em formato JSON
    return jsonify(lista_de_mensagens), 200


# Rota para o envio de mensagem via AJAX
@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem_ajax():
    if request.method == "POST":
        # Recebe os dados da requisição AJAX
        dados = request.json
        destinatario = dados["destinatario"]
        mensagem = dados["mensagem"]

        # Obtém o nome e o telefone do usuário logado na sessão
        nome_usuario = session["usuario_logado"]["nome"]
        telefone_usuario = session["usuario_logado"]["telefone"]
        
        # Instancia um objeto Chat para interagir com os contatos e mensagens
        chat = Chat(nome_usuario, telefone_usuario)
        # Cria um objeto Contato com o telefone do destinatário
        contato_destinatario = Contato("", destinatario)
        envia = chat.enviar_mensagem(mensagem,contato_destinatario)
        return jsonify({"status": "Mensagem enviada com sucesso"}), 200
    else:
       
        return jsonify({"status": "Erro ao enviar mensagem"}), 5000

# Executa a aplicação Flask em modo de depuração
app.run(debug=True)
