import customtkinter as ctk
from db_connection import get_db_connection 
from gerenciador import GerenciadorUsuarios, GerenciadorItens
from telas import TelaLogin, TelaCadastroUsuario, TelaPrincipal, TelaServicos, TelaFavoritaBebida, Tela_editar_perfil

class App:
    """
    Classe principal que gerencia o estado e o fluxo de navegação da aplicação.
    """

    def __init__(self):
        """Inicializa a aplicação, configura o tema e estabelece a conexão com o banco de dados."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Armazena o nome de usuário logado na sessão atual.
        self.current_user = None
        
        # Estabelece a conexão com o banco de dados e inicializa os gerenciadores.
        db_conn = get_db_connection()
        if not db_conn:
            print("Não foi possível iniciar a aplicação. Verifique a conexão com o banco de dados.")
            # Idealmente, aqui seria exibida uma tela de erro.
            return

        self.gerenciador_usuarios = GerenciadorUsuarios(db_conn)
        self.gerenciador_itens = GerenciadorItens(db_conn)

    def run(self):
        """Inicia o loop principal da aplicação, começando pela tela de login."""
        self.mostrar_tela_login()

    def mostrar_tela_login(self):
        """Cria e exibe a tela de login."""
        tela_login = TelaLogin(self)
        tela_login.mainloop()

    def mostrar_tela_servico(self):
        """Cria e exibe a tela de serviços."""
        tela_servico = TelaServicos(self)
        tela_servico.mainloop()

    def mostrar_tela_cadastro_usuario(self):
        """Cria e exibe a tela de cadastro de usuário."""
        tela_cadastro = TelaCadastroUsuario(self)
        tela_cadastro.mainloop()

    def mostrar_tela_principal(self):
        """Cria e exibe a tela principal de gerenciamento."""
        tela_principal = TelaPrincipal(self)
        tela_principal.mainloop()

    def mostrar_tela_bebida_favorita(self):
        """Cria e exibe a tela para escolher a bebida favorita."""
        tela_bebida = TelaFavoritaBebida(self)
        tela_bebida.mainloop()

    def mostrar_tela_editar_perfil(self):
        """Cria e exibe a tela de edição de perfil."""
        tela_perfil = Tela_editar_perfil(self)
        tela_perfil.mainloop()

# Ponto de entrada da aplicação.
if __name__ == "__main__":
    app = App()
    app.run()