# db_connection.py
import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL.
    A conexão usa DictCursor para retornar resultados como dicionários.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # <-- Mude para o nome do seu banco
            user="postgres",                # <-- Mude para o seu usuário
            password="postgres",      # <-- Mude para a sua senha
            host="localhost",
            port="5433"
        )
        print("Conexão com o PostgreSQL bem-sucedida!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar com o PostgreSQL: {e}")
        return None