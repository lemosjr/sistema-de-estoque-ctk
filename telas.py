import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class TelaLogin(ctk.CTk):
    """Tela para login do usuário."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Login")
        self.geometry("450x350")
        self._criar_widgets()

    def _criar_widgets(self):
        ctk.CTkLabel(self, text="Usuário:").pack(pady=(20, 5))
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Digite seu usuário:")
        self.entry_usuario.pack(pady=5)

        ctk.CTkLabel(self, text="Senha:").pack(pady=(20, 5))
        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha:", show="*")
        self.entry_senha.pack(pady=5)
        
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(pady=20)
        ctk.CTkButton(frame_botoes, text="Entrar", command=self._executar_login, fg_color="#ff7b00").grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botoes, text="Cancelar", command=self.destroy, fg_color="#a83232").grid(row=0, column=1, padx=10)
        ctk.CTkButton(self, text="Cadastro", width=10, command=self._abrir_cadastro, fg_color="#007acc").place(x=380, y=300)

    def _executar_login(self):
        """Valida as credenciais e decide se abre a tela principal."""
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        if self.app.gerenciador_usuarios.validar_credenciais(usuario, senha):
            self.destroy()
            self.app.mostrar_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def _abrir_cadastro(self):
        """Fecha a tela de login e abre a de cadastro."""
        self.destroy()
        self.app.mostrar_tela_cadastro_usuario()


class TelaCadastroUsuario(ctk.CTk):
    """Tela para cadastro de novos usuários."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Cadastro")
        self.geometry("550x600")
        self._criar_widgets()

    def _criar_widgets(self):
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(frame_principal, text="Nome Completo:", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="w")
        self.entry_nome = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome completo", font=("Arial", 12))
        self.entry_nome.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Email:", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        self.entry_email = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu email", font=("Arial", 12))
        self.entry_email.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Usuário:", font=("Arial", 12)).grid(row=2, column=0, pady=10, sticky="w")
        self.entry_usuario = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome de usuário", font=("Arial", 12))
        self.entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Senha:", font=("Arial", 12)).grid(row=3, column=0, pady=10, sticky="w")
        self.entry_senha = ctk.CTkEntry(frame_principal, placeholder_text="Digite sua senha", show="*", font=("Arial", 12))
        self.entry_senha.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(frame_botoes, text="Cadastrar", font=("Arial", 12), command=self._executar_cadastro, width=20).grid(row=0, column=0, padx=20)
        ctk.CTkButton(frame_botoes, text="Cancelar", font=("Arial", 12), fg_color="#a83232", command=self._voltar_login, hover_color="#F24B88", width=20).grid(row=0, column=1, padx=20)

        frame_principal.grid_columnconfigure(1, weight=1)

    def _executar_cadastro(self):
        """Coleta os dados dos campos e tenta registrar um novo usuário."""
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
        """Fecha a tela de cadastro e volta para a de login."""
        self.destroy()
        self.app.mostrar_tela_login()


class TelaPrincipal(ctk.CTk):
    """Tela principal para gerenciamento de itens (adicionar, editar, remover)."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.gerenciador_itens = app.gerenciador_itens
        
        self.selected_item_id_to_edit = None
        
        self.title("Cadastro de Itens")
        self.geometry("1280x720")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self.popular_tabela()

    def popular_tabela(self):
        """Limpa e preenche a tabela com os dados do gerenciador de itens."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.gerenciador_itens.listar_itens():
            self.tree.insert('', 'end', values=tuple(item.values()))

    def _create_widgets(self):
        canvas = tk.Canvas(self, width=1280, height=720, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        def draw_gradient(canvas, color1, color2):
            width = self.winfo_width()
            height = self.winfo_height()
            (r1,g1,b1) = self.winfo_rgb(color1)
            (r2,g2,b2) = self.winfo_rgb(color2)
            r_ratio = float(r2-r1) / height
            g_ratio = float(g2-g1) / height
            b_ratio = float(b2-b1) / height
            for i in range(height):
                nr = int(r1 + (r_ratio * i))
                ng = int(g1 + (g_ratio * i))
                nb = int(b1 + (b_ratio * i))
                color = f"#{nr:04x}{ng:04x}{nb:04x}"
                canvas.create_line(0, i, width, i, fill=color, tags=("gradient,"))
        
        self.after(100, lambda: draw_gradient(canvas, "#3c0a0a", "#1a0000"))

        self._style_treeview()
        self._create_input_frame()
        self._create_list_frame()

    def _style_treeview(self):
        """Configura o estilo visual da tabela (Treeview)."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#242424", foreground="#ffffff", fieldbackground="#242424", borderwidth=0)
        style.map('Treeview', background=[('selected', "#1f6aa5")])
        style.configure("Treeview.Heading", background="#565b5e", foreground="#ffffff", font=('Calibri', 10, 'bold'), relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def _create_input_frame(self):
        """Cria o frame da esquerda com os campos de entrada de dados."""
        frame_data_items = ctk.CTkFrame(self, corner_radius=10)
        frame_data_items.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        
        # Nome do Item
        ctk.CTkLabel(frame_data_items, text="Nome do item:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.entry_item = ctk.CTkEntry(frame_data_items, width=220)
        self.entry_item.grid(row=1, column=1, padx=10, pady=5)
        
        # Tipo (Alcoólico)
        ctk.CTkLabel(frame_data_items, text="Alcoólico (sim/nao):").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.entry_tipo = ctk.CTkEntry(frame_data_items, width=220)
        self.entry_tipo.grid(row=2, column=1, padx=10, pady=5)

        # Marca
        ctk.CTkLabel(frame_data_items, text="Marca:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.entry_marca = ctk.CTkEntry(frame_data_items, width=220)
        self.entry_marca.grid(row=3, column=1, padx=10, pady=5)
        
        # Quantidade
        ctk.CTkLabel(frame_data_items, text="Quantidade:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.entry_quantidade = ctk.CTkEntry(frame_data_items, width=220)
        self.entry_quantidade.grid(row=4, column=1, padx=10, pady=5)

        frame_button = ctk.CTkFrame(frame_data_items, fg_color="transparent")
        frame_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
        frame_button.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(frame_button, text="Cadastrar/Atualizar", command=self.register_item, fg_color="#ff7b00").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(frame_button, text="Limpar", command=self.clear_fields, fg_color="#D35B58").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(frame_button, text="Sair", command=self.destroy, fg_color="#271F1F").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    def _create_list_frame(self):
        """Cria o frame da direita com a tabela de itens registrados."""
        frame_registered_items = ctk.CTkFrame(self, corner_radius=10)
        frame_registered_items.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        frame_registered_items.grid_columnconfigure(0, weight=1)
        frame_registered_items.grid_rowconfigure(1, weight=1)
        
        self.tree = ttk.Treeview(frame_registered_items, columns=('Id', 'Nome', 'Alcoólico', 'Marca', 'Quantidade'), show="headings")
        self.tree.heading('Id', text='Id'); self.tree.heading('Nome', text='Nome'); self.tree.heading('Alcoólico', text='Alcoólico'); self.tree.heading('Marca', text='Marca'); self.tree.heading('Quantidade', text='Quantidade')
        
        # Configuração das larguras das colunas
        self.tree.column("Id", width=50, anchor="center")
        self.tree.column("Nome", width=200)
        self.tree.column("Alcoólico", width=100, anchor="center")
        self.tree.column("Marca", width=150)
        self.tree.column("Quantidade", width=100, anchor="center")
        
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(frame_registered_items, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        ctk.CTkButton(frame_registered_items, text="Editar Selecionado", command=self.edit_item).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        ctk.CTkButton(frame_registered_items, text="Remover Selecionado", command=self.remove_selected_item, fg_color="#D35B58").grid(row=2, column=0, padx=10, pady=10, sticky='e')

    def register_item(self):
        """Cadastra um novo item ou atualiza um item existente."""
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
        """Remove o item atualmente selecionado na tabela."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Aviso", "Nenhum item selecionado.")
            return
        
        item_id_to_remove = int(self.tree.item(selected_item, 'values')[0])
        self.gerenciador_itens.remover_item(item_id_to_remove)
        self.popular_tabela()
        messagebox.showinfo("Sucesso", "Item removido com sucesso!")

    def edit_item(self):
        """Preenche os campos de entrada com os dados do item selecionado."""
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
        """Limpa todos os campos de entrada de dados."""
        self.entry_item.delete(0, ctk.END)
        self.entry_tipo.delete(0, ctk.END)
        self.entry_marca.delete(0, ctk.END)
        self.entry_quantidade.delete(0, ctk.END)
        self.selected_item_id_to_edit = None