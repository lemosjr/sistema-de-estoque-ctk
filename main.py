# arquivo: main.py

import customtkinter as ctk
from gerenciador import GerenciadorUsuarios, GerenciadorItens
from telas import TelaLogin, TelaCadastroUsuario, TelaPrincipal

class App:
    """Classe principal que gerencia o fluxo da aplicação."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Inicializa os gerenciadores de dados UMA VEZ
        self.gerenciador_usuarios = GerenciadorUsuarios()
        self.gerenciador_itens = GerenciadorItens()

    def run(self):
        """Inicia a aplicação exibindo a tela de login."""
        self.mostrar_tela_login()

    def mostrar_tela_login(self):
        tela_login = TelaLogin(self)
        tela_login.mainloop()

    def mostrar_tela_cadastro_usuario(self):
        tela_cadastro = TelaCadastroUsuario(self)
        tela_cadastro.mainloop()

    def mostrar_tela_principal(self):
        """Ação a ser executada após o login bem-sucedido."""
        tela_principal = TelaPrincipal(self)
        tela_principal.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()