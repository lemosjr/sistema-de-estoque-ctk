# arquivo: gerenciador.py

import json
import os

class GerenciadorUsuarios:
    """Gerencia a leitura e escrita de dados de usuários."""

    def __init__(self, filepath="usuarios.json"):
        self.filepath = filepath
        self.usuarios = self._carregar_dados()

    def _carregar_dados(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump({}, file)
            return {}
        with open(self.filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    def _salvar_dados(self):
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.usuarios, file, ensure_ascii=False, indent=4)

    def validar_credenciais(self, usuario, senha):
        return self.usuarios.get(usuario) == senha

    def adicionar_usuario(self, usuario, senha):
        if usuario in self.usuarios:
            return False  # Usuário já existe
        self.usuarios[usuario] = senha
        self._salvar_dados()
        return True

# A lógica do seu sistema de itens também se torna uma classe gerenciadora
class GerenciadorItens:
    """Gerencia a leitura e escrita de dados de itens."""

    def __init__(self, filepath="itens.json"):
        self.filepath = filepath
        self.itens = self._carregar_dados()
        if self.itens:
            # Garante que o novo ID será maior que o último ID existente
            self.item_id = max(item['Id'] for item in self.itens)
        else:
            self.item_id = 0

    def _carregar_dados(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as file:
            return json.load(file)

    def _salvar_dados(self):
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.itens, file, indent=4)

    def adicionar_item(self, nome, tipo, marca, quantidade):
        self.item_id += 1
        novo_item = {
            "Id": self.item_id, "Nome": nome, "Alcoólico": tipo,
            "Marca": marca, "Quantidade": quantidade
        }
        self.itens.append(novo_item)
        self._salvar_dados()
        return novo_item

    def atualizar_item(self, item_id, nome, tipo, marca, quantidade):
        for item in self.itens:
            if item['Id'] == item_id:
                item.update({"Nome": nome, "Alcoólico": tipo, "Marca": marca, "Quantidade": quantidade})
                self._salvar_dados()
                return True
        return False

    def remover_item(self, item_id):
        self.itens = [item for item in self.itens if item['Id'] != item_id]
        self._salvar_dados()