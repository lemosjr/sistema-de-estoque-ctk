import os
import json
from tkinter import ttk, messagebox
import customtkinter as ctk

canvas = tk.Canvas(tela_principal, width=450, height=450, highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

def draw_gradient(canvas, color1, color2):
    width = canvas.winfo_reqwidth()
    height = canvas.winfo_reqheight()
    limit = height
    (r1,g1,b1) = tela_principal.winfo_rgb(color1)
    (r2,g2,b2) = tela_principal.winfo_rgb(color2)
    r_ratio = float(r2-r1) / limit
    g_ratio = float(g2-g1) / limit
    b_ratio = float(b2-b1) / limit

    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%04x%04x%04x" % (nr, ng, nb)
        canvas.create_line(0, i, width, i, fill=color, tags=("gradient,"))

draw_gradient(canvas, "#3c0a0a", "#1a0000")

def open_arquivo():
    """
    Verifica se o arquivo 'usuarios.json' existe. Se não existir, cria um
    arquivo vazio. Retorna o conteúdo do arquivo.
    """
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as file:
            return json.load(file)
    else:
        with open("usuarios.json", "w") as file:
            json.dump({}, file)
            return {}

class ItemManager:
    """
    Classe principal para gerenciar o cadastro de itens em uma interface gráfica.
    """
    # MÉTODO CONSTRUTOR
    def __init__(self, root):
        """
        Inicializa a janela principal e os atributos da classe.
        """
        self.root = root
        self.item_id = 0
        self.itens = []
        self.selected_item_id_to_edit = None
        
        self.create_widgets()
        self.carregar_itens()

    # MÉTODOS DE CRIAÇÃO DA INTERFACE GRÁFICA (WIDGETS)
    
    def create_widgets(self):
        """
        Configura a janela principal e chama os métodos para criar os frames.
        """
        self.root.title("Cadastro de itens")
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.geometry("1280x720")

        self.style_treeview()
        self.create_input_frame()
        self.create_list_frame()
        
    def style_treeview(self):
        """
        Configura o estilo visual da Treeview (tabela de itens).
        """
        style = ttk.Style()
        bg_color = "#242424"
        text_color = "#ffffff"
        selected_color = "#1f6aa5"
        field_bg_color = "#242424"
        heading_bg_color = "#565b5e"

        style.theme_use("default")
        style.configure("Treeview",
                        background=bg_color,
                        foreground=text_color,
                        fieldbackground=field_bg_color,
                        borderwidth=0)
        style.map('Treeview', background=[('selected', selected_color)])

        style.configure("Treeview.Heading",
                        background=heading_bg_color,
                        foreground=text_color,
                        font=('Calibri', 10, 'bold'),
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def create_input_frame(self):
        """
        Cria o frame da esquerda, com os campos de entrada e botões de ação.
        """
        frame_data_items = ctk.CTkFrame(self.root, corner_radius=10)
        frame_data_items.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

        label_data_title = ctk.CTkLabel(frame_data_items, text="Cadastro de itens", font=ctk.CTkFont(size=16, weight="bold"))
        label_data_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))

        # --- Campos de Entrada ---
        label_item = ctk.CTkLabel(frame_data_items, text="Nome do item:")
        label_item.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.entry_item = ctk.CTkEntry(frame_data_items, width=220)
        self.entry_item.grid(row=1, column=1, padx=10, pady=5)

        label_type = ctk.CTkLabel(frame_data_items, text="Tipo do item:")
        label_type.grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.entry_type = ctk.CTkEntry(frame_data_items, width=220)
        self.entry_type.grid(row=2, column=1, padx=10, pady=5)

        label_quality = ctk.CTkLabel(frame_data_items, text="Qualidade do item:")
        label_quality.grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.entry_quality = ctk.CTkEntry(frame_data_items, width=220)
        self.entry_quality.grid(row=3, column=1, padx=10, pady=5)

        label_amount = ctk.CTkLabel(frame_data_items, text="Quantidade do item:")
        label_amount.grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.entry_amount = ctk.CTkEntry(frame_data_items, width=220)
        self.entry_amount.grid(row=4, column=1, padx=10, pady=5)

        # --- Botões de Ação ---
        frame_button = ctk.CTkFrame(frame_data_items, fg_color="transparent")
        frame_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
        frame_button.grid_columnconfigure((0, 1, 2), weight=1)

        botao_register = ctk.CTkButton(frame_button, text="Cadastrar", command=self.register_item, fg_color="#ff7b00", hover_color="#3484F0")
        botao_register.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        button_clean = ctk.CTkButton(frame_button, text="Limpar", fg_color="#D35B58", hover_color="#C77C78", command=self.clear_fields)
        button_clean.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_exit = ctk.CTkButton(frame_button, text="Sair", fg_color="#271F1F", hover_color="#413B3B", command=self.root.destroy)
        button_exit.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    def create_list_frame(self):
        """
        Cria o frame da direita, com a barra de pesquisa e a lista de itens.
        """
        frame_registered_items = ctk.CTkFrame(self.root, corner_radius=10)
        frame_registered_items.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        frame_registered_items.grid_columnconfigure(0, weight=1)
        frame_registered_items.grid_rowconfigure(1, weight=1)
        
        label_registered_titles = ctk.CTkLabel(frame_registered_items, text="Itens Cadastrados", font=ctk.CTkFont(size=16, weight="bold"))
        label_registered_titles.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # --- Barra de Pesquisa ---
        frame_search = ctk.CTkFrame(frame_registered_items, fg_color="transparent")
        frame_search.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="e")

        self.entry_search = ctk.CTkEntry(frame_search, width=200, placeholder_text="Pesquisar Item...")
        self.entry_search.pack(side='left', padx=(0, 10))

        botao_search = ctk.CTkButton(frame_search, text="Pesquisar", command=self.search_item)
        botao_search.pack(side='left')

        # --- Tabela (Treeview) ---
        self.tree = ttk.Treeview(frame_registered_items, columns=('Id', 'Nome', 'Tipo', 'Qualidade', 'Quantidade'), show="headings")
        self.tree.heading('Id', text='Id')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Qualidade', text='Qualidade')
        self.tree.heading('Quantidade', text='Quantidade')

        self.tree.column('Id', width=125, anchor='center')
        self.tree.column('Nome', width=125)
        self.tree.column('Tipo', width=125)
        self.tree.column('Qualidade', width=125)
        self.tree.column('Quantidade', width=125)

        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        # --- Botões de Edição/Remoção da Lista ---
        button_edit = ctk.CTkButton(frame_registered_items, text="Editar Selecionado", command=self.edit_item)
        button_edit.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        button_clean_all = ctk.CTkButton(frame_registered_items, text="Remover Selecionado", command=self.remove_selected_item, fg_color="#D35B58", hover_color="#C77C78")
        button_clean_all.grid(row=2, column=0, padx=10, pady=10, sticky='e')

    # MÉTODOS DE GERENCIAMENTO DE DADOS (JSON)
    
    def carregar_itens(self):
        """
        Carrega os itens do arquivo 'itens.json' e os exibe na Treeview.
        """
        if os.path.exists("itens.json"):
            with open("itens.json", "r", encoding="utf-8") as file:
                self.itens = json.load(file)
                for item in self.itens:
                    self.tree.insert('', 'end', values=tuple(item.values()))
                if self.itens:
                    self.item_id = self.itens[-1]['Id']
    
    def salvar_itens(self):
        """
        Salva a lista atual de itens no arquivo 'itens.json'.
        """
        with open("itens.json", "w") as file:
            json.dump(self.itens, file, indent=4)

    # MÉTODOS DE FUNCIONALIDADE E EVENTOS
    def register_item(self):
        """
        Registra um novo item ou atualiza um item existente.
        """
        name = self.entry_item.get()
        item_type = self.entry_type.get()
        quality = self.entry_quality.get()
        amount = self.entry_amount.get()

        if name and item_type and quality and amount:
            if self.selected_item_id_to_edit is not None:
                # Lógica para ATUALIZAR um item existente
                for i in range(len(self.itens)):
                    if self.itens[i]['Id'] == self.selected_item_id_to_edit:
                        self.itens[i]['Nome'] = name
                        self.itens[i]['Tipo'] = item_type
                        self.itens[i]['Qualidade'] = quality
                        self.itens[i]['Quantidade'] = amount
                        break

                selected_item_id_on_treeview = self.tree.selection()[0]
                self.tree.item(selected_item_id_on_treeview, values=(self.selected_item_id_to_edit, name, item_type, quality, amount))
                messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
                self.selected_item_id_to_edit = None   
            else:
                # Lógica para CADASTRAR um novo item
                self.item_id += 1
                novo_item = {
                    "Id": self.item_id,
                    "Nome": name,
                    "Tipo": item_type,
                    "Qualidade": quality,
                    "Quantidade": amount
                }
                self.itens.append(novo_item)
                self.tree.insert('', 'end', values=(self.item_id, name, item_type, quality, amount))
                messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")
            
            self.salvar_itens()
            self.clear_fields()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    def clear_fields(self):
        """
        Limpa todos os campos de entrada de texto.
        """
        self.entry_item.delete(0, ctk.END)
        self.entry_type.delete(0, ctk.END)
        self.entry_quality.delete(0, ctk.END)
        self.entry_amount.delete(0, ctk.END)

    def remove_selected_item(self):
        """
        Remove o item que está selecionado na Treeview.
        """
        selected_item = self.tree.selection()
        if selected_item:
            # Pega os valores do item selecionado na tabela
            item_values = self.tree.item(selected_item, 'values')
            item_id_to_remove = int(item_values[0]) # Converte o ID para inteiro

            # Remove o item da lista interna 'self.itens'
            self.itens = [item for item in self.itens if item['Id'] != item_id_to_remove]
            
            # Remove o item da Treeview (interface)
            self.tree.delete(selected_item)
            
            self.salvar_itens()
            messagebox.showinfo("Sucesso", "Item removido com sucesso!")
        else:
            messagebox.showinfo("Informação", "Nenhum item selecionado para remover.")
    
    def search_item(self):
        """
        Filtra os itens na Treeview com base no termo de pesquisa.
        """
        search_term = self.entry_search.get().lower()

        # Limpa a visualização atual da Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Encontra os itens que correspondem à pesquisa
        found_items = [item for item in self.itens if search_term in item['Nome'].lower()]
        
        if not found_items:
            messagebox.showinfo("Pesquisa", "Nenhum item encontrado.")
        
        # Adiciona os itens encontrados de volta na Treeview
        for item in found_items:
            self.tree.insert('', 'end', values=tuple(item.values()))

    def edit_item(self):
        """
        Pega os dados de um item selecionado e os coloca nos campos de entrada para edição.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Informação", "Nenhum item selecionado para editar.")
            return

        item_data = self.tree.item(selected_item, 'values')
        # Armazena o ID do item que está sendo editado
        self.selected_item_id_to_edit = int(item_data[0]) 
        
        # Preenche os campos de entrada com os dados do item
        self.clear_fields()
        self.entry_item.insert(0, item_data[1])
        self.entry_type.insert(0, item_data[2])
        self.entry_quality.insert(0, item_data[3])
        self.entry_amount.insert(0, item_data[4])

def abrir_cadastro():
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        root = ctk.CTk()
        app = ItemManager(root)
        root.mainloop()
#abrir_cadastro()