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
        with open(self.filepath, "r", encoding="utf-8") as file:
            return json.load(file)

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
    """Gerencia as operações de CRUD (Criar, Ler, Atualizar, Deletar) para itens."""

    def __init__(self, filepath="itens.json"):
        self.filepath = filepath
        self.itens = self._carregar_dados()
        
        # Define o próximo ID com base no maior ID existente para evitar duplicatas.
        if self.itens:
            self.item_id = max(item['Id'] for item in self.itens)
        else:
            self.item_id = 0

    def _carregar_dados(self):
        """Carrega a lista de itens do arquivo JSON. Retorna uma lista vazia se não existir."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    def _salvar_dados(self):
        """Salva a lista de itens atual no arquivo JSON."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.itens, file, indent=4)

    def adicionar_item(self, nome, tipo, marca, quantidade):
        """Cria um novo item com um ID único e o adiciona à lista."""
        self.item_id += 1
        novo_item = {
            "Id": self.item_id, "Nome": nome, "Alcoólico": tipo,
            "Marca": marca, "Quantidade": quantidade
        }
        self.itens.append(novo_item)
        self._salvar_dados()
        return novo_item

    def atualizar_item(self, item_id, nome, tipo, marca, quantidade):
        """Atualiza os dados de um item existente com base em seu ID."""
        for item in self.itens:
            if item['Id'] == item_id:
                item.update({"Nome": nome, "Alcoólico": tipo, "Marca": marca, "Quantidade": quantidade})
                self._salvar_dados()
                return True
        return False

    def remover_item(self, item_id):
        """Remove um item da lista com base em seu ID."""
        self.itens = [item for item in self.itens if item['Id'] != item_id]
        self._salvar_dados()