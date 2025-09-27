# main.py (versão corrigida e completa)

import customtkinter as ctk
from db_connection import get_db_connection 
from gerenciador import GerenciadorUsuarios, GerenciadorItens
# ADICIONADO: Importar as novas telas
from telas import TelaLogin, TelaCadastroUsuario, TelaPrincipal, TelaServicos, TelaFavoritaBebida, Tela_editar_perfil

class App:
    """Classe principal que gerencia o fluxo da aplicação."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.current_user = None
        
        db_conn = get_db_connection()
        if not db_conn:
            print("Não foi possível iniciar a aplicação. Verifique a conexão com o banco de dados.")
            return

        self.gerenciador_usuarios = GerenciadorUsuarios(db_conn)
        self.gerenciador_itens = GerenciadorItens(db_conn)

    def run(self):
        """Inicia a aplicação exibindo a tela de login."""
        self.mostrar_tela_login()

    def mostrar_tela_login(self):
        """Cria e exibe a tela de login."""
        tela_login = TelaLogin(self)
        tela_login.mainloop()

    def mostrar_tela_servico(self):
        """Cria e exibe a tela de serviços"""
        tela_servico = TelaServicos(self)
        tela_servico.mainloop()

    def mostrar_tela_cadastro_usuario(self):
        """Cria e exibe a tela de cadastro de usuário."""
        tela_cadastro = TelaCadastroUsuario(self)
        tela_cadastro.mainloop()

    def mostrar_tela_principal(self):
        """Cria e exibe a tela principal após o login bem-sucedido."""
        tela_principal = TelaPrincipal(self)
        tela_principal.mainloop()

    # ADICIONADO: Método para mostrar a tela de bebida favorita
    def mostrar_tela_bebida_favorita(self):
        tela_bebida = TelaFavoritaBebida(self)
        tela_bebida.mainloop()

    # ADICIONADO: Método para mostrar a tela de edição de perfil
    def mostrar_tela_editar_perfil(self):
        tela_perfil = Tela_editar_perfil(self)
        tela_perfil.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()