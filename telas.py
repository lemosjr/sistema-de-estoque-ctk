import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
import os

# Mantendo sua lógica original de carregamento de fonte
FONT_PATH = "fonts/Quicksand-Light.ttf"
if os.path.exists(FONT_PATH):
    # Esta linha prepara a fonte, mas seu uso depende do sistema.
    # Se a fonte não aparecer, pode ser necessário instalá-la no sistema operacional.
    quicksand_font = tk.font.Font(file=FONT_PATH)

class TelaLogin(ctk.CTk):
    """Tela para login do usuário."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Login")
        self.geometry("450x350")
        self.resizable(False, False)

        self.create_canvas() # Reativando a criação do gradiente
        self._criar_widgets()

    def create_canvas(self):
        """Cria o canvas e desenha um gradiente vertical."""
        canvas = tk.Canvas(self, width=450, height=350, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        def draw_gradient():
            width = self.winfo_width()
            height = self.winfo_height()
            (r1, g1, b1) = self.winfo_rgb("#3c0a0a")
            (r2, g2, b2) = self.winfo_rgb("#1a0000")
            r_ratio = float(r2 - r1) / height
            g_ratio = float(g2 - g1) / height
            b_ratio = float(b2 - b1) / height

            for i in range(height):
                nr = int(r1 + (r_ratio * i))
                ng = int(g1 + (g_ratio * i))
                nb = int(b1 + (b_ratio * i))
                color = f"#{nr:04x}{ng:04x}{nb:04x}"
                canvas.create_line(0, i, width, i, fill=color)

        self.after(100, draw_gradient)

    def _criar_widgets(self):
        """Cria os widgets de entrada de usuário e botões."""
        FONT = ("Quicksand", 14) # Usando sua fonte original

        # CORREÇÃO PRINCIPAL: Todos os widgets são colocados em um frame transparente
        # para que o gradiente no fundo fique visível.
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(main_frame, text="Usuário:", font=FONT).pack(pady=(20, 5), anchor="w")
        self.entry_usuario = ctk.CTkEntry(main_frame, placeholder_text="Digite seu usuário", font=FONT)
        self.entry_usuario.pack(pady=5, fill="x")

        ctk.CTkLabel(main_frame, text="Senha:", font=FONT).pack(pady=(20, 5), anchor="w")
        self.entry_senha = ctk.CTkEntry(main_frame, placeholder_text="Senha", show="*", font=FONT)
        self.entry_senha.pack(pady=5, fill="x")
        
        frame_botoes = ctk.CTkFrame(main_frame, fg_color="transparent")
        frame_botoes.pack(pady=20)

        ctk.CTkButton(frame_botoes, text="Entrar", command=self._executar_login, fg_color="#ff7b00", font=FONT).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botoes, text="Cancelar", command=self.destroy, fg_color="#a83232", font=FONT).grid(row=0, column=1, padx=10)
        
        # CORREÇÃO DE LAYOUT: Botão de cadastro movido para uma posição mais estável
        ctk.CTkButton(self, text="Cadastro", width=10, command=self._abrir_cadastro, fg_color="#007acc", font=FONT).place(relx=0.98, rely=0.95, anchor="se")

    def _executar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        if self.app.gerenciador_usuarios.validar_credenciais(usuario, senha):
            self.destroy()
            self.app.mostrar_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def _abrir_cadastro(self):
        self.destroy()
        self.app.mostrar_tela_cadastro_usuario()


class TelaCadastroUsuario(ctk.CTk):
    """Tela para cadastro de novos usuários."""
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Tela de Cadastro")
        self.geometry("550x600")
        self.resizable(False, False)

        self.create_canvas()
        self._criar_widgets()

    def create_canvas(self):
        """Cria o canvas e desenha um gradiente vertical."""
        canvas = tk.Canvas(self, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        def draw_gradient():
            width = self.winfo_width()
            height = self.winfo_height()
            (r1, g1, b1) = self.winfo_rgb("#3c0a0a")
            (r2, g2, b2) = self.winfo_rgb("#1a0000")
            r_ratio = float(r2 - r1) / height
            g_ratio = float(g2 - g1) / height
            b_ratio = float(b2 - b1) / height

            for i in range(height):
                nr = int(r1 + (r_ratio * i))
                ng = int(g1 + (g_ratio * i))
                nb = int(b1 + (b_ratio * i))
                color = f"#{nr:04x}{ng:04x}{nb:04x}"
                canvas.create_line(0, i, width, i, fill=color)

        self.after(100, draw_gradient)

    def _criar_widgets(self):
        # CORREÇÃO PRINCIPAL: O frame que contém os campos agora é transparente.
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

        FONT = ("Quicksand", 12) # Consistência de fonte

        ctk.CTkLabel(frame_principal, text="Nome Completo:", font=FONT).grid(row=0, column=0, pady=10, sticky="w")
        self.entry_nome = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome completo", font=FONT)
        self.entry_nome.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Email:", font=FONT).grid(row=1, column=0, pady=10, sticky="w")
        self.entry_email = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu email", font=FONT)
        self.entry_email.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Usuário:", font=FONT).grid(row=2, column=0, pady=10, sticky="w")
        self.entry_usuario = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome de usuário", font=FONT)
        self.entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_principal, text="Senha:", font=FONT).grid(row=3, column=0, pady=10, sticky="w")
        self.entry_senha = ctk.CTkEntry(frame_principal, placeholder_text="Digite sua senha", show="*", font=FONT)
        self.entry_senha.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(frame_botoes, text="Cadastrar", font=FONT, command=self._executar_cadastro).grid(row=0, column=0, padx=20)
        ctk.CTkButton(frame_botoes, text="Cancelar", font=FONT, fg_color="#a83232", command=self._voltar_login).grid(row=0, column=1, padx=20)

        frame_principal.grid_columnconfigure(1, weight=1)

    def _executar_cadastro(self):
        nome = self.entry_nome.get(); email = self.entry_email.get(); usuario = self.entry_usuario.get(); senha = self.entry_senha.get()
        if not all([nome, email, usuario, senha]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        if self.app.gerenciador_usuarios.adicionar_usuario(usuario, senha):
            messagebox.showinfo("Sucesso", f"Cadastro de {nome} realizado com sucesso!")
            self._voltar_login()
        else:
            messagebox.showerror("Erro", "Usuário já cadastrado!")

    def _voltar_login(self):
        self.destroy()
        self.app.mostrar_tela_login()


class TelaPrincipal(ctk.CTk):
    """Tela principal para gerenciamento de itens (adicionar, editar, remover)."""
    def __init__(self, app):
        super().__init__()
        self.app = app; self.gerenciador_itens = app.gerenciador_itens
        self.selected_item_id_to_edit = None
        self.title("Cadastro de Itens"); self.geometry("1280x720")
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self._create_widgets(); self.popular_tabela()

    def popular_tabela(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for item in self.gerenciador_itens.listar_itens(): self.tree.insert('', 'end', values=tuple(item.values()))

    def _create_widgets(self):
        canvas = tk.Canvas(self, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        def draw_gradient():
            width = self.winfo_width(); height = self.winfo_height()
            (r1,g1,b1) = self.winfo_rgb("#3c0a0a"); (r2,g2,b2) = self.winfo_rgb("#1a0000")
            r_ratio = float(r2-r1) / height; g_ratio = float(g2-g1) / height; b_ratio = float(b2-b1) / height
            for i in range(height):
                nr = int(r1 + (r_ratio * i)); ng = int(g1 + (g_ratio * i)); nb = int(b1 + (b_ratio * i))
                color = f"#{nr:04x}{ng:04x}{nb:04x}"; canvas.create_line(0, i, width, i, fill=color)
        
        self.after(100, draw_gradient)
        self._style_treeview(); self._create_input_frame(); self._create_list_frame()

    def _style_treeview(self):
        style = ttk.Style(); style.theme_use("default")
        style.configure("Treeview", background="#242424", foreground="#ffffff", fieldbackground="#242424", borderwidth=0, rowheight=25)
        style.map('Treeview', background=[('selected', "#1f6aa5")])
        style.configure("Treeview.Heading", background="#565b5e", foreground="#ffffff", font=('Calibri', 12, 'bold'), relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def _create_input_frame(self):
        # CORREÇÃO PRINCIPAL: Frame de dados transparente
        frame_data_items = ctk.CTkFrame(self, fg_color="transparent")
        frame_data_items.grid(row=0, column=0, padx=20, pady=20, sticky="ns")
        
        ctk.CTkLabel(frame_data_items, text="Nome do item:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.entry_item = ctk.CTkEntry(frame_data_items, width=220); self.entry_item.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(frame_data_items, text="Alcoólico (sim/nao):").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.entry_tipo = ctk.CTkEntry(frame_data_items, width=220); self.entry_tipo.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(frame_data_items, text="Marca:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.entry_marca = ctk.CTkEntry(frame_data_items, width=220); self.entry_marca.grid(row=3, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(frame_data_items, text="Quantidade:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.entry_quantidade = ctk.CTkEntry(frame_data_items, width=220); self.entry_quantidade.grid(row=4, column=1, padx=10, pady=5)

        frame_button = ctk.CTkFrame(frame_data_items, fg_color="transparent")
        frame_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
        frame_button.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(frame_button, text="Cadastrar/Atualizar", command=self.register_item, fg_color="#ff7b00").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(frame_button, text="Limpar", command=self.clear_fields, fg_color="#D35B58").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(frame_button, text="Sair", command=self.destroy, fg_color="#271F1F").grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    
    def _create_list_frame(self):
        # CORREÇÃO PRINCIPAL: Frame da tabela transparente
        frame_registered_items = ctk.CTkFrame(self, fg_color="transparent")
        frame_registered_items.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        frame_registered_items.grid_columnconfigure(0, weight=1); frame_registered_items.grid_rowconfigure(1, weight=1)
        
        self.tree = ttk.Treeview(frame_registered_items, columns=('Id', 'Nome', 'Alcoólico', 'Marca', 'Quantidade'), show="headings")
        self.tree.heading('Id', text='Id'); self.tree.heading('Nome', text='Nome'); self.tree.heading('Alcoólico', text='Alcoólico'); self.tree.heading('Marca', text='Marca'); self.tree.heading('Quantidade', text='Quantidade')
        
        self.tree.column("Id", width=50, anchor="center"); self.tree.column("Nome", width=200); self.tree.column("Alcoólico", width=100, anchor="center"); self.tree.column("Marca", width=150); self.tree.column("Quantidade", width=100, anchor="center")
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(frame_registered_items, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns'); self.tree.configure(yscrollcommand=scrollbar.set)
        
        # CORREÇÃO DE LAYOUT: Botões em um frame separado para não se sobreporem
        bottom_frame = ctk.CTkFrame(frame_registered_items, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        ctk.CTkButton(bottom_frame, text="Editar Selecionado", command=self.edit_item).pack(side="left", padx=10)
        ctk.CTkButton(bottom_frame, text="Remover Selecionado", command=self.remove_selected_item, fg_color="#D35B58").pack(side="right", padx=10)

    def register_item(self):
        nome = self.entry_item.get(); tipo = self.entry_tipo.get().lower(); marca = self.entry_marca.get(); quantidade = self.entry_quantidade.get()
        if not all([nome, tipo, marca, quantidade]): messagebox.showerror("Erro", "Todos os campos devem ser preenchidos."); return
        if tipo not in ["sim", "nao"]: messagebox.showerror("Erro", "O campo 'Alcoólico' deve ser 'sim' ou 'nao'."); return
        try: quantidade = int(quantidade)
        except ValueError: messagebox.showerror("Erro", "Quantidade deve ser um número inteiro."); return

        if self.selected_item_id_to_edit is not None:
            self.gerenciador_itens.atualizar_item(self.selected_item_id_to_edit, nome, tipo, marca, quantidade)
            self.selected_item_id_to_edit = None; messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
        else:
            self.gerenciador_itens.adicionar_item(nome, tipo, marca, quantidade); messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")
        
        self.popular_tabela(); self.clear_fields()

    def remove_selected_item(self):
        selected_item = self.tree.selection()
        if not selected_item: messagebox.showinfo("Aviso", "Nenhum item selecionado."); return
        
        item_id_to_remove = int(self.tree.item(selected_item, 'values')[0])
        self.gerenciador_itens.remover_item(item_id_to_remove)
        self.popular_tabela(); messagebox.showinfo("Sucesso", "Item removido com sucesso!")

    def edit_item(self):
        selected_item = self.tree.selection()
        if not selected_item: messagebox.showinfo("Aviso", "Nenhum item selecionado para editar."); return

        item_data = self.tree.item(selected_item, 'values'); self.selected_item_id_to_edit = int(item_data[0]) 
        self.clear_fields(); self.entry_item.insert(0, item_data[1]); self.entry_tipo.insert(0, item_data[2]); self.entry_marca.insert(0, item_data[3]); self.entry_quantidade.insert(0, item_data[4])
        
    def clear_fields(self):
        self.entry_item.delete(0, 'end'); self.entry_tipo.delete(0, 'end'); self.entry_marca.delete(0, 'end'); self.entry_quantidade.delete(0, 'end')
        self.selected_item_id_to_edit = None