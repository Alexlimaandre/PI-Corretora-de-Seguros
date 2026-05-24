import psycopg2 
from psycopg2 import Error
import config

password = config.password

def conexao():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Frank_Costa",
            user="postgres",
            password=password,
            port="5432"
        )
        print('connextado com sucesso')
        return conn
    
    except Exception as e:
       print("Erro ao conectar com o banco de dados:", e)
       return None
  
  
        
def fechar_conexao(conn):
    if conn:
        conn.close()