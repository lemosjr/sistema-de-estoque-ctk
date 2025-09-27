# gerenciador.py
import bcrypt
from psycopg2.extras import DictCursor # Importante para os resultados virem como dicionários

class GerenciadorUsuarios:
    """Gerencia o cadastro e a validação de usuários usando um banco de dados PostgreSQL."""

    def __init__(self, db_conn):
        """
        Inicializa o gerenciador com uma conexão de banco de dados.
        :param db_conn: Objeto de conexão do psycopg2.
        """
        self.db_conn = db_conn

    def validar_credenciais(self, usuario, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado no banco de dados."""
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT senha_hash FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cur.fetchone()
            
            if resultado:
                senha_hash_db = resultado[0].encode('utf-8')
                senha_digitada_bytes = senha.encode('utf-8')
                return bcrypt.checkpw(senha_digitada_bytes, senha_hash_db)
        return False

    def adicionar_usuario(self, usuario, senha, nome, email):
        """Adiciona um novo usuário com a senha hasheada no banco de dados."""
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT id FROM usuarios WHERE usuario = %s OR email = %s", (usuario, email))
            if cur.fetchone():
                return False  # Usuário ou email já existe

            senha_bytes = senha.encode('utf-8')
            senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')
            
            # ALTERADO: Inserindo os novos campos
            cur.execute(
                "INSERT INTO usuarios (usuario, senha_hash, nome, email) VALUES (%s, %s, %s, %s)",
                (usuario, senha_hash, nome, email)
            )
            self.db_conn.commit()
            return True
    
    def editar_usuario(self, usuario, nova_senha):
        """Atualiza a senha de um usuário existente."""
        with self.db_conn.cursor() as cur:
            # Gera o hash da nova senha
            nova_senha_bytes = nova_senha.encode('utf-8')
            nova_senha_hash = bcrypt.hashpw(nova_senha_bytes, bcrypt.gensalt()).decode('utf-8')
            
            # Atualiza a senha do usuário
            cur.execute(
                "UPDATE usuarios SET senha_hash = %s WHERE usuario = %s",
                (nova_senha_hash, usuario)
            )
            self.db_conn.commit() # Efetiva a transação
            return cur.rowcount > 0 # Retorna True se alguma linha foi afetada
        
    

class GerenciadorItens:
    """Gerencia o cadastro, a atualização, a remoção e a busca de itens no PostgreSQL."""

    def __init__(self, db_conn):
        """
        Inicializa o gerenciador com uma conexão de banco de dados.
        :param db_conn: Objeto de conexão do psycopg2.
        """
        self.db_conn = db_conn

    def _formatar_item(self, item_row):
        """Converte uma linha do banco (com booleano) para o formato de dicionário esperado (com 'sim'/'nao')."""
        if not item_row:
            return None
        
        item_dict = dict(item_row) # Converte DictRow para um dict padrão
        item_dict['Alcoólico'] = 'sim' if item_dict.pop('alcoolico') else 'nao'

        # Garante a ordem das chaves para consistência com a TreeView
        return {
            'Id': item_dict['id'],
            'Nome': item_dict['nome'],
            'Alcoólico': item_dict['Alcoólico'],
            'Marca': item_dict['marca'],
            'Quantidade': item_dict['quantidade'],
            'Valor': float(item_dict['valor']) # Converte Decimal para float
        }

    def listar_itens(self):
        """Retorna a lista completa de itens do banco de dados."""
        with self.db_conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id, nome, alcoolico, marca, quantidade, valor FROM itens ORDER BY id")
            itens = cur.fetchall()
            # Converte 'alcoolico' (True/False) para 'Alcoólico' ('sim'/'nao')
            return [self._formatar_item(item) for item in itens]

    def adicionar_item(self, nome, tipo, marca, quantidade, valor):
        """Cria um novo item e o insere no banco de dados."""
        alcoolico = True if tipo.lower() == 'sim' else False
        with self.db_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO itens (nome, alcoolico, marca, quantidade, valor)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (nome, alcoolico, marca, quantidade, valor)
            )
            novo_id = cur.fetchone()[0]
            self.db_conn.commit()
            
            # Para manter a consistência, retornamos o item recém-criado
            return {
                "Id": novo_id, "Nome": nome, "Alcoólico": tipo, "Marca": marca, 
                "Quantidade": quantidade, "Valor": valor
            }

    def atualizar_item(self, item_id, nome, tipo, marca, quantidade, valor):
        """Atualiza os dados de um item existente com base em seu ID."""
        alcoolico = True if tipo.lower() == 'sim' else False
        with self.db_conn.cursor() as cur:
            cur.execute(
                """
                UPDATE itens
                SET nome = %s, alcoolico = %s, marca = %s, quantidade = %s, valor = %s
                WHERE id = %s
                """,
                (nome, alcoolico, marca, quantidade, valor, item_id)
            )
            self.db_conn.commit()
            return cur.rowcount > 0 # Retorna True se alguma linha foi afetada

    def remover_item(self, item_id):
        """Remove um item do banco de dados com base em seu ID."""
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM itens WHERE id = %s", (item_id,))
            self.db_conn.commit()
            return cur.rowcount > 0 # Retorna True se alguma linha foi afetada

    def buscar_item(self, termo):
        """Busca itens que correspondem a um termo de busca no nome ou marca."""
        termo_like = f"%{termo.lower()}%"
        with self.db_conn.cursor(cursor_factory=DictCursor) as cur:
            # ILIKE faz a busca ignorando maiúsculas e minúsculas
            cur.execute(
                """
                SELECT id, nome, alcoolico, marca, quantidade, valor FROM itens
                WHERE lower(nome) LIKE %s OR lower(marca) LIKE %s
                ORDER BY id
                """,
                (termo_like, termo_like)
            )
            itens = cur.fetchall()
            return [self._formatar_item(item) for item in itens]
        
    def favoritar_bebida(self, usuario, bebida):
        """Salva a bebida favorita do usuário no banco de dados."""
        with self.db_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO bebidas_favoritas (usuario, bebida)
                VALUES (%s, %s)
                ON CONFLICT (usuario) DO UPDATE SET bebida = EXCLUDED.bebida
                """,
                (usuario, bebida)
            )
            self.db_conn.commit()
            return True
    
    def obter_bebida_favorita(self, usuario):
        """Obtém a bebida favorita do usuário do banco de dados."""
        with self.db_conn.cursor() as cur:
            cur.execute(
                "SELECT bebida FROM bebidas_favoritas WHERE usuario = %s",
                (usuario,)
            )
            resultado = cur.fetchone()
            return resultado[0] if resultado else None
        
