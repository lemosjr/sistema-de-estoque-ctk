import customtkinter as ctk
from tkinter import ttk, messagebox

def abrir_cadastro():
    global item_id, selected_item_id_to_edit
    item_id = 0
    selected_item_id_to_edit = None

    def register_item():
        global item_id, selected_item_id_to_edit
        name = entry_item.get()
        item_type = entry_type.get()
        quality = entry_quality.get()
        amount = entry_amount.get()

        if name and item_type and quality and amount:
            
            if selected_item_id_to_edit is not None:
                selected_item = tree.selection()[0]
                tree.item(selected_item, values=(selected_item_id_to_edit, name, item_type, quality, amount))
                messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
                selected_item_id_to_edit = None  
            else:
                item_id += 1
                tree.insert('', 'end', values=(item_id, name, item_type, quality, amount))
                messagebox.showinfo("Sucesso", "Item cadastrado com sucesso!")
            
            clear_fields()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    def clear_fields():
        entry_item.delete(0, ctk.END)
        entry_type.delete(0, ctk.END)
        entry_quality.delete(0, ctk.END)
        entry_amount.delete(0, ctk.END)

    def remove_selected_item():
        selected_item = tree.selection()
        if selected_item:
            tree.delete(selected_item)
        else:
            messagebox.showinfo("Informação", "Nenhum item selecionado para remover.")
    
    def search_item():
        search_term = entry_search.get().lower()

        for item in tree.get_children():
            tree.delete(item)

        items = [
            (1, "Espada", "Arma", "Épica", "1"),
            (2, "Escudo", "Defesa", "Comum", "3"),
            (3, "Poção de Vida", "Consumível", "Rara", "5")
        ]
        
        found_items = [item for item in items if search_term in item[1].lower()]
        
        if not found_items:
            messagebox.showinfo("Pesquisa", "Nenhum item encontrado.")
        
        for item in found_items:
            tree.insert('', 'end', values=item)

    def edit_item():
        global selected_item_id_to_edit
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Informação", "Nenhum item selecionado para editar.")
            return

        selected_item_id_to_edit = selected_item[0]
        item_data = tree.item(selected_item, 'values')
        
        clear_fields()
        entry_item.insert(0, item_data[1])
        entry_type.insert(0, item_data[2])
        entry_quality.insert(0, item_data[3])
        entry_amount.insert(0, item_data[4])


    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Cadastro de itens")

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

    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    frame_data_items = ctk.CTkFrame(root, corner_radius=10)
    frame_data_items.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

    frame_registered_items = ctk.CTkFrame(root, corner_radius=10)
    frame_registered_items.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
    frame_registered_items.grid_columnconfigure(0, weight=1)
    frame_registered_items.grid_rowconfigure(1, weight=1)

    label_data_title = ctk.CTkLabel(frame_data_items, text="Cadastro de itens", font=ctk.CTkFont(size=16, weight="bold"))
    label_data_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))

    label_item = ctk.CTkLabel(frame_data_items, text="Nome do item:")
    label_item.grid(row=1, column=0, padx=10, pady=5, sticky='w')
    entry_item = ctk.CTkEntry(frame_data_items, width=220)
    entry_item.grid(row=1, column=1, padx=10, pady=5)

    label_type = ctk.CTkLabel(frame_data_items, text="Tipo do item:")
    label_type.grid(row=2, column=0, padx=10, pady=5, sticky='w')
    entry_type = ctk.CTkEntry(frame_data_items, width=220)
    entry_type.grid(row=2, column=1, padx=10, pady=5)

    label_quality = ctk.CTkLabel(frame_data_items, text="Qualidade do item:")
    label_quality.grid(row=3, column=0, padx=10, pady=5, sticky='w')
    entry_quality = ctk.CTkEntry(frame_data_items, width=220)
    entry_quality.grid(row=3, column=1, padx=10, pady=5)

    label_amount = ctk.CTkLabel(frame_data_items, text="Quantidade do item:")
    label_amount.grid(row=4, column=0, padx=10, pady=5, sticky='w')
    entry_amount = ctk.CTkEntry(frame_data_items, width=220)
    entry_amount.grid(row=4, column=1, padx=10, pady=5)

    frame_button = ctk.CTkFrame(frame_data_items, fg_color="transparent")
    frame_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
    frame_button.grid_columnconfigure((0, 1, 2), weight=1)

    botao_register = ctk.CTkButton(frame_button, text="Cadastrar", command=register_item)
    botao_register.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    button_clean = ctk.CTkButton(frame_button, text="Limpar", fg_color="#D35B58", hover_color="#C77C78", command=clear_fields)
    button_clean.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    button_exit = ctk.CTkButton(frame_button, text="Sair", fg_color="#6C757D", hover_color="#5A6268", command=root.destroy)
    button_exit.grid(row=0, column=2, padx=5, pady=5, sticky="e")

    label_registered_titles = ctk.CTkLabel(frame_registered_items, text="Itens Cadastrados", font=ctk.CTkFont(size=16, weight="bold"))
    label_registered_titles.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

    frame_search = ctk.CTkFrame(frame_registered_items, fg_color="transparent")
    frame_search.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="e")

    entry_search = ctk.CTkEntry(frame_search, width=200, placeholder_text="Pesquisar Item...")
    entry_search.pack(side='left', padx=(0, 10))

    botao_search = ctk.CTkButton(frame_search, text="Pesquisar", command=search_item)
    botao_search.pack(side='left')


    tree = ttk.Treeview(frame_registered_items, columns=('Id', 'Nome', 'Tipo', 'Qualidade', 'Quantidade'), show="headings")
    tree.heading('Id', text='Id')
    tree.heading('Nome', text='Nome')
    tree.heading('Tipo', text='Tipo')
    tree.heading('Qualidade', text='Qualidade')
    tree.heading('Quantidade', text='Quantidade')

    tree.column('Id', width=125, anchor='center')
    tree.column('Nome', width=125)
    tree.column('Tipo', width=125)
    tree.column('Qualidade', width=125)
    tree.column('Quantidade', width=125)

    tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    
    button_edit = ctk.CTkButton(frame_registered_items, text="Editar Selecionado", command=edit_item)
    button_edit.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    button_clean_all = ctk.CTkButton(frame_registered_items, text="Remover Selecionado", command=remove_selected_item, fg_color="#D35B58", hover_color="#C77C78")
    button_clean_all.grid(row=2, column=0, padx=10, pady=10, sticky='e')


    root.mainloop()