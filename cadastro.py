import customtkinter as ctk
from tkinter import messagebox

def abrir_cadastro():
    # Função que vai abrir a tela de cadastro
    def bnt_cadastrar():
        nome = entry_nome.get()
        email = entry_email.get()
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        # Validação para garantir que os campos não estão vazios
        if not nome or not email or not usuario or not senha:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
        else:
            messagebox.showinfo("Sucesso", f"Cadastro de {nome} realizado com sucesso!")
            root.destroy()  # Fecha a tela de cadastro após sucesso

    def bnt_cancelar():
        root.destroy()  # Fecha a tela de cadastro sem registrar

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Janela de cadastro
    root = ctk.CTk()
    root.title("Tela de Cadastro")
    root.geometry("550x500")

    # Rótulo e campo para Nome
    label_nome = ctk.CTkLabel(root, text="Nome:")
    label_nome.pack(pady=(20, 5))  # Usando 'pack' para o layout
    entry_nome = ctk.CTkEntry(root, placeholder_text="Digite seu nome completo:")
    entry_nome.pack(pady=5)

    # Rótulo e campo para Email
    label_email = ctk.CTkLabel(root, text="Email:")
    label_email.pack(pady=(20, 5))
    entry_email = ctk.CTkEntry(root, placeholder_text="Digite seu email:")
    entry_email.pack(pady=5)

    # Rótulo e campo para Usuário
    label_usuario = ctk.CTkLabel(root, text="Usuário:")
    label_usuario.pack(pady=(20, 5))
    entry_usuario = ctk.CTkEntry(root, placeholder_text="Digite seu nome de usuário:")
    entry_usuario.pack(pady=5)

    # Rótulo e campo para Senha
    label_senha = ctk.CTkLabel(root, text="Senha:")
    label_senha.pack(pady=(20, 5))
    entry_senha = ctk.CTkEntry(root, placeholder_text="Digite sua senha:", show="*")
    entry_senha.pack(pady=5)

    # Frame para os botões (usando grid para alinhamento)
    frame_botoes = ctk.CTkFrame(root)
    frame_botoes.pack(pady=20)

    # Botões de Cadastro e Cancelar
    bnt_cadastrar = ctk.CTkButton(frame_botoes, text="Cadastrar", command=bnt_cadastrar)
    bnt_cadastrar.grid(row=0, column=0, padx=10)

    bnt_cancelar = ctk.CTkButton(frame_botoes, text="Cancelar", fg_color="#a83232", command=bnt_cancelar, hover_color="#F24B88")
    bnt_cancelar.grid(row=0, column=1, padx=10)

    root.mainloop()  # Garantir que o mainloop está sendo chamado

