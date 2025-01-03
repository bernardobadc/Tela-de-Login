from PIL import Image
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
import hashlib

# Criando o banco de dados e suas operações
def setup_database():
    conn = sqlite3.connect("banco_usuarios.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT UNIQUE NOT NULL,
        password TEXT UNIQUE NOT NULL
        )'''
    )
    
    conn.commit()
    conn.close()

# Criando messageboxes do tkinter pra sinalizar se o registro foi efetuado com sucesso, ou não
def show_msg():
    messagebox.showinfo("Sucesso!", "Usuário registrado com sucesso!")

def show_error():
    messagebox.showerror("Erro!", "Usuário já existente!")

# Função de Login
def login():
    username = login_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning(title="Atenção!", message="Atenção, por favor preencha todos os campos!")
        return
    conn = sqlite3.connect("banco_usuarios.db")
    cursor = conn.cursor()

    # Hash da senha inserida para comparação
    password_hashed = hash_password(password)

    # Fazendo o SELECT pra verificar usuário e senha, e fechando a conexão com o banco
    cursor.execute("SELECT * FROM users WHERE user = ? AND password = ?", (username, password_hashed))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo(title="Login Realizado",message=f"Login bem sucedido, bem vindo(a) {username}!")
    else:
        messagebox.showerror(title="Falha no Login",message="Houve uma falha no Login. Usuário ou senha incorretos!")

# Registrar usuário
def user_register(username, password):
    conn = sqlite3.connect("banco_usuarios.db")
    cursor = conn.cursor()

    # Criptografando a senha antes de armazená-la
    password_hashed = hash_password(password)
    try:
        cursor.execute('''INSERT INTO users (user, password) VALUES (?, ?)''', (username, password_hashed))
        conn.commit()
        show_msg()
    except sqlite3.IntegrityError:
        show_error()
    finally:
        conn.close()

setup_database()

# Hash para a senha
def hash_password(password):
    # Gera um código hash SHA para a senha
    return hashlib.sha256(password.encode()).hexdigest()

# Definindo variáveis de cores
light_blue = "#2a93f5"
dark_blue = "#0f094a"
frame_color = "#05011c"

# Função de hover do botão login
def on_enter_login(event):
    login_btn.configure(cursor="hand2")

# Criando tela de registro ao clicar no botão "Registrar-se"
def register_btn():
    window.withdraw()

    # Criando a janela de registro
    ctk.set_appearance_mode("dark")
    register_window = ctk.CTk()
    register_window.title("Tela de Login")
    register_window.geometry("350x300")
    register_window.resizable(width=False, height=False)
    register_window.iconbitmap("assets/login_icon.ico")


    username_label = ctk.CTkLabel(register_window, text="Crie um usuário", font=("Arial", 14), text_color=light_blue)
    username_label.place(relx=0.5, y=50, anchor="center")

    # Definindo a variável username_entry dentro da função
    username_entry = ctk.CTkEntry(register_window, 
                                    placeholder_text="Nome de usuário",
                                    font=("Arial", 12),
                                    fg_color=dark_blue,
                                    border_width=2,
                                    border_color=light_blue,
                                    corner_radius=15,
                                    width=240,
                                    height=30)
    username_entry.place(relx=0.5, y=87, anchor="center")

    password_label = ctk.CTkLabel(register_window, text="Crie uma senha", font=("Arial", 14), text_color=light_blue)
    password_label.place(relx=0.5, y=135, anchor="center")

    # Definindo a variável password_entry dentro da função
    password_entry = ctk.CTkEntry(register_window, 
                                    placeholder_text="Senha",
                                    show="*",
                                    font=("Arial", 12),
                                    fg_color=dark_blue,
                                    border_width=2,
                                    border_color=light_blue,
                                    corner_radius=15,
                                    width=240,
                                    height=30)
    password_entry.place(relx=0.5, y=170, anchor="center")

    # Criando botão de registrar
    register_btn = ctk.CTkButton(register_window,
                                    text="Registrar",
                                    font=("Arial", 14),
                                    width=100,
                                    height=30,
                                    )
    register_btn.place(relx=0.5, y=220, anchor="center")
    # Criando bind para evento de clique no botão de Registrar
    register_btn.bind("<Button-1>", lambda e: user_register(username_entry.get(), password_entry.get()))

    # Criando botão de voltar para tela de Login
    back_to_login_btn = ctk.CTkButton(register_window,
                                text="Retornar para Login",
                                font=("Arial", 14),
                                text_color="white",
                                width=70,
                                height=25,
                                command=lambda: (window.deiconify(), register_window.destroy()))
    back_to_login_btn.place(relx=0.5, y=270, anchor="center")

    register_window.mainloop()


# Funções de hover do botão registrar-se na tela de login
def on_enter_register(event):
    register_label.configure(font=("Arial", 14, "underline"))
    register_label.configure(cursor="hand2")

def on_leave_register(event):
    register_label.configure(font=("Arial", 13))

# Definindo as propriedades da janela
ctk.set_appearance_mode("dark")
window = ctk.CTk()
window.title("Tela de Login")
window.geometry("350x350")
window.resizable(width=False, height=False)
window.iconbitmap("assets/login_icon.ico")

# Carregando a imagem
image = ctk.CTkImage(Image.open("assets/login_image.png"), size=(70, 70))

# Criando a label da imagem para mostrá-la
image_label = ctk.CTkLabel(window, image=image, text="")
image_label.place(relx=0.5, y=35, anchor="center")

# Criando o frame com as entrys e labels de login e senha
main_frame = ctk.CTkFrame(window, width=280, height=200, fg_color=frame_color, corner_radius=15)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Criando as entrys e labels de login

# Login
login_label = ctk.CTkLabel(main_frame, text="Usuário", font=("Arial", 14), text_color=light_blue)
login_label.place(relx=0.5, y=30, anchor="center")

login_entry = ctk.CTkEntry(main_frame, 
                           placeholder_text="Usuário",
                           font=("Arial", 12),
                           fg_color=dark_blue,
                           border_width=2,
                           border_color=light_blue,
                           corner_radius=15,
                           width=240,
                           height=30)
login_entry.place(relx=0.5, y=67, anchor="center")

# Senha
password_label = ctk.CTkLabel(main_frame, text="Senha", font=("Arial", 14), text_color=light_blue)
password_label.place(relx=0.5, y=115, anchor="center")

password_entry = ctk.CTkEntry(main_frame, 
                           placeholder_text="Senha",
                           show="*",
                           font=("Arial", 12),
                           fg_color=dark_blue,
                           border_width=2,
                           border_color=light_blue,
                           corner_radius=15,
                           width=240,
                           height=30)
password_entry.place(relx=0.5, y=150, anchor="center")

# Criando o botão de login
login_btn = ctk.CTkButton(window,
                          text="Login",
                          font=("Arial", 14),
                          fg_color="black",
                          hover_color="#0e054a",
                          width=100,
                          height=30,
                          command=login)

login_btn.place(relx=0.5, y=300, anchor="center")

# Adicionando efeito hover e função ao botão de Login
# login_btn.bind("<Button-1>", lambda e: logar())
login_btn.bind("<Enter>", on_enter_login)


# Criando uma label parecida com um link para ser o botão de "Registrar-se"
register_label = ctk.CTkLabel(window, 
                              text="Registrar-se",
                              font=("Arial", 13)
                              )
register_label.place(relx=0.5, y=330, anchor="center")

# Adicionando efeito hover e função ao botão de "Registrar-se"
register_label.bind("<Enter>", on_enter_register)
register_label.bind("<Leave>", on_leave_register)
register_label.bind("<Button-1>", lambda e: register_btn())

window.mainloop()