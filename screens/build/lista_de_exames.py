import sqlite3
from tkinter import Tk, Canvas, Button, ttk, Entry, messagebox

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

# Configuração da janela principal
window = Tk()
window.title("Lista de Clientes")
window.geometry("1200x600")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
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
tree = ttk.Treeview(window, columns=columns, show="headings")
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
entry_search = Entry(window, font=("Arial", 14))
entry_search.place(x=900, y=50, width=250, height=30)

button_search = Button(
    window,
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
    window,
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
    window,
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
    window,
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
    window,
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

window.mainloop()
