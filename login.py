import customtkinter as ctk
from tkinter import messagebox
import cadastro 

def abrir_login(on_success):
    def bnt_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if usuario == "admin" and senha == "123":
            root.destroy()  
            on_success()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def bnt_cancelar():
        root.destroy()  

    def bnt_cadastro():
        root.destroy()  
        cadastro.abrir_cadastro()  

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

    frame_botoes = ctk.CTkFrame(root)
    frame_botoes.pack(pady=20)

    bnt_entra = ctk.CTkButton(frame_botoes, text="Entrar", command=bnt_login)
    bnt_entra.grid(row=0, column=0, padx=1)

    bnt_cancelar = ctk.CTkButton(frame_botoes, text="Cancelar", fg_color="#a83232", command=bnt_cancelar, hover_color="#F24B88")
    bnt_cancelar.grid(row=0, column=1, padx=10)

    
    bnt_cadastro = ctk.CTkButton(root, text="Cadastro", width=10, command=bnt_cadastro, fg_color="#007acc", hover_color="#005a99")
    bnt_cadastro.place(x=380, y=300)  

    root.mainloop()
