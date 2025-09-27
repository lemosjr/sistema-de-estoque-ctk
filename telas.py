import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
import os
import pyglet
import re
from PIL import Image, ImageDraw

# Carrega a fonte personalizada para ser usada na aplicação
FONT_PATH = "fonts/Quicksand-Light.ttf"
if os.path.exists(FONT_PATH):
    pyglet.font.add_file(FONT_PATH)
QUICKSAND_FONT_NAME = "Quicksand"

class BaseTela(ctk.CTk):
    """Classe base para todas as telas, configurando o tema e a fonte padrão."""
    def __init__(self, app, title, geometry):
        super().__init__()
        self.app = app
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.grad_frame = GradientFrame(self, color1=(60, 10, 10), color2=(26, 0, 0), fg_color="transparent")
        self.grad_frame.place(relwidth=1, relheight=1)
    
    def centralizar_janela(self):
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

class GradientFrame(ctk.CTkFrame):
    """Um frame que desenha um fundo com gradiente vertical."""
    def __init__(self, parent, color1, color2, **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.gradient_label = ctk.CTkLabel(self, text="")
        self.gradient_label.place(relwidth=1, relheight=1)
        self.bind("<Configure>", self._draw_gradient)
        self._gradient_image = None

    def _draw_gradient(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            return

        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        for y in range(height):
            r = int(self.color1[0] + (self.color2[0] - self.color1[0]) * y / height)
            g = int(self.color1[1] + (self.color2[1] - self.color1[1]) * y / height)
            b = int(self.color1[2] + (self.color2[2] - self.color1[2]) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        self._gradient_image = ctk.CTkImage(light_image=image, size=(width, height))
        self.gradient_label.configure(image=self._gradient_image)

class TelaLogin(BaseTela):
    """Define a interface gráfica e as funcionalidades da tela de login."""
    def __init__(self, app):
        super().__init__(app, "Tela de Login", "380x480")
        self._criar_widgets()
        self.centralizar_janela()

    def _criar_widgets(self):
        frame_central = ctk.CTkFrame(self.grad_frame, fg_color="transparent")
        frame_central.pack(expand=True, fill="both", padx=20, pady=20)

        imagem_path = "Logo_projeto_bebidas_png.png" 
        if os.path.exists(imagem_path):
            self.logo_image = ctk.CTkImage(light_image=Image.open(imagem_path), size=(100, 100))
            ctk.CTkLabel(frame_central, image=self.logo_image, text="").pack(pady=(10, 20))
        else:
            ctk.CTkLabel(frame_central, text="Imagem não encontrada", text_color="white").pack(pady=(10, 20))
        
        ctk.CTkLabel(frame_central, text="Usuário:", font=(QUICKSAND_FONT_NAME, 14)).pack(pady=(10, 5))
        self.entry_usuario = ctk.CTkEntry(frame_central, placeholder_text="Digite seu usuário:", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_usuario.pack(pady=5, padx=30, fill="x")

        ctk.CTkLabel(frame_central, text="Senha:", font=(QUICKSAND_FONT_NAME, 14)).pack(pady=(10, 5))
        self.entry_senha = ctk.CTkEntry(frame_central, placeholder_text="Senha:", show="*", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_senha.pack(pady=5, padx=30, fill="x")
        
        btn_entrar = ctk.CTkButton(frame_central, text="Entrar", fg_color="#ff7b00", text_color="white", command=self._executar_login, corner_radius=10, width=200)
        btn_entrar.pack(pady=20)

        frame_links = ctk.CTkFrame(frame_central, fg_color="transparent")
        frame_links.pack(pady=10)

        link_recuperar = ctk.CTkLabel(frame_links, text="Recuperar senha", text_color="#c2a999", cursor="hand2")
        link_recuperar.pack(side="left", padx=10)

        link_cadastrar = ctk.CTkLabel(frame_links, text="Cadastrar", text_color="#c2a999", cursor="hand2")
        link_cadastrar.pack(side="left", padx=10)
        link_cadastrar.bind("<Button-1>", lambda e: self._abrir_cadastro())

    def _executar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        if self.app.gerenciador_usuarios.validar_credenciais(usuario, senha):
            self.app.current_user = usuario 
            self.destroy()
            self.app.mostrar_tela_servico()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")

    def _abrir_cadastro(self, event=None):
        self.destroy()
        self.app.mostrar_tela_cadastro_usuario()

class TelaServicos(BaseTela):
    """Define a interface do menu de serviços da aplicação."""
    def __init__(self, app):
        super().__init__(app, "Tela de Serviços", "380x480")
        self._criar_widgets()
        self.centralizar_janela()

    def _criar_widgets(self):
        frame_central = ctk.CTkFrame(self.grad_frame, fg_color="transparent")
        frame_central.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame_central, text=f"Bem-vindo, {self.app.current_user}", font=(QUICKSAND_FONT_NAME, 16)).pack(pady=(10, 5))

        imagem_path = "Logo_projeto_bebidas_png.png" 
        if os.path.exists(imagem_path):
            self.logo_image = ctk.CTkImage(light_image=Image.open(imagem_path), size=(100, 100))
            ctk.CTkLabel(frame_central, image=self.logo_image, text="").pack(pady=(10, 20))
        else:
            ctk.CTkLabel(frame_central, text="Imagem não encontrada", text_color="white").pack(pady=(10, 20))
        
        btn_gerenciamento = ctk.CTkButton(frame_central, text="Gerenciamento",width=200, fg_color="#1f6aa5", text_color="white", command=self.tela_principal)
        btn_gerenciamento.pack(pady=10)
        
        btn_editar_perfil = ctk.CTkButton(frame_central, text="Editar Perfil",width=200, fg_color="#1f6aa5", text_color="white", command=self._abrir_editar_perfil)
        btn_editar_perfil.pack(pady=10)
        
        btn_favorita_bebida = ctk.CTkButton(frame_central, text="Favorita Bebida",width=200, fg_color="#1f6aa5", text_color="white", command=self._abrir_bebida_favorita)
        btn_favorita_bebida.pack(pady=10)
        
        btn_sair = ctk.CTkButton(frame_central, text="Sair", width=200, command=self._voltar_login, fg_color="#a83232")
        btn_sair.pack(pady=20)
    
    def tela_principal(self):
        self.destroy()
        self.app.mostrar_tela_principal()
        
    def _voltar_login(self):
        self.destroy()
        self.app.mostrar_tela_login()
    
    def _abrir_editar_perfil(self):
        self.destroy()
        self.app.mostrar_tela_editar_perfil()
        
    def _abrir_bebida_favorita(self):
        self.destroy()
        self.app.mostrar_tela_bebida_favorita()

class TelaErroConexao(BaseTela):
    """Tela exibida quando a conexão com o banco de dados falha."""
    def __init__(self, app):
        super().__init__(app, "Erro de Conexão", "400x200")
        ctk.CTkLabel(self.grad_frame, text="Não foi possível conectar ao banco de dados.", font=(QUICKSAND_FONT_NAME, 14), text_color="white").pack(pady=40)
        ctk.CTkButton(self.grad_frame, text="Fechar", command=self.destroy, fg_color="#a83232").pack(pady=20)
        self.centralizar_janela()

class TelaConexaoSucesso(BaseTela):
    """Tela exibida quando a conexão com o banco de dados é bem-sucedida."""
    def __init__(self, app):
        super().__init__(app, "Conexão Bem-Sucedida", "400x200")
        ctk.CTkLabel(self.grad_frame, text="Conexão com o banco de dados estabelecida com sucesso!", font=(QUICKSAND_FONT_NAME, 14), text_color="white").pack(pady=40)
        ctk.CTkButton(self.grad_frame, text="Continuar", command=self._continuar, fg_color="#1f6aa5").pack(pady=20)
        self.centralizar_janela()

    def _continuar(self):
        self.destroy()
        self.app.mostrar_tela_login()

class Tela_editar_perfil(BaseTela):
    """Define a interface para edição de perfil do usuário."""
    def __init__(self, app):
        super().__init__(app, "Editar Perfil", "550x550")
        self._criar_widgets()
        self._carregar_dados_usuario()
        self.centralizar_janela()

    def _criar_widgets(self):
        frame_principal = ctk.CTkFrame(self.grad_frame, fg_color="transparent")
        frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(frame_principal, text="Nome Completo:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=0, pady=10, sticky="w")
        self.entry_nome = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome completo", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_nome.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Email:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=1, column=0, pady=10, sticky="w")
        self.entry_email = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu email", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_email.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Usuário:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=2, column=0, pady=10, sticky="w")
        self.entry_usuario = ctk.CTkEntry(frame_principal, font=(QUICKSAND_FONT_NAME, 14))
        self.entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Nova Senha:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=3, column=0, pady=10, sticky="w")
        self.entry_nova_senha = ctk.CTkEntry(frame_principal, placeholder_text="Deixe em branco para não alterar", show="*", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_nova_senha.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
        
        ctk.CTkLabel(frame_principal, text="Confirmar Senha:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=4, column=0, pady=10, sticky="w")
        self.entry_confirmar_senha = ctk.CTkEntry(frame_principal, placeholder_text="Confirme a nova senha", show="*", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_confirmar_senha.grid(row=4, column=1, pady=10, padx=10, sticky="ew")
        
        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=30)
        
        ctk.CTkButton(frame_botoes, text="Salvar Alterações", command=self._executar_salvar).pack(side="left", padx=10)
        ctk.CTkButton(frame_botoes, text="Voltar", command=self._voltar_servicos, fg_color="#a83232").pack(side="left", padx=10)

        frame_principal.grid_columnconfigure(1, weight=1)

    def _carregar_dados_usuario(self):
        usuario_logado = self.app.current_user
        if not usuario_logado:
            messagebox.showerror("Erro", "Não foi possível identificar o usuário logado.")
            self._voltar_servicos()
            return
            
        dados = self.app.gerenciador_usuarios.obter_dados_usuario(usuario_logado)
        if dados:
            self.entry_nome.insert(0, dados['nome'])
            self.entry_email.insert(0, dados['email'])
            self.entry_usuario.insert(0, usuario_logado)
            self.entry_usuario.configure(state="readonly") 
        else:
            messagebox.showerror("Erro", f"Não foi possível encontrar os dados do usuário '{usuario_logado}'.")

    def _executar_salvar(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        nova_senha = self.entry_nova_senha.get()
        confirmar_senha = self.entry_confirmar_senha.get()

        if not nome or not email:
            messagebox.showerror("Erro", "Nome e E-mail são campos obrigatórios.")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erro de Cadastro", "Por favor, insira um formato de e-mail válido.")
            return
        if nova_senha:
            if len(nova_senha) < 6:
                messagebox.showerror("Erro", "A nova senha deve ter pelo menos 6 caracteres.")
                return
            if nova_senha != confirmar_senha:
                messagebox.showerror("Erro", "As senhas não coincidem.")
                return
        
        resultado = self.app.gerenciador_usuarios.editar_usuario(
            self.app.current_user, nome, email, nova_senha if nova_senha else None
        )

        if resultado == "sucesso":
            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")
            self._voltar_servicos()
        elif resultado == "email_em_uso":
            messagebox.showerror("Erro", "O e-mail informado já está em uso por outra conta.")
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar o perfil.")

    def _voltar_servicos(self):
        self.destroy()
        self.app.mostrar_tela_servico()

class TelaFavoritaBebida(BaseTela):
    """Define a interface para o usuário salvar sua bebida favorita."""
    def __init__(self, app):
        super().__init__(app, "Bebida Favorita", "550x450")
        self._criar_widgets()
        self.centralizar_janela()

    def _criar_widgets(self):
        frame_principal = ctk.CTkFrame(self.grad_frame, fg_color="transparent")
        frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(frame_principal, text="Selecione sua bebida favorita:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=0, pady=10, sticky="w")
        self.entry_bebida = ctk.CTkEntry(frame_principal, placeholder_text="Digite o nome da bebida", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_bebida.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.grid(row=1, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(frame_botoes, text="Salvar", font=(QUICKSAND_FONT_NAME, 14), command=self._salvar_bebida).grid(row=0, column=0, padx=20)
        ctk.CTkButton(frame_botoes, text="Voltar", font=(QUICKSAND_FONT_NAME, 14), fg_color="#a83232", command=self._voltar_servicos, hover_color="#F24B88").grid(row=0, column=1, padx=20)

        frame_principal.grid_columnconfigure(1, weight=1)

    def _salvar_bebida(self):
        bebida = self.entry_bebida.get()
        if bebida:
            if self.app.current_user:
                self.app.gerenciador_itens.favoritar_bebida(self.app.current_user, bebida)
                messagebox.showinfo("Sucesso", f"Sua bebida favorita '{bebida}' foi salva!")
                self._voltar_servicos()
            else:
                messagebox.showerror("Erro", "Nenhum usuário logado para salvar a preferência.")
        else:
            messagebox.showwarning("Aviso", "Por favor, digite o nome de uma bebida.")

    def _voltar_servicos(self):
        self.destroy()
        self.app.mostrar_tela_servico()

class TelaCadastroUsuario(BaseTela):
    """Define a interface gráfica para cadastro de novos usuários."""
    def __init__(self, app):
        super().__init__(app, "Tela de Cadastro", "550x450")
        self._criar_widgets()
        self.centralizar_janela()

    def _criar_widgets(self):
        frame_principal = ctk.CTkFrame(self.grad_frame, fg_color="transparent")
        frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(frame_principal, text="Nome Completo:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=0, pady=10, sticky="w")
        self.entry_nome = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome completo", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_nome.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Email:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=1, column=0, pady=10, sticky="w")
        self.entry_email = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu email", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_email.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Usuário:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=2, column=0, pady=10, sticky="w")
        self.entry_usuario = ctk.CTkEntry(frame_principal, placeholder_text="Crie um nome de usuário", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Senha:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=3, column=0, pady=10, sticky="w")
        self.entry_senha = ctk.CTkEntry(frame_principal, placeholder_text="Crie uma senha", show="*", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_senha.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(frame_botoes, text="Cadastrar", font=(QUICKSAND_FONT_NAME, 14), command=self._executar_cadastro).grid(row=0, column=0, padx=20)
        ctk.CTkButton(frame_botoes, text="Voltar", font=(QUICKSAND_FONT_NAME, 14), fg_color="#a83232", command=self._voltar_login, hover_color="#F24B88").grid(row=0, column=1, padx=20)

        frame_principal.grid_columnconfigure(1, weight=1)

    def _executar_cadastro(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erro de Cadastro", "Por favor, insira um formato de e-mail válido.")
            return
        if len(senha) < 6:
            messagebox.showerror("Erro de Cadastro", "A senha deve ter pelo menos 6 caracteres.")
            return
        if not all([nome, email, usuario, senha]):
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios!")
            return
        
        if self.app.gerenciador_usuarios.adicionar_usuario(usuario, senha, nome, email):
            messagebox.showinfo("Sucesso", f"Usuário '{usuario}' cadastrado com sucesso!")
            self._voltar_login()
        else:
            messagebox.showerror("Erro de Cadastro", "Este nome de usuário ou e-mail já está em uso!")
            
    def _voltar_login(self):
        self.destroy()
        self.app.mostrar_tela_login()

class TelaPrincipal(BaseTela):
    """Define a interface principal para gerenciamento de itens (CRUD)."""
    def __init__(self, app):
        super().__init__(app, "Tela Principal", "1280x720")
        self.gerenciador_itens = app.gerenciador_itens
        self.selected_item_id_to_edit = None
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self.popular_tabela()
        self.centralizar_janela()

    def popular_tabela(self, itens=None):
        """Preenche a tabela com os dados de itens."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        lista_para_exibir = itens if itens is not None else self.gerenciador_itens.listar_itens()
        
        for item in lista_para_exibir:
            self.tree.insert('', 'end', values=tuple(item.values()))

    def _executar_pesquisa(self):
        """Filtra os itens da tabela com base no termo de pesquisa."""
        termo_pesquisa = self.entry_pesquisa.get()
        if not termo_pesquisa:
            self.popular_tabela()
            return
        
        resultado = self.gerenciador_itens.buscar_item(termo_pesquisa)
        self.popular_tabela(resultado)

    def _limpar_pesquisa(self):
        """Limpa o campo de pesquisa e recarrega todos os itens."""
        self.entry_pesquisa.delete(0, tk.END)
        self.popular_tabela()

    def _create_widgets(self):
        """Cria e organiza todos os widgets da tela principal."""
        self._style_treeview()
        self._create_input_frame()
        self._create_list_frame()

    def _style_treeview(self):
        """Aplica um estilo visual à tabela de itens (Treeview)."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#242424", foreground="#ffffff", fieldbackground="#242424", borderwidth=0, font=(QUICKSAND_FONT_NAME, 11), rowheight=25)
        style.map('Treeview', background=[('selected', "#1f6aa5")])
        style.configure("Treeview.Heading", background="#565b5e", foreground="#ffffff", font=(QUICKSAND_FONT_NAME, 12, 'bold'), relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def _create_input_frame(self):
        """Cria o painel de entrada de dados para os itens."""
        frame_data_items = ctk.CTkFrame(self.grad_frame, corner_radius=10, fg_color="transparent")
        frame_data_items.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        
        ctk.CTkLabel(frame_data_items, text="Nome do item:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.entry_item = ctk.CTkEntry(frame_data_items, width=220, font=(QUICKSAND_FONT_NAME, 14))
        self.entry_item.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(frame_data_items, text="Alcoólico (sim/nao):", font=(QUICKSAND_FONT_NAME, 14)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.entry_tipo = ctk.CTkEntry(frame_data_items, width=220, font=(QUICKSAND_FONT_NAME, 14))
        self.entry_tipo.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_data_items, text="Marca:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.entry_marca = ctk.CTkEntry(frame_data_items, width=220, font=(QUICKSAND_FONT_NAME, 14))
        self.entry_marca.grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(frame_data_items, text="Quantidade:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.entry_quantidade = ctk.CTkEntry(frame_data_items, width=220, font=(QUICKSAND_FONT_NAME, 14))
        self.entry_quantidade.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_data_items, text="Valor:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.entry_valor = ctk.CTkEntry(frame_data_items, width=220, font=(QUICKSAND_FONT_NAME, 14))
        self.entry_valor.grid(row=5, column=1, padx=10, pady=5)
        
        frame_button = ctk.CTkFrame(frame_data_items, fg_color="transparent")
        frame_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        frame_button.grid_columnconfigure((0, 1), weight=1)

        self.btn_salvar = ctk.CTkButton(frame_button, text="Salvar Item", command=self.register_item, fg_color="#ff7b00", font=(QUICKSAND_FONT_NAME, 14))
        self.btn_salvar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        ctk.CTkButton(frame_button, text="Limpar", command=self.clear_fields, fg_color="#D35B58", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkButton(frame_data_items, text="Sair", command=self.destroy, fg_color="#271F1F", font=(QUICKSAND_FONT_NAME, 14)).grid(row=8, column=0, columnspan=2, padx=10, pady=(20, 0), sticky="ew")
    
    def _create_list_frame(self):
        """Cria o painel que exibe a lista de itens e a funcionalidade de busca."""
        frame_registered_items = ctk.CTkFrame(self.grad_frame, corner_radius=10, fg_color="transparent")
        frame_registered_items.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        frame_registered_items.grid_columnconfigure(0, weight=1)
        frame_registered_items.grid_rowconfigure(1, weight=1)
        
        frame_pesquisa = ctk.CTkFrame(frame_registered_items, fg_color="transparent")
        frame_pesquisa.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        frame_pesquisa.grid_columnconfigure(0, weight=1)

        self.entry_pesquisa = ctk.CTkEntry(frame_pesquisa, placeholder_text="Pesquisar por nome, marca, etc...", font=(QUICKSAND_FONT_NAME, 12))
        self.entry_pesquisa.grid(row=0, column=0, padx=(0,5), pady=5, sticky="ew")
        
        ctk.CTkButton(frame_pesquisa, text="Pesquisar", width=100, command=self._executar_pesquisa, font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(frame_pesquisa, text="Limpar", width=100, command=self._limpar_pesquisa, font=(QUICKSAND_FONT_NAME, 14), fg_color="#565b5e").grid(row=0, column=2, padx=(0,5), pady=5)

        self.tree = ttk.Treeview(frame_registered_items, columns=('Id', 'Nome', 'Alcoólico', 'Marca', 'Quantidade', 'Valor'), show="headings")
        self.tree.heading('Id', text='Id'); self.tree.heading('Nome', text='Nome'); self.tree.heading('Alcoólico', text='Alcoólico'); self.tree.heading('Marca', text='Marca'); self.tree.heading('Quantidade', text='Quantidade'); self.tree.heading('Valor', text='Valor')
        
        self.tree.column("Id", width=50, anchor="center"); self.tree.column("Nome", width=200); self.tree.column("Alcoólico", width=100, anchor="center"); self.tree.column("Marca", width=150); self.tree.column("Quantidade", width=100, anchor="center"); self.tree.column("Valor", width=100, anchor="center")
        
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        scrollbar = ctk.CTkScrollbar(frame_registered_items, orientation="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        frame_botoes_lista = ctk.CTkFrame(frame_registered_items, fg_color="transparent")
        frame_botoes_lista.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkButton(frame_botoes_lista, text="Editar Selecionado", command=self.edit_item, font=(QUICKSAND_FONT_NAME, 14)).pack(side="left")
        ctk.CTkButton(frame_botoes_lista, text="Remover Selecionado", command=self.remove_selected_item, fg_color="#D35B58", font=(QUICKSAND_FONT_NAME, 14)).pack(side="right")

    def register_item(self):
        """Salva um novo item ou atualiza um item existente no banco de dados."""
        nome = self.entry_item.get()
        tipo = self.entry_tipo.get().lower()
        marca = self.entry_marca.get()
        quantidade_str = self.entry_quantidade.get()
        valor_str = self.entry_valor.get()
        
        if not all([nome, tipo, marca, quantidade_str, valor_str]):
            messagebox.showerror("Erro de Cadastro", "Todos os campos devem ser preenchidos.")
            return

        if tipo not in ["sim", "nao"]:
            messagebox.showerror("Erro de Validação", "O campo 'Alcoólico' deve ser preenchido com 'sim' ou 'nao'.")
            return

        try:
            quantidade = int(quantidade_str)
            valor = float(valor_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro de Validação", "Os campos 'Quantidade' e 'Valor' devem ser números.")
            return

        if self.selected_item_id_to_edit is not None:
            self.gerenciador_itens.atualizar_item(self.selected_item_id_to_edit, nome, tipo, marca, quantidade, valor)
            messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
        else:
            self.gerenciador_itens.adicionar_item(nome, tipo, marca, quantidade, valor)
            messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")
        
        self.popular_tabela()
        self.clear_fields()

    def remove_selected_item(self):
        """Remove o item que está selecionado na tabela."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum item foi selecionado para remoção.")
            return

        if messagebox.askyesno("Confirmar Remoção", "Você tem certeza que deseja remover o item selecionado?"):
            item_id_to_remove = int(self.tree.item(selected_item, 'values')[0])
            
            if self.gerenciador_itens.remover_item(item_id_to_remove):
                self.popular_tabela()
                messagebox.showinfo("Sucesso", "Item removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível encontrar o item para remover.")

    def edit_item(self):
        """Carrega os dados de um item selecionado para os campos de edição."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum item foi selecionado para edição.")
            return

        item_data = self.tree.item(selected_item, 'values')
        self.selected_item_id_to_edit = int(item_data[0])
        
        self.clear_fields(clear_id=False)
        self.entry_item.insert(0, item_data[1])
        self.entry_tipo.insert(0, item_data[2])
        self.entry_marca.insert(0, item_data[3])
        self.entry_quantidade.insert(0, item_data[4])
        self.entry_valor.insert(0, item_data[5])
        self.btn_salvar.configure(text="Atualizar Item")
        
    def clear_fields(self, clear_id=True):
        """Limpa os campos de entrada do formulário de itens."""
        self.entry_item.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        if clear_id:
            self.selected_item_id_to_edit = None
            self.btn_salvar.configure(text="Salvar Item")