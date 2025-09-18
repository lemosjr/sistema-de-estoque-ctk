import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
import os
import pyglet
from tkinter import PhotoImage

# Carrega a fonte personalizada para ser usada na aplicação.
FONT_PATH = "fonts/Quicksand-Light.ttf"
if os.path.exists(FONT_PATH):
    pyglet.font.add_file(FONT_PATH)
QUICKSAND_FONT_NAME = "Quicksand"

# --- Gradiente da tela ---
class GradientFrame(ctk.CTkFrame):
    """Um Frame que desenha um fundo com gradiente de forma eficiente."""
    def __init__(self, parent, color1, color2, **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self._canvas = tk.Canvas(self, highlightthickness=0)
        self._canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # O bind faz o gradiente ser redesenhado se a janela mudar de tamanho
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        """Desenha o gradiente como uma imagem de fundo."""
        self._canvas.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Cria a imagem de 1px de largura
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
        
        # Amplia a imagem para a largura total da janela
        self._bg_image = self._gradient_image.zoom(width)
        
        self._canvas.create_image(0, 0, anchor="nw", image=self._bg_image, tags="gradient")
# --- Tela de Login ---
class TelaLogin(ctk.CTk):
    """Define a interface gráfica e as funcionalidades da tela de login."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Login")
        self.geometry("450x350")       
        grad_frame = GradientFrame(self, color1="#3c0a0a", color2="#1a0000", fg_color="transparent")
        grad_frame.place(relwidth=1, relheight=1)
        self._criar_widgets()

    def _criar_widgets(self):
        """Cria e posiciona os widgets na tela de login."""
        ctk.CTkLabel(self, text="Usuário:", font=(QUICKSAND_FONT_NAME, 14)).pack(pady=(20, 5))
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Digite seu usuário:", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_usuario.pack(pady=5)

        ctk.CTkLabel(self, text="Senha:", font=(QUICKSAND_FONT_NAME, 14)).pack(pady=(20, 5))
        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha:", show="*", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_senha.pack(pady=5)
        
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(pady=20)

        ctk.CTkButton(frame_botoes, text="Entrar", command=self._executar_login, fg_color="#ff7b00", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botoes, text="Cancelar", command=self.destroy, fg_color="#a83232", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=1, padx=10)
        ctk.CTkButton(self, text="Cadastro", width=10, command=self._abrir_cadastro, fg_color="#007acc", font=(QUICKSAND_FONT_NAME, 14)).place(x=380, y=300)

    def _executar_login(self):
        """Valida as credenciais do usuário para permitir o acesso."""
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        if self.app.gerenciador_usuarios.validar_credenciais(usuario, senha):
            self.destroy()
            self.app.mostrar_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def _abrir_cadastro(self):
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
        self.geometry("550x600")      
        grad_frame = GradientFrame(self, color1="#3c0a0a", color2="#1a0000", fg_color="transparent")
        grad_frame.place(relwidth=1, relheight=1)
        self._criar_widgets()

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
        self.entry_usuario = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome de usuário", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Senha:", font=(QUICKSAND_FONT_NAME, 14)).grid(row=3, column=0, pady=10, sticky="w")
        self.entry_senha = ctk.CTkEntry(frame_principal, placeholder_text="Digite sua senha", show="*", font=(QUICKSAND_FONT_NAME, 14))
        self.entry_senha.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(frame_botoes, text="Cadastrar", font=(QUICKSAND_FONT_NAME, 14), command=self._executar_cadastro, width=20).grid(row=0, column=0, padx=20)
        ctk.CTkButton(frame_botoes, text="Cancelar", font=(QUICKSAND_FONT_NAME, 14), fg_color="#a83232", command=self._voltar_login, hover_color="#F24B88", width=20).grid(row=0, column=1, padx=20)

        frame_principal.grid_columnconfigure(1, weight=1)

    def _executar_cadastro(self):
        """Registra um novo usuário com os dados informados."""
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if not all([nome, email, usuario, senha]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        if self.app.gerenciador_usuarios.adicionar_usuario(usuario, senha):
            messagebox.showinfo("Sucesso", f"Cadastro de {nome} realizado com sucesso!")
            self._voltar_login()
        else:
            messagebox.showerror("Erro", "Usuário já cadastrado!")

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
        
        self.title("Cadastro de Itens")
        self.geometry("1280x720")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        grad_frame = GradientFrame(self, color1="#3c0a0a", color2="#1a0000", fg_color="transparent")
        grad_frame.place(relwidth=1, relheight=1)
        
        self._create_widgets()
        self.popular_tabela()

    def popular_tabela(self, itens=None):
        """Preenche a tabela com os dados de itens existentes."""
        # Limpa a visualização atual da tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Se nenhuma lista de itens for fornecida, busca a lista completa
        lista_para_exibir = itens if itens is not None else self.gerenciador_itens.listar_itens()
        
        for item in lista_para_exibir:
            self.tree.insert('', 'end', values=tuple(item.values()))

    def _executar_pesquisa(self):
        """Filtra os itens da tabela com base no termo de pesquisa."""
        termo_pesquisa = self.entry_pesquisa.get().lower()
        if not termo_pesquisa:
            self.popular_tabela()
            return
        
        # Filtra os itens
        itens_completos = self.gerenciador_itens.listar_itens()
        resultado = []
        for item in itens_completos:
            # Converte todos os valores do item para string e minúsculas para a busca
            valores_item = [str(v).lower() for v in item.values()]
            if any(termo_pesquisa in valor for valor in valores_item):
                resultado.append(item)
        
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
        style.configure("Treeview", background="#242424", foreground="#ffffff", fieldbackground="#242424", borderwidth=0, font=(QUICKSAND_FONT_NAME, 11))
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

        frame_button = ctk.CTkFrame(frame_data_items, fg_color="transparent")
        frame_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
        frame_button.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(frame_button, text="Cadastrar/Atualizar", command=self.register_item, fg_color="#ff7b00", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(frame_button, text="Limpar Campos", command=self.clear_fields, fg_color="#D35B58", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(frame_button, text="Sair", command=self.destroy, fg_color="#271F1F", font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    def _create_list_frame(self):
        """Cria o painel que exibe a lista de itens cadastrados."""
        frame_registered_items = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        frame_registered_items.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        frame_registered_items.grid_columnconfigure(0, weight=1)
        frame_registered_items.grid_rowconfigure(2, weight=1) # Mudar para linha 2 para dar espaço à pesquisa
        
        # --- Frame para a barra de pesquisa ---
        frame_pesquisa = ctk.CTkFrame(frame_registered_items, fg_color="transparent")
        frame_pesquisa.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        frame_pesquisa.grid_columnconfigure(0, weight=1)

        self.entry_pesquisa = ctk.CTkEntry(frame_pesquisa, placeholder_text="Pesquisar por nome, marca, etc...")
        self.entry_pesquisa.grid(row=0, column=0, padx=(0,5), pady=5, sticky="ew")
        
        # Adiciona o comando para executar a pesquisa
        ctk.CTkButton(frame_pesquisa, text="Pesquisar", width=100, command=self._executar_pesquisa, font=(QUICKSAND_FONT_NAME, 14)).grid(row=0, column=1, padx=5, pady=5)
        # Novo botão para limpar a pesquisa
        ctk.CTkButton(frame_pesquisa, text="Limpar", width=100, command=self._limpar_pesquisa, font=(QUICKSAND_FONT_NAME, 14), fg_color="#565b5e").grid(row=0, column=2, padx=(0,5), pady=5)

        self.tree = ttk.Treeview(frame_registered_items, columns=('Id', 'Nome', 'Alcoólico', 'Marca', 'Quantidade'), show="headings")
        self.tree.heading('Id', text='Id'); self.tree.heading('Nome', text='Nome'); self.tree.heading('Alcoólico', text='Alcoólico'); self.tree.heading('Marca', text='Marca'); self.tree.heading('Quantidade', text='Quantidade')
        
        self.tree.column("Id", width=50, anchor="center")
        self.tree.column("Nome", width=200)
        self.tree.column("Alcoólico", width=100, anchor="center")
        self.tree.column("Marca", width=150)
        self.tree.column("Quantidade", width=100, anchor="center")
        
        self.tree.grid(row=2, column=0, padx=10, pady=10, sticky='nsew') # Mudar para linha 2
        
        scrollbar = ttk.Scrollbar(frame_registered_items, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=1, sticky='ns') # Mudar para linha 2
        self.tree.configure(yscrollcommand=scrollbar.set)

        ctk.CTkButton(frame_registered_items, text="Editar Selecionado", command=self.edit_item, font=(QUICKSAND_FONT_NAME, 14)).grid(row=3, column=0, padx=10, pady=10, sticky='w') # Mudar para linha 3
        ctk.CTkButton(frame_registered_items, text="Remover Selecionado", command=self.remove_selected_item, fg_color="#D35B58", font=(QUICKSAND_FONT_NAME, 14)).grid(row=3, column=0, padx=10, pady=10, sticky='e') # Mudar para linha 3

    def register_item(self):
        """Salva um novo item ou atualiza um item existente."""
        nome = self.entry_item.get()
        tipo = self.entry_tipo.get().lower()
        marca = self.entry_marca.get()
        quantidade = self.entry_quantidade.get()
        
        if not all([nome, tipo, marca, quantidade]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        if tipo not in ["sim", "nao"]:
            messagebox.showerror("Erro", "O campo 'Alcoólico' deve ser 'sim' ou 'nao'.")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
            return

        if self.selected_item_id_to_edit is not None:
            self.gerenciador_itens.atualizar_item(self.selected_item_id_to_edit, nome, tipo, marca, quantidade)
            self.selected_item_id_to_edit = None
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
            messagebox.showinfo("Aviso", "Nenhum item selecionado.")
            return
        
        item_id_to_remove = int(self.tree.item(selected_item, 'values')[0])
        self.gerenciador_itens.remover_item(item_id_to_remove)
        self.popular_tabela()
        messagebox.showinfo("Sucesso", "Item removido com sucesso!")

    def edit_item(self):
        """Carrega os dados de um item selecionado para edição."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Aviso", "Nenhum item selecionado para editar.")
            return

        item_data = self.tree.item(selected_item, 'values')
        self.selected_item_id_to_edit = int(item_data[0])
        
        self.clear_fields()
        self.entry_item.insert(0, item_data[1])
        self.entry_tipo.insert(0, item_data[2])
        self.entry_marca.insert(0, item_data[3])
        self.entry_quantidade.insert(0, item_data[4])
        
    def clear_fields(self):
        """Limpa os campos de entrada do formulário."""
        self.entry_item.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.selected_item_id_to_edit = None