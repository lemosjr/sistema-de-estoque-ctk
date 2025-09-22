import json
import os

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
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
             # Se o arquivo estiver vazio ou corrompido, retorna um dicionário vazio.
            return {}


    def _salvar_dados(self):
        """Salva o dicionário de usuários atual no arquivo JSON."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.usuarios, file, ensure_ascii=False, indent=4)

    def validar_credenciais(self, usuario, senha):
        """Verifica se um par de usuário e senha corresponde a um registro existente."""
        return self.usuarios.get(usuario) == senha

    def adicionar_usuario(self, usuario, senha):
        """Adiciona um novo usuário. Retorna False se o usuário já existir."""
        if usuario in self.usuarios:
            return False
        self.usuarios[usuario] = senha
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
        """Remove um item da lista com base em seu ID."""
        self.itens = [item for item in self.itens if item['Id'] != item_id]
        self._salvar_dados()
        
    def buscar_item(self, termo):
        """Busca itens que correspondem a um termo de busca no nome, marca ou tipo."""
        termo = termo.lower()
        return [
            item for item in self.itens 
            if termo in item['Nome'].lower() or 
               termo in item['Marca'].lower() or
               termo in item['Alcoólico'].lower()
        ]