import psycopg2 
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("password")

def conexao():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Frank_Costa",
            user="postgres",
            password='root',
            port="5432"
        )
        print("Banco Conectado")
        return conn
    
    except Exception as e:
       print("Erro ao conectar com o banco de dados:", e)
       return None
  
  
        
def fim_conexao(conn):
    if conn:
        conn.close()
        print("Conexão encerrada")