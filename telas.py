import customtkinter as ctk
from tkinter import ttk, messagebox

# --- Tela de Login ---
class TelaLogin(ctk.CTk):
    """Tela para login do usuário."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Login")
        self.geometry("450x350")
        self.resizable(False, False) # Evita que a janela seja redimensionada

        # CORREÇÃO: Substituído o canvas por uma cor de fundo sólida e performática.
        self.configure(fg_color="#2a0a0a")

        self._criar_widgets()

    # REMOÇÃO: O método create_canvas foi removido por ser ineficiente.

    def _criar_widgets(self):
        """Cria os widgets de entrada de usuário e botões."""
        # CORREÇÃO: Usando uma fonte padrão e consistente (Arial).
        FONT = ("Arial", 14)

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="Usuário:", font=FONT).pack(pady=(20, 5), anchor="w")
        self.entry_usuario = ctk.CTkEntry(main_frame, placeholder_text="Digite seu usuário", font=FONT)
        self.entry_usuario.pack(pady=5, fill="x")

        ctk.CTkLabel(main_frame, text="Senha:", font=FONT).pack(pady=(20, 5), anchor="w")
        self.entry_senha = ctk.CTkEntry(main_frame, placeholder_text="Digite sua senha", show="*", font=FONT)
        self.entry_senha.pack(pady=5, fill="x")
        
        frame_botoes = ctk.CTkFrame(main_frame, fg_color="transparent")
        frame_botoes.pack(pady=30)

        ctk.CTkButton(frame_botoes, text="Entrar", command=self._executar_login, fg_color="#ff7b00", font=FONT).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botoes, text="Cancelar", command=self.destroy, fg_color="#a83232", font=FONT).grid(row=0, column=1, padx=10)
        
        # CORREÇÃO: Botão de cadastro movido para o rodapé para um layout mais robusto.
        ctk.CTkButton(self, text="Criar Cadastro", command=self._abrir_cadastro, fg_color="transparent", border_width=1, border_color="#007acc", hover_color="#007acc").pack(side="bottom", pady=10)

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

# --- Tela de Cadastro de Usuário ---
class TelaCadastroUsuario(ctk.CTk):
    """Tela para cadastro de novos usuários."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Cadastro de Usuário")
        self.geometry("500x500")
        self.resizable(False, False)

        # CORREÇÃO: Fundo sólido consistente com a tela de login.
        self.configure(fg_color="#2a0a0a")

        self._criar_widgets()

    # REMOÇÃO: O método create_canvas foi removido.

    def _criar_widgets(self):
        FONT = ("Arial", 14)
        
        # CORREÇÃO: Frame principal configurado para ser transparente.
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(frame_principal, text="Nome Completo:", font=FONT).grid(row=0, column=0, pady=10, sticky="w")
        self.entry_nome = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome completo", font=FONT)
        self.entry_nome.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Email:", font=FONT).grid(row=1, column=0, pady=10, sticky="w")
        self.entry_email = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu email", font=FONT)
        self.entry_email.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Usuário:", font=FONT).grid(row=2, column=0, pady=10, sticky="w")
        self.entry_usuario = ctk.CTkEntry(frame_principal, placeholder_text="Crie um nome de usuário", font=FONT)
        self.entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Senha:", font=FONT).grid(row=3, column=0, pady=10, sticky="w")
        self.entry_senha = ctk.CTkEntry(frame_principal, placeholder_text="Crie uma senha", show="*", font=FONT)
        self.entry_senha.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=30)
        
        # CORREÇÃO: Removido o parâmetro 'width' para auto-ajuste.
        ctk.CTkButton(frame_botoes, text="Cadastrar", font=FONT, command=self._executar_cadastro).grid(row=0, column=0, padx=20)
        ctk.CTkButton(frame_botoes, text="Voltar para Login", font=FONT, fg_color="#a83232", command=self._voltar_login).grid(row=0, column=1, padx=20)

        frame_principal.grid_columnconfigure(1, weight=1)

    def _executar_cadastro(self):
        """Coleta os dados dos campos e tenta registrar um novo usuário."""
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
            messagebox.showerror("Erro de Cadastro", "Este nome de usuário já existe!")

    def _voltar_login(self):
        """Fecha a tela de cadastro e volta para a de login."""
        self.destroy()
        self.app.mostrar_tela_login()

# --- Tela Principal de Gerenciamento ---
class TelaPrincipal(ctk.CTk):
    """Tela principal para gerenciamento de itens (adicionar, editar, remover)."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.gerenciador_itens = app.gerenciador_itens
        
        self.selected_item_id_to_edit = None
        
        self.title("Gerenciador de Estoque")
        self.geometry("1280x720")
        
        # CORREÇÃO: Fundo sólido consistente com as outras telas.
        self.configure(fg_color="#2a0a0a")

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
        # REMOÇÃO: O canvas de fundo foi removido.
        self._style_treeview()
        self._create_input_frame()
        self._create_list_frame()

    def _style_treeview(self):
        """Configura o estilo visual da tabela (Treeview)."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#242424", foreground="#ffffff", fieldbackground="#242424", borderwidth=0, rowheight=25)
        style.map('Treeview', background=[('selected', "#1f6aa5")])
        style.configure("Treeview.Heading", background="#565b5e", foreground="#ffffff", font=('Arial', 12, 'bold'), relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def _create_input_frame(self):
        """Cria o frame da esquerda com os campos de entrada de dados."""
        # CORREÇÃO: Frame transparente para se mesclar ao fundo.
        frame_data_items = ctk.CTkFrame(self, fg_color="transparent")
        frame_data_items.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        FONT = ("Arial", 12)
        
        ctk.CTkLabel(frame_data_items, text="Nome do item:", font=FONT).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.entry_item = ctk.CTkEntry(frame_data_items, width=220, font=FONT)
        self.entry_item.grid(row=1, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(frame_data_items, text="Alcoólico (sim/nao):", font=FONT).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.entry_tipo = ctk.CTkEntry(frame_data_items, width=220, font=FONT)
        self.entry_tipo.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(frame_data_items, text="Marca:", font=FONT).grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.entry_marca = ctk.CTkEntry(frame_data_items, width=220, font=FONT)
        self.entry_marca.grid(row=3, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(frame_data_items, text="Quantidade:", font=FONT).grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.entry_quantidade = ctk.CTkEntry(frame_data_items, width=220, font=FONT)
        self.entry_quantidade.grid(row=4, column=1, padx=10, pady=10)

        frame_button = ctk.CTkFrame(frame_data_items, fg_color="transparent")
        frame_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
        frame_button.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(frame_button, text="Salvar Item", command=self.register_item, fg_color="#ff7b00", font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(frame_button, text="Limpar Campos", command=self.clear_fields, fg_color="#a83232", font=FONT).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkButton(frame_data_items, text="Sair do Sistema", command=self.destroy, fg_color="#333333").grid(row=6, column=0, columnspan=2, padx=10, pady=(20, 0), sticky="ew")
    
    def _create_list_frame(self):
        """Cria o frame da direita com a tabela de itens registrados."""
        frame_registered_items = ctk.CTkFrame(self, fg_color="transparent")
        frame_registered_items.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        frame_registered_items.grid_columnconfigure(0, weight=1)
        frame_registered_items.grid_rowconfigure(0, weight=1) # Alterado de 1 para 0 para o Treeview
        
        self.tree = ttk.Treeview(frame_registered_items, columns=('Id', 'Nome', 'Alcoólico', 'Marca', 'Quantidade'), show="headings")
        self.tree.heading('Id', text='Id'); self.tree.heading('Nome', text='Nome'); self.tree.heading('Alcoólico', text='Alcoólico'); self.tree.heading('Marca', text='Marca'); self.tree.heading('Quantidade', text='Quantidade')
        
        self.tree.column("Id", width=50, anchor="center")
        self.tree.column("Nome", width=200, anchor="w")
        self.tree.column("Alcoólico", width=100, anchor="center")
        self.tree.column("Marca", width=150, anchor="w")
        self.tree.column("Quantidade", width=100, anchor="center")
        
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(frame_registered_items, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # CORREÇÃO: Botões de ação da tabela em um frame separado para layout correto.
        bottom_frame = ctk.CTkFrame(frame_registered_items, fg_color="transparent")
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ctk.CTkButton(bottom_frame, text="Editar Selecionado", command=self.edit_item).pack(side="left", padx=5)
        ctk.CTkButton(bottom_frame, text="Remover Selecionado", command=self.remove_selected_item, fg_color="#D35B58").pack(side="right", padx=5)

    def register_item(self):
        """Cadastra um novo item ou atualiza um item existente."""
        nome = self.entry_item.get()
        tipo = self.entry_tipo.get().lower()
        marca = self.entry_marca.get()
        quantidade_str = self.entry_quantidade.get()
        
        if not all([nome, tipo, marca, quantidade_str]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
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
        """Remove o item atualmente selecionado na tabela."""
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
        """Preenche os campos de entrada com os dados do item selecionado."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum item foi selecionado para edição.")
            return

        item_data = self.tree.item(selected_item, 'values')
        self.selected_item_id_to_edit = int(item_data[0]) 
        
        self.clear_fields(clear_id=False) # Evita limpar o ID que acabamos de setar
        self.entry_item.insert(0, item_data[1])
        self.entry_tipo.insert(0, item_data[2])
        self.entry_marca.insert(0, item_data[3])
        self.entry_quantidade.insert(0, item_data[4])
        
    def clear_fields(self, clear_id=True):
        """Limpa todos os campos de entrada de dados."""
        self.entry_item.delete(0, "end")
        self.entry_tipo.delete(0, "end")
        self.entry_marca.delete(0, "end")
        self.entry_quantidade.delete(0, "end")
        if clear_id:
            self.selected_item_id_to_edit = None