import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

# --- Configuração da Aparência ---
# Define o tema inicial (pode ser "dark", "light" ou "system")
ctk.set_appearance_mode("dark")  
# Define o tema de cores padrão para os widgets
ctk.set_default_color_theme("blue") 

# --- Janela Principal ---
janela = ctk.CTk()
janela.geometry("950x500")
janela.title("Cadastro de Clientes com CustomTkinter")

# --- Estilização do Treeview para combinar com o tema ---
style = ttk.Style()
# Cores para o tema escuro (ajuste se usar o tema claro)
bg_color = "#2b2b2b"
text_color = "#ffffff"
selected_color = "#1f6aa5"
field_bg_color = "#2b2b2b"
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


# --- Layout da Janela (Grid) ---
janela.grid_columnconfigure(1, weight=1)
janela.grid_rowconfigure(0, weight=1)


# --- Frames ---
frame_dados_clientes = ctk.CTkFrame(janela, corner_radius=10)
frame_dados_clientes.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

frame_clientes_cadastrados = ctk.CTkFrame(janela, corner_radius=10)
frame_clientes_cadastrados.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
frame_clientes_cadastrados.grid_columnconfigure(0, weight=1)
frame_clientes_cadastrados.grid_rowconfigure(1, weight=1)

# Título para o frame de dados
label_titulo_dados = ctk.CTkLabel(frame_dados_clientes, text="Dados do Cliente", font=ctk.CTkFont(size=16, weight="bold"))
label_titulo_dados.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20))


# --- Widgets no Frame de Dados do Cliente ---

# Nome
label_nome = ctk.CTkLabel(frame_dados_clientes, text="Nome:")
label_nome.grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_nome = ctk.CTkEntry(frame_dados_clientes, width=220)
entry_nome.grid(row=1, column=1, padx=10, pady=5)

# Email
label_email = ctk.CTkLabel(frame_dados_clientes, text="Email:")
label_email.grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_email = ctk.CTkEntry(frame_dados_clientes, width=220)
entry_email.grid(row=2, column=1, padx=10, pady=5)

# Telefone (Corrigido o texto da label de "Email:" para "Telefone:")
label_telefone = ctk.CTkLabel(frame_dados_clientes, text="Telefone:")
label_telefone.grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_telefone = ctk.CTkEntry(frame_dados_clientes, width=220)
entry_telefone.grid(row=3, column=1, padx=10, pady=5)

# --- Botões ---
frame_botoes = ctk.CTkFrame(frame_dados_clientes, fg_color="transparent")
frame_botoes.grid(row=4, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
frame_botoes.grid_columnconfigure((0, 1), weight=1)

# Cadastrar e Limpar
botao_cadastrar = ctk.CTkButton(frame_botoes, text="Cadastrar")
botao_cadastrar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

botao_limpar = ctk.CTkButton(frame_botoes, text="Limpar", fg_color="#D35B58", hover_color="#C77C78")
botao_limpar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")


# --- Widgets no Frame de Clientes Cadastrados ---
# Título para o frame de clientes
label_titulo_cadastrados = ctk.CTkLabel(frame_clientes_cadastrados, text="Clientes Cadastrados", font=ctk.CTkFont(size=16, weight="bold"))
label_titulo_cadastrados.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

# Pesquisar
frame_pesquisa = ctk.CTkFrame(frame_clientes_cadastrados, fg_color="transparent")
frame_pesquisa.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="e")

entry_pesquisar = ctk.CTkEntry(frame_pesquisa, width=200, placeholder_text="Pesquisar cliente...")
entry_pesquisar.pack(side='left', padx=(0, 10))

botao_pesquisar = ctk.CTkButton(frame_pesquisa, text="Pesquisar")
botao_pesquisar.pack(side='left')


# Treeview (Tabela de Clientes)
tree = ttk.Treeview(frame_clientes_cadastrados, columns=('Id', 'Nome', 'Email', 'Telefone'), show="headings")
tree.heading('Id', text='Id')
tree.heading('Nome', text='Nome')
tree.heading('Email', text='Email')
tree.heading('Telefone', text='Telefone')

# Ajuste de largura das colunas
tree.column('Id', width=50, anchor='center')
tree.column('Nome', width=150)
tree.column('Email', width=200)
tree.column('Telefone', width=120)

tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

# Botão para remover selecionados
botao_excluir_varios = ctk.CTkButton(frame_clientes_cadastrados, text="Remover Selecionado", command=lambda: 0, fg_color="#D35B58", hover_color="#C77C78")
botao_excluir_varios.grid(row=2, column=0, padx=10, pady=10, sticky='e')


janela.mainloop()