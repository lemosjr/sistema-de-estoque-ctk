import customtkinter as ctk
from tkinter import ttk, messagebox, PhotoImage
import tkinter as tk
import os
import pyglet
from PIL import Image

# Carrega a fonte personalizada para ser usada na aplicação.
FONT_PATH = "fonts/Quicksand-Light.ttf"
if os.path.exists(FONT_PATH):
    pyglet.font.add_file(FONT_PATH)
QUICKSAND_FONT_NAME = "Quicksand"

# --- Componente de Fundo com Gradiente ---
class GradientFrame(ctk.CTkFrame):
    """Um Frame que desenha um fundo com gradiente de forma eficiente."""
    def __init__(self, parent, color1, color2, **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self._canvas = tk.Canvas(self, highlightthickness=0)
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        """Desenha o gradiente como uma imagem de fundo, otimizado para performance."""
        self._canvas.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Cria uma imagem vertical de 1px de largura que será esticada
        self._gradient_image = PhotoImage(width=1, height=height)

        (r1, g1, b1) = self.winfo_rgb(self.color1)
        (r2, g2, b2) = self.winfo_rgb(self.color2)
        r_ratio = (r2 - r1) / height
        g_ratio = (g2 - g1) / height
        b_ratio = (b2 - b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr:04x}{ng:04x}{nb:04x}"
            self._gradient_image.put(color, (0, i))
        
        # Amplia a imagem para a largura total do widget
        self._bg_image = self._gradient_image.zoom(width, 1)
        
        self._canvas.create_image(0, 0, anchor="nw", image=self._bg_image, tags="gradient")

# --- Tela de Login ---
class TelaLogin(ctk.CTk):
    """Define a interface gráfica e as funcionalidades da tela de login."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Login")
        self.resizable(False, False)

        grad_frame = GradientFrame(self, color1="#3c0a0a", color2="#1a0000", fg_color="transparent")
        grad_frame.place(relwidth=1, relheight=1)
        
        self._criar_widgets()
        self.centralizar_janela()

    def centralizar_janela(self):
        """Centraliza a janela na tela do usuário."""
        self.update()  # <-- Correção: Usando update() para forçar o desenho da janela
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def _criar_widgets(self):
        """Cria e posiciona os widgets na tela de login."""
        frame_central = ctk.CTkFrame(self, fg_color="transparent")
        frame_central.pack(expand=True, fill="both", padx=20, pady=20)

        imagem_path = "Logo_projeto_bebidas_png.png"  
        if os.path.exists(imagem_path):
            self.logo_image = ctk.CTkImage(light_image=Image.open(imagem_path), size=(100, 100))
            ctk.CTkLabel(frame_central, image=self.logo_image, text="").pack(pady=(10, 20))
        else:
            ctk.CTkLabel(frame_central, text="Imagem não encontrada", text_color="white").pack(pady=(10, 20))
        
        # Campo Usuário
        ctk.CTkLabel(frame_central, text="Usuário:", font=(QUICKSAND_FONT_NAME, 14)).pack(pady=(10, 5))
        self.entry_usuario = ctk.CTkEntry(frame_central, placeholder_text="Digite seu usuário:", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_usuario.pack(pady=5, padx=30, fill="x")

        # Campo Senha
        ctk.CTkLabel(frame_central, text="Senha:", font=(QUICKSAND_FONT_NAME, 14)).pack(pady=(10, 5))
        self.entry_senha = ctk.CTkEntry(frame_central, placeholder_text="Senha:", show="*", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_senha.pack(pady=5, padx=30, fill="x")
        
        # Botão Entrar
        btn_entrar = ctk.CTkButton(frame_central, text="Entrar", fg_color="#ff7b00", text_color="white", command=self._executar_login, corner_radius=10, width=200)
        btn_entrar.pack(pady=20)

        frame_links = ctk.CTkFrame(frame_central, fg_color="transparent")
        frame_links.pack(pady=10)

        link_recuperar = ctk.CTkLabel(frame_links, text="Recuperar senha", text_color="#c2a999", cursor="hand2")
        link_recuperar.pack(side="left", padx=10)
        # link_recuperar.bind("<Button-1>", lambda e: self.app.mostrar_tela_recuperar_senha())

        link_cadastrar = ctk.CTkLabel(frame_links, text="Cadastrar", text_color="#c2a999", cursor="hand2")
        link_cadastrar.pack(side="left", padx=10)
        link_cadastrar.bind("<Button-1>", lambda e: self._abrir_cadastro())


    def _executar_login(self):
        """Valida as credenciais do usuário para permitir o acesso."""
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        if self.app.gerenciador_usuarios.validar_credenciais(usuario, senha):
            self.destroy()
            self.app.mostrar_tela_principal()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos.")

    def _abrir_cadastro(self, event=None):
        """Abre a tela de cadastro de usuário."""
        self.destroy()
        self.app.mostrar_tela_cadastro_usuario()

# --- Tela de Cadastro de Usuário ---
class TelaCadastroUsuario(ctk.CTk):
    """Define a interface gráfica e as funcionalidades da tela de cadastro."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Cadastro")
        self.geometry("550x450")
        self.resizable(False, False)

        grad_frame = GradientFrame(self, color1="#3c0a0a", color2="#1a0000", fg_color="transparent")
        grad_frame.place(relwidth=1, relheight=1)

        self._criar_widgets()
        self.centralizar_janela()

    def centralizar_janela(self):
        """Centraliza a janela na tela do usuário."""
        self.update()  # <-- Correção: Usando update() para forçar o desenho da janela
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")


    def _criar_widgets(self):
        """Cria e posiciona os widgets na tela de cadastro."""
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
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
        """Registra um novo usuário com os dados informados."""
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if not all([nome, email, usuario, senha]):
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios!")
            return
        
        if self.app.gerenciador_usuarios.adicionar_usuario(usuario, senha):
            messagebox.showinfo("Sucesso", f"Usuário '{usuario}' cadastrado com sucesso!")
            self._voltar_login()
        else:
            messagebox.showerror("Erro de Cadastro", "Este nome de usuário já está em uso!")

    def _voltar_login(self):
        """Retorna para a tela de login."""
        self.destroy()
        self.app.mostrar_tela_login()

# --- Tela Principal de Gerenciamento ---
class TelaPrincipal(ctk.CTk):
    """Define a interface principal para gerenciamento de itens."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.gerenciador_itens = app.gerenciador_itens
        self.selected_item_id_to_edit = None
        
        self.title("Gerenciador de Itens")
        self.geometry("1280x720")
        
        grad_frame = GradientFrame(self, color1="#3c0a0a", color2="#1a0000", fg_color="transparent")
        grad_frame.place(relwidth=1, relheight=1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self.popular_tabela()
        self.centralizar_janela()
    
    def centralizar_janela(self):
        """Centraliza a janela na tela do usuário."""
        self.update()  # <-- Correção: Usando update() para forçar o desenho da janela
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")


    def popular_tabela(self, itens=None):
        """Preenche a tabela com os dados de itens existentes."""
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
        """Cria todos os widgets da tela principal."""
        self._style_treeview()
        self._create_input_frame()
        self._create_list_frame()

    def _style_treeview(self):
        """Aplica um estilo visual à tabela de itens."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#242424", foreground="#ffffff", fieldbackground="#242424", borderwidth=0, font=(QUICKSAND_FONT_NAME, 11), rowheight=25)
        style.map('Treeview', background=[('selected', "#1f6aa5")])
        style.configure("Treeview.Heading", background="#565b5e", foreground="#ffffff", font=(QUICKSAND_FONT_NAME, 12, 'bold'), relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def _create_input_frame(self):
        """Cria o painel de entrada de dados para os itens."""
        frame_data_items = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
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

        ctk.CTkLabel(frame_data_items, text="Preço:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=5, column=0, padx=10, pady=5, sticky='w')
        self.entry_quantidade = ctk.CTkEntry(frame_data_items, width=220, font=(QUICKSAND_FONT_NAME, 14))
        self.entry_quantidade.grid(row=5, column=1, padx=10, pady=5)
        
        frame_button = ctk.CTkFrame(frame_data_items, fg_color="transparent")
        frame_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        frame_button.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(frame_button, text="Salvar Item", command=self.register_item, fg_color="#ff7b00", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(frame_button, text="Limpar", command=self.clear_fields, fg_color="#D35B58", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkButton(frame_data_items, text="Sair", command=self.destroy, fg_color="#271F1F", font=(QUICKSAND_FONT_NAME, 14)).grid(row=8, column=0, columnspan=2, padx=10, pady=(20, 0), sticky="ew")
    
    def _create_list_frame(self):
        """Cria o painel que exibe a lista de itens cadastrados."""
        frame_registered_items = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
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

        self.tree = ttk.Treeview(frame_registered_items, columns=('Id', 'Nome', 'Alcoólico', 'Marca', 'Quantidade', 'Preço'), show="headings")
        self.tree.heading('Id', text='Id'); self.tree.heading('Nome', text='Nome'); self.tree.heading('Alcoólico', text='Alcoólico'); self.tree.heading('Marca', text='Marca'); self.tree.heading('Quantidade', text='Quantidade'); self.tree.heading('Preço', text='preço')
        
        self.tree.column("Id", width=50, anchor="center"); self.tree.column("Nome", width=200); self.tree.column("Alcoólico", width=100, anchor="center"); self.tree.column("Marca", width=150); self.tree.column("Quantidade", width=100, anchor="center");self.tree.column("Preço", width=100, anchor="center")
        
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(frame_registered_items, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        frame_botoes_lista = ctk.CTkFrame(frame_registered_items, fg_color="transparent")
        frame_botoes_lista.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkButton(frame_botoes_lista, text="Editar Selecionado", command=self.edit_item, font=(QUICKSAND_FONT_NAME, 14)).pack(side="left")
        ctk.CTkButton(frame_botoes_lista, text="Remover Selecionado", command=self.remove_selected_item, fg_color="#D35B58", font=(QUICKSAND_FONT_NAME, 14)).pack(side="right")

    def register_item(self):
        """Salva um novo item ou atualiza um item existente."""
        nome = self.entry_item.get(); tipo = self.entry_tipo.get().lower(); marca = self.entry_marca.get(); quantidade_str = self.entry_quantidade.get()
        
        if not all([nome, tipo, marca, quantidade_str]):
            messagebox.showerror("Erro de Cadastro", "Todos os campos devem ser preenchidos.")
            return

        if tipo not in ["sim", "nao"]:
            messagebox.showerror("Erro de Validação", "O campo 'Alcoólico' deve ser preenchido com 'sim' ou 'nao'.")
            return

        try:
            quantidade = int(quantidade_str)
        except ValueError:
            messagebox.showerror("Erro de Validação", "O campo 'Quantidade' deve ser um número inteiro.")
            return

        if self.selected_item_id_to_edit is not None:
            self.gerenciador_itens.atualizar_item(self.selected_item_id_to_edit, nome, tipo, marca, quantidade)
            messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
        else:
            self.gerenciador_itens.adicionar_item(nome, tipo, marca, quantidade)
            messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")
        
        self.popular_tabela()
        self.clear_fields()

    def remove_selected_item(self):
        """Remove o item selecionado na tabela."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum item foi selecionado para remoção.")
            return
        
        if messagebox.askyesno("Confirmar Remoção", "Você tem certeza que deseja remover o item selecionado?"):
            item_id_to_remove = int(self.tree.item(selected_item, 'values')[0])
            self.gerenciador_itens.remover_item(item_id_to_remove)
            self.popular_tabela()
            messagebox.showinfo("Sucesso", "Item removido com sucesso!")

    def edit_item(self):
        """Carrega os dados de um item selecionado para edição."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum item foi selecionado para edição.")
            return

        item_data = self.tree.item(selected_item, 'values')
        self.selected_item_id_to_edit = int(item_data[0])
        
        self.clear_fields(clear_id=False)
        self.entry_item.insert(0, item_data[1]); self.entry_tipo.insert(0, item_data[2]); self.entry_marca.insert(0, item_data[3]); self.entry_quantidade.insert(0, item_data[4])
        
    def clear_fields(self, clear_id=True):
        """Limpa os campos de entrada do formulário."""
        self.entry_item.delete(0, tk.END); self.entry_tipo.delete(0, tk.END); self.entry_marca.delete(0, tk.END); self.entry_quantidade.delete(0, tk.END)
        if clear_id:
            self.selected_item_id_to_edit = None