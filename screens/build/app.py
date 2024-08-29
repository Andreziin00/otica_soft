import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import Tk, ttk, Canvas, Entry, Button, PhotoImage, messagebox
import re  # Importa o módulo para usar expressões regulares

#funcoes da TELA PRINCIPAL

# Função para criar a tabela no banco de dados
def criar_tabela():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Exames (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            rg TEXT NOT NULL,
            cpf TEXT NOT NULL,
            endereco TEXT NOT NULL,
            oe TEXT,
            od TEXT,
            status BOOLEAN NOT NULL
        )
    ''')
    conn.commit()

# Função para verificar se o nome contém apenas letras e espaços
def validar_nome(nome):
    return bool(re.match("^[A-Za-z\s]+$", nome))

# Função para verificar se o RG contém exatamente 8 dígitos
def validar_rg(rg):
    return bool(re.match("^\d{8}$", rg))

# Função para verificar se o CPF contém exatamente 11 dígitos
def validar_cpf(cpf):
    return bool(re.match("^\d{11}$", cpf))

# Função para verificar se o endereço tem no máximo 60 caracteres
def validar_endereco(endereco):
    return len(endereco) <= 60

# Função para inserir os dados no banco de dados
def salvar_dados():
    nome = entry_1.get()
    rg = entry_4.get()
    cpf = entry_3.get()
    endereco = entry_2.get()
    oe = ""  # OE pode ser vazio
    od = ""  # OD pode ser vazio

    # Verifica se os campos estão preenchidos corretamente
    if not validar_nome(nome):
        messagebox.showerror("Erro", "O nome deve conter apenas letras e espaços.")
        return
    if not validar_rg(rg):
        messagebox.showerror("Erro", "O RG deve conter exatamente 8 dígitos numéricos.")
        return
    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "O CPF deve conter exatamente 11 dígitos numéricos.")
        return
    if not validar_endereco(endereco):
        messagebox.showerror("Erro", "O endereço deve ter no máximo 60 caracteres.")
        return

    # Define o status
    status = True  # Todos os campos obrigatórios estão preenchidos

    # Insere os dados no banco de dados
    cursor.execute('''
        INSERT INTO Exames (nome, rg, cpf, endereco, oe, od, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, rg, cpf, endereco, oe, od, status))

    conn.commit()
    messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

# Caminho para os arquivos
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\andre\OneDrive\Área de Trabalho\otica\screens\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Função para exibir a segunda tela
def show_second_screen():
    window.pack_forget()
    create_second_screen()

#FUNCAO QUE CRIA A TELA DE EXAMES
def create_second_screen():

    #FUNCOES TELA DE EXAMES
    def carregar_dados(status_filter=None):
        # Limpa os dados existentes no Treeview
        for i in tree.get_children():
            tree.delete(i)
        
        # Define a query com base no filtro de status
        query = "SELECT * FROM Exames"
        if status_filter == "incompletos":
            query += " WHERE Status = 1"
        elif status_filter == "completos":
            query += " WHERE Status = 0"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            status_text = "Incompleto" if row[7] == 1 else "Completo"
            tree.insert("", "end", values=row[:7] + (status_text,))  # Adiciona o status como último valor

    def deletar_dado(id):
        confirm = messagebox.askyesno("Confirmação", "Deseja realmente excluir este registro?")
        if confirm:
            cursor.execute("DELETE FROM Exames WHERE ID = ?", (id,))
            conn.commit()
            carregar_dados()

    def pesquisar():
        search_term = entry_search.get()
        query = "SELECT * FROM Exames WHERE Nome LIKE ?"
        cursor.execute(query, ('%' + search_term + '%',))
        rows = cursor.fetchall()
        
        for i in tree.get_children():
            tree.delete(i)
        
        for row in rows:
            status_text = "Completo" if row[6] == 1 else "Incompleto"
            tree.insert("", "end", values=row[:7] + (status_text,))

    def filtrar_completos():
        carregar_dados("completos")

    def filtrar_incompletos():
        carregar_dados("incompletos")

    # Função para excluir o item selecionado
    def excluir():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Selecione um registro para excluir.")
            return

        item_id = tree.item(selected_item[0], "values")[0]  # Assume que o ID é a primeira coluna
        deletar_dado(item_id)

        window_exams.mainloop()

    #CONFIGURACOES DA TELA DE EXAMES
    window_exams = tk.Tk()
    window_exams.title("Lista de Clientes")
    window_exams.geometry("1200x600")
    window_exams.configure(bg="#FFFFFF")

    canvas = Canvas(
        window_exams,
        bg="#FFFFFF",
        height=600,
        width=1200,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Conexão com o banco de dados SQLite
    conn = sqlite3.connect('dados_exames.db')
    cursor = conn.cursor()

    # Criação do Treeview
    columns = ("ID", "Nome", "RG", "CPF", "Endereço", "OE", "OD", "Status")
    tree = ttk.Treeview(window_exams, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("RG", text="RG")
    tree.heading("CPF", text="CPF")
    tree.heading("Endereço", text="Endereço")
    tree.heading("OE", text="OE")
    tree.heading("OD", text="OD")
    tree.heading("Status", text="Status")
    tree.column("ID", width=50)
    tree.column("Nome", width=150)
    tree.column("RG", width=100)
    tree.column("CPF", width=100)
    tree.column("Endereço", width=200)
    tree.column("OE", width=50)
    tree.column("OD", width=50)
    tree.column("Status", width=100)

    tree.place(x=50, y=50, width=800, height=400)

    # Barra de pesquisa
    entry_search = Entry(window_exams, font=("Arial", 14))
    entry_search.place(x=900, y=50, width=250, height=30)

    button_search = Button(
        window_exams,
        text="Pesquisar",
        borderwidth=0,
        highlightthickness=0,
        command=pesquisar,
        relief="flat",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12)
    )
    button_search.place(x=900, y=90, width=250, height=30)

    # Botão para carregar os dados
    button_load = Button(
        window_exams,
        text="Carregar Dados",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: carregar_dados(),
        relief="flat",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12)
    )
    button_load.place(x=900, y=130, width=250, height=30)

    # Botões de filtro
    button_completos = Button(
        window_exams,
        text="Completos",
        borderwidth=0,
        highlightthickness=0,
        command=filtrar_completos,
        relief="flat",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12)
    )
    button_completos.place(x=900, y=170, width=120, height=30)

    button_incompletos = Button(
        window_exams,
        text="Incompletos",
        borderwidth=0,
        highlightthickness=0,
        command=filtrar_incompletos,
        relief="flat",
        bg="#F44336",
        fg="white",
        font=("Arial", 12)
    )
    button_incompletos.place(x=1030, y=170, width=120, height=30)

    # Botão para excluir dados (mais discreto)
    button_delete = Button(
        window_exams,
        text="Excluir",
        borderwidth=0,
        highlightthickness=0,
        command=excluir,
        relief="flat",
        bg="#F44336",
        fg="white",
        font=("Arial", 12)
    )
    button_delete.place(x=900, y=210, width=250, height=30)

    # Carregar os dados ao iniciar
    carregar_dados()

# Configuração da janela principal

# Configuração inicial da janela principal

window = tk.Tk()
window.title("formulario de dados 1")
window.geometry("1720x900")
window.configure(bg="#FFFFFF")

# Primeira tela (frame)
first_frame = tk.Frame(window)
first_frame.pack(fill='both', expand=True)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=900,
    width=1720,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    1720.0,
    900.0,
    fill="#D9D9D9",
    outline=""
)

canvas.create_text(
    71.0,
    75.0,
    anchor="nw",
    text="otica_fluid_atendimento",
    fill="#000000",
    font=("Inter", 24 * -1)
)

canvas.create_text(
    71.0,
    212.0,
    anchor="nw",
    text="nome",
    fill="#000000",
    font=("Inter", 24 * -1)
)

canvas.create_text(
    73.0,
    452.0,
    anchor="nw",
    text="CPF",
    fill="#000000",
    font=("Inter", 24 * -1)
)

canvas.create_text(
    71.0,
    572.0,
    anchor="nw",
    text="endereço",
    fill="#000000",
    font=("Inter", 24 * -1)
)

canvas.create_text(
    72.0,
    332.0,
    anchor="nw",
    text="RG",
    fill="#000000",
    font=("Inter", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    649.0,
    227.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=344.0,
    y=193.0,
    width=610.0,
    height=66.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    649.0,
    587.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=344.0,
    y=553.0,
    width=610.0,
    height=66.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    649.0,
    467.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=344.0,
    y=433.0,
    width=610.0,
    height=66.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    649.0,
    347.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=344.0,
    y=313.0,
    width=610.0,
    height=66.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=salvar_dados,  # Chama a função para salvar os dados
    relief="flat"
)
button_1.place(
    x=683.0,
    y=712.0,
    width=250.0,
    height=80.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command= create_second_screen, #Chama a função para alternar tela
    relief="flat"
)
button_2.place(
    x=1383.0,
    y=112.0,
    width=250.0,
    height=80.0
)

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('dados_exames.db')
cursor = conn.cursor()

# Criação da tabela (caso ainda não exista)
criar_tabela()

window.resizable(False, False)
window.mainloop()
