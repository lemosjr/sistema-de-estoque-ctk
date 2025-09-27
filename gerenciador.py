import bcrypt
from psycopg2.extras import DictCursor # Permite que os resultados do banco de dados venham como dicionários

class GerenciadorUsuarios:
    """Gerencia todas as operações de usuário com o banco de dados."""

    def __init__(self, db_conn):
        """Inicializa o gerenciador com uma conexão de banco de dados ativa.
        
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
        """Adiciona um novo usuário ao banco de dados, com a senha criptografada."""
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT id FROM usuarios WHERE usuario = %s OR email = %s", (usuario, email))
            if cur.fetchone():
                return False  # Usuário ou email já existe

            senha_bytes = senha.encode('utf-8')
            senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')
            
            cur.execute(
                "INSERT INTO usuarios (usuario, senha_hash, nome, email) VALUES (%s, %s, %s, %s)",
                (usuario, senha_hash, nome, email)
            )
            self.db_conn.commit()
            return True
            
    def obter_dados_usuario(self, usuario):
        """Busca e retorna o nome e o email de um usuário em formato de dicionário."""
        with self.db_conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT nome, email FROM usuarios WHERE usuario = %s", (usuario,))
            return cur.fetchone()

    def obter_nome_usuario(self, usuario):
        """Busca e retorna apenas o nome completo de um usuário."""
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT nome FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cur.fetchone()
            return resultado[0] if resultado else usuario

    def editar_usuario(self, usuario_atual, novo_nome, novo_email, nova_senha=None):
        """Atualiza nome, email e, opcionalmente, a senha de um usuário.
        
        Retorna strings de status: 'sucesso', 'email_em_uso' ou 'falha'.
        """
        with self.db_conn.cursor() as cur:
            # Verifica se o novo e-mail já está em uso por outro usuário
            cur.execute("SELECT id FROM usuarios WHERE email = %s AND usuario != %s", (novo_email, usuario_atual))
            if cur.fetchone():
                return "email_em_uso"

            if nova_senha:
                # Se uma nova senha foi fornecida, gera o hash e atualiza todos os campos
                nova_senha_bytes = nova_senha.encode('utf-8')
                nova_senha_hash = bcrypt.hashpw(nova_senha_bytes, bcrypt.gensalt()).decode('utf-8')
                cur.execute(
                    "UPDATE usuarios SET nome = %s, email = %s, senha_hash = %s WHERE usuario = %s",
                    (novo_nome, novo_email, nova_senha_hash, usuario_atual)
                )
            else:
                # Caso contrário, atualiza apenas nome e e-mail
                cur.execute(
                    "UPDATE usuarios SET nome = %s, email = %s WHERE usuario = %s",
                    (novo_nome, novo_email, usuario_atual)
                )
            
            self.db_conn.commit()
            return "sucesso" if cur.rowcount > 0 else "falha"

class GerenciadorItens:
    """Gerencia todas as operações de itens (CRUD) com o banco de dados."""

    def __init__(self, db_conn):
        """Inicializa o gerenciador com uma conexão de banco de dados ativa.
        
        :param db_conn: Objeto de conexão do psycopg2.
        """
        self.db_conn = db_conn

    def _formatar_item(self, item_row):
        """Converte uma linha do banco para um dicionário padronizado para a interface."""
        if not item_row:
            return None
        
        item_dict = dict(item_row)
        item_dict['Alcoólico'] = 'sim' if item_dict.pop('alcoolico') else 'nao'

        # Garante a ordem das chaves para consistência com a TreeView da interface
        return {
            'Id': item_dict['id'],
            'Nome': item_dict['nome'],
            'Alcoólico': item_dict['Alcoólico'],
            'Marca': item_dict['marca'],
            'Quantidade': item_dict['quantidade'],
            'Valor': float(item_dict['valor']) # Converte o tipo Decimal do DB para float
        }

    def listar_itens(self):
        """Retorna uma lista de todos os itens cadastrados no banco de dados."""
        with self.db_conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id, nome, alcoolico, marca, quantidade, valor FROM itens ORDER BY id")
            itens = cur.fetchall()
            return [self._formatar_item(item) for item in itens]

    def adicionar_item(self, nome, tipo, marca, quantidade, valor):
        """Adiciona um novo item ao banco de dados."""
        alcoolico = True if tipo.lower() == 'sim' else False
        with self.db_conn.cursor() as cur:
            cur.execute(
                "INSERT INTO itens (nome, alcoolico, marca, quantidade, valor) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (nome, alcoolico, marca, quantidade, valor)
            )
            novo_id = cur.fetchone()[0]
            self.db_conn.commit()
            
            # Retorna o dicionário do item recém-criado para consistência
            return {
                "Id": novo_id, "Nome": nome, "Alcoólico": tipo, "Marca": marca, 
                "Quantidade": quantidade, "Valor": valor
            }

    def atualizar_item(self, item_id, nome, tipo, marca, quantidade, valor):
        """Atualiza os dados de um item existente com base no seu ID."""
        alcoolico = True if tipo.lower() == 'sim' else False
        with self.db_conn.cursor() as cur:
            cur.execute(
                "UPDATE itens SET nome = %s, alcoolico = %s, marca = %s, quantidade = %s, valor = %s WHERE id = %s",
                (nome, alcoolico, marca, quantidade, valor, item_id)
            )
            self.db_conn.commit()
            return cur.rowcount > 0 # Retorna True se a operação foi bem-sucedida

    def remover_item(self, item_id):
        """Remove um item do banco de dados com base no seu ID."""
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM itens WHERE id = %s", (item_id,))
            self.db_conn.commit()
            return cur.rowcount > 0 # Retorna True se a operação foi bem-sucedida

    def buscar_item(self, termo):
        """Busca itens cujo nome ou marca correspondem a um termo de pesquisa."""
        termo_like = f"%{termo.lower()}%"
        with self.db_conn.cursor(cursor_factory=DictCursor) as cur:
            # Usa lower() para fazer a busca ignorando maiúsculas e minúsculas
            cur.execute(
                "SELECT id, nome, alcoolico, marca, quantidade, valor FROM itens WHERE lower(nome) LIKE %s OR lower(marca) LIKE %s ORDER BY id",
                (termo_like, termo_like)
            )
            itens = cur.fetchall()
            return [self._formatar_item(item) for item in itens]
        
    def favoritar_bebida(self, usuario, bebida):
        """Salva ou atualiza a bebida favorita de um usuário."""
        with self.db_conn.cursor() as cur:
            # ON CONFLICT garante que um usuário tenha apenas uma bebida favorita (UPSERT)
            cur.execute(
                "INSERT INTO bebidas_favoritas (usuario, bebida) VALUES (%s, %s) ON CONFLICT (usuario) DO UPDATE SET bebida = EXCLUDED.bebida",
                (usuario, bebida)
            )
            self.db_conn.commit()
            return True
    
    def obter_bebida_favorita(self, usuario):
        """Obtém a bebida favorita de um usuário do banco de dados."""
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT bebida FROM bebidas_favoritas WHERE usuario = %s", (usuario,))
            resultado = cur.fetchone()
            return resultado[0] if resultado else None