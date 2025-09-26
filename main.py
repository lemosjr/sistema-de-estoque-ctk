# main.py
import customtkinter as ctk
# Importe a função de conexão
from db_connection import get_db_connection 
from gerenciador import GerenciadorUsuarios, GerenciadorItens
from telas import TelaLogin, TelaCadastroUsuario, TelaPrincipal, TelaServicos

class App:
    """Classe principal que gerencia o fluxo da aplicação."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        # 1. Crie a conexão com o banco de dados
        db_conn = get_db_connection()
        if not db_conn:
            print("Não foi possível iniciar a aplicação. Verifique a conexão com o banco de dados.")
            # Opcional: mostrar uma janela de erro e fechar o app
            return

        # 2. Passe a conexão para os gerenciadores
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
        tela_serviço = TelaServicos(self)
        tela_serviço.mainloop()

    def mostrar_tela_cadastro_usuario(self):
        """Cria e exibe a tela de cadastro de usuário."""
        tela_cadastro = TelaCadastroUsuario(self)
        tela_cadastro.mainloop()

    def mostrar_tela_principal(self):
        """Cria e exibe a tela principal após o login bem-sucedido."""
        tela_principal = TelaPrincipal(self)
        tela_principal.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()