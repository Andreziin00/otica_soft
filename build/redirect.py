import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
from pathlib import Path

# Caminho para os assets da segunda tela
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\andre\OneDrive\Área de Trabalho\otica\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Função para exibir a segunda tela
def show_second_screen():
    first_frame.pack_forget()
    create_second_screen()

# Configuração inicial da janela principal
root = tk.Tk()
root.title("Navegação entre Telas")
root.geometry("300x200")

# Primeira tela (frame)
first_frame = tk.Frame(root)
first_frame.pack(fill='both', expand=True)

label1 = tk.Label(first_frame, text="Primeira Tela")
label1.pack(pady=20)

button1 = tk.Button(first_frame, text="Ir para Segunda Tela", command=show_second_screen)
button1.pack(pady=10)

# Função para criar a segunda tela
def create_second_screen():
    second_frame = tk.Frame(root)
    second_frame.pack(fill='both', expand=True)
    
    canvas = Canvas(
        second_frame,
        bg = "#FFFFFF",
        height = 900,
        width = 1720,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        0.0,
        1720.0,
        900.0,
        fill="#D9D9D9",
        outline=""
    )

    canvas.create_text(
        52.0,
        80.0,
        anchor="nw",
        text="otica_fluid",
        fill="#000000",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        769.0,
        80.0,
        anchor="nw",
        text="entrar",
        fill="#000000",
        font=("Inter", 64 * -1)
    )

    try:
        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            second_frame,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.image = button_image_1  # Referência para evitar coleta de lixo
        button_1.place(
            x=208.0,
            y=679.0,
            width=536.0,
            height=80.0
        )
    except Exception as e:
        print(f"Erro ao carregar a imagem do botão 1: {e}")

    try:
        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            second_frame,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.image = button_image_2  # Referência para evitar coleta de lixo
        button_2.place(
            x=976.0,
            y=676.0,
            width=536.0,
            height=80.0
        )
    except Exception as e:
        print(f"Erro ao carregar a imagem do botão 2: {e}")

    try:
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        canvas.create_image(
            476.0,
            450.0,
            image=image_image_1
        )
        canvas.image_image_1 = image_image_1  # Referência para evitar coleta de lixo
    except Exception as e:
        print(f"Erro ao carregar a imagem 1: {e}")

    try:
        image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        canvas.create_image(
            1244.0,
            450.0,
            image=image_image_2
        )
        canvas.image_image_2 = image_image_2  # Referência para evitar coleta de lixo
    except Exception as e:
        print(f"Erro ao carregar a imagem 2: {e}")

    root.geometry("1720x900")
    root.configure(bg = "#FFFFFF")
    root.resizable(False, False)

# Executa a aplicação
root.mainloop()
