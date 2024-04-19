# Importação da classe de conexão com o banco de dados e da função de criptografia sha256
from conexao import Conexao
from hashlib import sha256

# Definição da classe Usuario
class Usuario():
    
    # Método de inicialização da classe Usuario
    def __init__(self) -> None:
        # Inicialização das propriedades do usuário
        self.nome = None
        self.telefone = None
        self.senha = None
        self.logado = False
        
    # Método para cadastrar um novo usuário
    def cadastrar(self, nome, telefone, senha):
        
        # Criptografando a senha usando o algoritmo SHA-256
        senha = sha256(senha.encode()).hexdigest()
        
        try:
            # Conexão com o banco de dados
            mydb = Conexao.conectar()
            
            # Criação de um cursor para interagir com o banco de dados
            mycursor = mydb.cursor()
            
            # Forma 1: Inserção dos dados do usuário na tabela de usuários
            sql = "INSERT INTO tb_usuario (nome, tel, senha) VALUES (%s, %s, %s)"
            val = (nome, telefone, senha)
            mycursor.execute(sql, val)
            
            # Forma 2 (comentada): outra maneira de inserir os dados do usuário
            # sql = f"INSERT INTO tb_usuario (nome, tel, senha) VALUES ('{nome}', '{telefone}', '{senha}')"
            # mycursor.execute(sql)
            
            # Confirmação da transação no banco de dados
            mydb.commit()
            
            # Atribuição dos dados do usuário e marcação como logado
            self.nome = nome
            self.telefone = telefone
            self.senha = senha
            self.logado = True
            
            # Retorna True se o cadastro for bem-sucedido
            return True
        
        # Tratamento de exceção
        except:
            # Retorna False se ocorrer algum erro no cadastro do usuário
            return False
        
    # Método para realizar login
    def logar(self, telefone, senha):
        
        # Criptografando a senha fornecida para comparar com a senha armazenada no banco de dados
        senha = sha256(senha.encode()).hexdigest()
         
        # Conexão com o banco de dados
        mydb = Conexao.conectar()
        
        # Criação de um cursor para interagir com o banco de dados
        mycursor = mydb.cursor()
        
        # Forma 1: Consulta para buscar um usuário com o número de telefone e senha correspondentes
        sql = "SELECT nome, tel, senha FROM tb_usuario where tel = %s and BINARY senha = %s;"
        valores = (telefone, senha)
        mycursor.execute(sql, valores)
        
        # Forma 2 (comentada): outra maneira de executar a consulta
        # sql = f"SELECT * FROM tb_usuario where tel = ' ' and senha = '{senha}';"
        # mycursor.execute(sql)
     
        # Recuperação do resultado da consulta
        resultado = mycursor.fetchone()
        
        # Verifica se o usuário foi encontrado no banco de dados
        if resultado != None:
            # Marca o usuário como logado e atribui os dados do usuário
            self.logado = True
            self.nome = resultado[0]
            self.telefone = resultado[1]
            self.senha = resultado[2]
        else:
            # Marca o usuário como não logado se não for encontrado no banco de dados
            self.logado = False


