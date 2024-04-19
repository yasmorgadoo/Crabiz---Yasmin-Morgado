# Importações das classes necessárias
from usuario import Usuario
from mensagem import Mensagem
from contato import Contato
from conexao import Conexao

# Definição da classe Chat
class Chat:
    
    # Método de inicialização da classe Chat
    def __init__(self, nome_usuario:str, telefone_usuario:str):
        # Atribuição dos dados do usuário que está utilizando o chat
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario
        
    # Método para enviar mensagem
    def enviar_mensagem(self, conteudo: str, destinatario:Contato) -> bool:
        try:
            # Conexão com o banco de dados
            mydb = Conexao.conectar()
            
            # Criação de um cursor para interagir com o banco de dados
            mycursor = mydb.cursor()
            
            # Forma 1: Inserção da mensagem na tabela de mensagens
            sql = "INSERT INTO tb_mensagem (tel_remetente, mensagem, tel_destinatario) VALUES (%s, %s, %s)"
            val = (self.telefone_usuario, conteudo, destinatario.telefone)
            mycursor.execute(sql, val)
            
            # Forma 2 (comentada): outra maneira de inserir mensagem
            # sql = f"INSERT INTO tb_mensagem (tel_remetente, mensagem, tel_destinatario) VALUES ('{self.usuario.telefone}', '{conteudo}','{destinatario.telefone})"
            # mycursor.execute(sql)
            
            # Confirmação da transação no banco de dados
            mydb.commit()
            
            # Retorna True se a mensagem foi enviada com sucesso
            return True
        
        # Tratamento de exceção
        except:
            # Retorna False se ocorrer algum erro no envio da mensagem
            return False
        
    # Método para verificar mensagens recebidas
    def verificar_mensagem(self, quantidade:int, destinatario:Contato):
        
        # Conexão com o banco de dados
        mydb = Conexao.conectar()
        
        # Criação de um cursor para interagir com o banco de dados
        mycursor = mydb.cursor()
        
        # Consulta SQL para buscar mensagens relacionadas ao usuário atual e ao destinatário
        sql = f"SELECT nome, mensagem FROM tb_mensagem m " \
                f"INNER JOIN tb_usuario u " \
                f"ON m.tel_remetente = u.tel " \
                f"WHERE m.tel_remetente = '{self.telefone_usuario}' " \
                    f"AND m.tel_destinatario = '{destinatario.telefone}' "\
                    f"OR m.tel_remetente = '{destinatario.telefone}' " \
                    f"AND m.tel_destinatario = '{self.telefone_usuario}' "
        
        # Execução da consulta SQL
        mycursor.execute(sql)
        
        # Recuperação dos resultados da consulta
        resultado = mycursor.fetchall()
        
        # Lista para armazenar as mensagens encontradas
        lista_mensagens = []
        
        # Iteração sobre os resultados e armazenamento das mensagens na lista
        for linha in resultado:
            # Criando um dicionário representando a mensagem e adicionando à lista
            mensagem = {"nome": linha[0], "mensagem": linha[1]}
            lista_mensagens.append(mensagem)
        
        # Retorna a lista de mensagens
        return lista_mensagens
    
    # Método para retornar a lista de contatos
    def retornar_contatos(self): 
        
        # Conexão com o banco de dados
        mydb = Conexao.conectar()
        
        # Criação de um cursor para interagir com o banco de dados
        mycursor = mydb.cursor()
        
        # Consulta SQL para buscar os contatos ordenados por nome
        sql = "SELECT nome, tel FROM tb_usuario ORDER BY nome"
        
        # Execução da consulta SQL
        mycursor.execute(sql)
        
        # Recuperação dos resultados da consulta
        resultado = mycursor.fetchall()
        
        # Lista para armazenar os contatos
        lista_contatos = []
        
        # Inserção do contato especial "TODOS"
        lista_contatos.append({"nome": "TODOS", "telefone": ""})
        
        # Iteração sobre os resultados e armazenamento dos contatos na lista
        for linha in resultado:
            #Criando a mensagem primeiro e incluindo na lista
            contato = {"nome":linha[0],"telefone":linha[1]}
            lista_contatos.append(contato)
        
        return (lista_contatos)
