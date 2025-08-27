import customtkinter as ctk
import tkinter as messagebox

def bnt_login():
    messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def bnt_cancelar():
     root.destroy()

#configure o tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#janela Principal
root = ctk.CTk()
root.title("Tela de login")
root.geometry("450x350")

#rotulo e campo usuario 
label_usuario = ctk.CTkLabel(root, text="Usuário:")
label_usuario.pack(pady=(20, 5))
entry_usuario = ctk.CTkEntry(root, placeholder_text= "Digite seu usuário:")
entry_usuario.pack(pady=5)

label_senha = ctk.CTkLabel(root, text="Senha:")
label_senha.pack(pady=(20, 5))
entry_senha = ctk.CTkEntry(root, placeholder_text= "Senha:")
entry_senha.pack(pady=5)

#frame para os botões lado a lado
frame_botoes = ctk.CTkFrame(root)
frame_botoes.pack(pady=20)

bnt_entra = ctk.CTkButton (frame_botoes, text="Entra", command=bnt_login)
bnt_entra.grid(row=0, column=0,padx=1)

bnt_cancelar = ctk.CTkButton (frame_botoes, text="cancelar",fg_color="#a83232",command=bnt_cancelar, hover_color="#F24B88")
bnt_cancelar.grid(row=0, column=1,padx=10)

root.mainloop()