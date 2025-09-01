import customtkinter as ctk
from tkinter import messagebox
import json
import os

def open_arquivo():
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as file:
            return json.load(file)
    else:
        with open("usuarios.json", "w") as file:
            json.dump({}, file)
            return {}
def abrir_login(on_success):
    def bnt_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        usuarios = open_arquivo()
        if usuario in usuarios and usuarios[usuario] == senha:
            root.destroy()  
            on_success()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def bnt_cancelar():
        root.destroy()  

    def bnt_cadastro():
        root.destroy()  
        abrir_cadastro()  

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Tela de Login")
    root.geometry("450x350")

    
    label_usuario = ctk.CTkLabel(root, text="Usuário:")
    label_usuario.pack(pady=(20, 5))
    entry_usuario = ctk.CTkEntry(root, placeholder_text="Digite seu usuário:")
    entry_usuario.pack(pady=5)

    label_senha = ctk.CTkLabel(root, text="Senha:")
    label_senha.pack(pady=(20, 5))
    entry_senha = ctk.CTkEntry(root, placeholder_text="Senha:", show="*")
    entry_senha.pack(pady=5)

    frame_botoes = ctk.CTkFrame(root, fg_color="transparent")
    frame_botoes.pack(pady=20)

    bnt_entra = ctk.CTkButton(frame_botoes, text="Entrar", command=bnt_login, border_width=0)
    bnt_entra.grid(row=0, column=0, padx=10)

    bnt_cancelar = ctk.CTkButton(frame_botoes, text="Cancelar", fg_color="#a83232", command=bnt_cancelar, hover_color="#F24B88", border_width=0)
    bnt_cancelar.grid(row=0, column=1, padx=10)

    
    bnt_cadastro = ctk.CTkButton(root, text="Cadastro", width=10, command=bnt_cadastro, fg_color="#007acc", hover_color="#005a99")
    bnt_cadastro.place(x=380, y=300)  

    root.mainloop()

def abrir_cadastro():
    def bnt_cadastrar():
        nome = entry_nome.get()
        email = entry_email.get()
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        usuarios = open_arquivo()

        if not nome or not email or not usuario or not senha:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
        elif usuario in usuarios:
            messagebox.showerror("Erro", "Usuário já cadastrado!")
        else:
            usuarios[usuario] = senha
            with open("usuarios.json", "w") as file:
                json.dump(usuarios, file)
            messagebox.showinfo("Sucesso", f"Cadastro de {nome} realizado com sucesso!")
            root.destroy()
            abrir_login(on_success=lambda: None)

    def bnt_cancelar():
        root.destroy() 
        abrir_login(on_success=lambda: None)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Janela de Cadastro
    root = ctk.CTk()
    root.title("Tela de Cadastro")
    root.geometry("550x600") 
  
    frame_principal = ctk.CTkFrame(root)
    frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

    # Nome Completo
    label_nome = ctk.CTkLabel(frame_principal, text="Nome Completo:", font=("Arial", 12))
    label_nome.grid(row=0, column=0, pady=10, sticky="w")
    entry_nome = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome completo", font=("Arial", 12))
    entry_nome.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

    # Email
    label_email = ctk.CTkLabel(frame_principal, text="Email:", font=("Arial", 12))
    label_email.grid(row=1, column=0, pady=10, sticky="w")
    entry_email = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu email", font=("Arial", 12))
    entry_email.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

    # Usuário
    label_usuario = ctk.CTkLabel(frame_principal, text="Usuário:", font=("Arial", 12))
    label_usuario.grid(row=2, column=0, pady=10, sticky="w")
    entry_usuario = ctk.CTkEntry(frame_principal, placeholder_text="Digite seu nome de usuário", font=("Arial", 12))
    entry_usuario.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

    # Senha
    label_senha = ctk.CTkLabel(frame_principal, text="Senha:", font=("Arial", 12))
    label_senha.grid(row=3, column=0, pady=10, sticky="w")
    entry_senha = ctk.CTkEntry(frame_principal, placeholder_text="Digite sua senha", show="*", font=("Arial", 12))
    entry_senha.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

    frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
    frame_botoes.grid(row=4, column=0, columnspan=2, pady=20)
    # Botão cadastrar
    bnt_cadastrar = ctk.CTkButton(frame_botoes, text="Cadastrar", font=("Arial", 12), command=bnt_cadastrar, width=20)
    bnt_cadastrar.grid(row=0, column=0, padx=20)
    
    # Botão cancelar
    bnt_cancelar = ctk.CTkButton(frame_botoes, text="Cancelar", font=("Arial", 12), fg_color="#a83232", command=bnt_cancelar, hover_color="#F24B88", width=20)
    bnt_cancelar.grid(row=0, column=1, padx=20)

    frame_principal.grid_columnconfigure(1, weight=1)

    root.mainloop() 
