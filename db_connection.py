import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    """
    Estabelece e retorna uma conexão com o banco de dados PostgreSQL.

    A conexão é configurada para retornar linhas como dicionários (DictCursor),
    facilitando o acesso aos dados por nome de coluna.

    :return: Um objeto de conexão psycopg2 em caso de sucesso, ou None em caso de falha.
    """
    try:
        # --- CONFIGURAÇÕES DE CONEXÃO ---
        # Altere os valores abaixo para corresponder à sua configuração do PostgreSQL.
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5433"
        )
        # Mensagem de sucesso para depuração. Pode ser removida em produção.
        print("Conexão com o PostgreSQL bem-sucedida!")
        return conn
        
    except psycopg2.OperationalError as e:
        # Mensagem de erro para depuração.
        print(f"Erro ao conectar com o PostgreSQL: {e}")
        return None