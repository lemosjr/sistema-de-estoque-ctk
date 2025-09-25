import json
import os
import bcrypt

class GerenciadorUsuarios:
    """Gerencia o cadastro e a validação de usuários em um arquivo JSON."""

    def __init__(self, filepath="usuarios.json"):
        self.filepath = filepath
        self.usuarios = self._carregar_dados()

    def _carregar_dados(self):
        """Carrega os usuários do arquivo JSON. Se o arquivo não existir, cria um vazio."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump({}, file)
            return {}
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                dados_carregados = json.load(file)
                # Convertemos as senhas de string de volta para bytes
                return {
                    usuario: senha_hash.encode('utf-8')
                    for usuario, senha_hash in dados_carregados.items()
                }
        except (json.JSONDecodeError, FileNotFoundError):
            return {}


    def _salvar_dados(self):
        """Salva o dicionário de usuários atual no arquivo JSON."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            # O dicionário agora conterá hashes, que são bytes.
            # Precisamos de uma forma de salvá-los em JSON.
            # Vamos converter os bytes para strings antes de salvar.
            usuarios_para_salvar = {
                usuario: senha_hash.decode('utf-8') 
                for usuario, senha_hash in self.usuarios.items()
            }
            json.dump(usuarios_para_salvar, file, ensure_ascii=False, indent=4)

    def validar_credenciais(self, usuario, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        senha_hash = self.usuarios.get(usuario)
        if senha_hash:
            # Compara a senha digitada (em bytes) com o hash do arquivo
            return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)
        return False

    def adicionar_usuario(self, usuario, senha):
        """Adiciona um novo usuário com a senha hasheada."""
        if usuario in self.usuarios:
            return False
        
        # Gera o hash da senha
        senha_bytes = senha.encode('utf-8')
        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        
        self.usuarios[usuario] = senha_hash
        self._salvar_dados()
        return True

class GerenciadorItens:
    """Gerencia o cadastro, a atualização, a remoção e a busca de itens em um arquivo JSON."""

    def __init__(self, filepath="itens.json"):
        self.filepath = filepath
        self.itens = self._carregar_dados()
        self.item_id = self._obter_proximo_id()

    def _carregar_dados(self):
        """Carrega a lista de itens do arquivo JSON. Retorna uma lista vazia se não existir."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Se o arquivo estiver vazio ou corrompido, retorna uma lista vazia.
            return []

    def _salvar_dados(self):
        """Salva a lista de itens atual no arquivo JSON."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.itens, file, indent=4)

    def _obter_proximo_id(self):
        """Retorna o próximo ID disponível para um novo item."""
        if not self.itens:
            return 1
        return max(item['Id'] for item in self.itens) + 1

    def listar_itens(self):
        """Retorna a lista completa de itens."""
        return self.itens

    def adicionar_item(self, nome, tipo, marca, quantidade, valor):
        """Cria um novo item com um ID único e o adiciona à lista."""
        novo_item = {
            "Id": self.item_id, 
            "Nome": nome, 
            "Alcoólico": tipo,
            "Marca": marca, 
            "Quantidade": quantidade,
            "Valor": valor
        }
        self.itens.append(novo_item)
        self.item_id += 1
        self._salvar_dados()
        return novo_item

    def atualizar_item(self, item_id, nome, tipo, marca, quantidade, valor):
        """Atualiza os dados de um item existente com base em seu ID."""
        for item in self.itens:
            if item['Id'] == item_id:
                item.update({
                    "Nome": nome, 
                    "Alcoólico": tipo, 
                    "Marca": marca, 
                    "Quantidade": quantidade,
                    "Valor": valor
                })
                self._salvar_dados()
                return True
        return False
        
    def remover_item(self, item_id):
        """Remove um item da lista com base em seu ID e retorna True se bem-sucedido."""
        tamanho_inicial = len(self.itens)
        self.itens = [item for item in self.itens if item['Id'] != item_id]
        
        # Se o tamanho da lista diminuiu, a remoção foi bem-sucedida
        if len(self.itens) < tamanho_inicial:
            self._salvar_dados()
            return True
        return False
        
    def buscar_item(self, termo):
        """Busca itens que correspondem a um termo de busca no nome, marca ou tipo."""
        termo = termo.lower()
        return [
            item for item in self.itens 
            if termo in item['Nome'].lower() or 
               termo in item['Marca'].lower() or
               termo in item['Alcoólico'].lower()
        ]