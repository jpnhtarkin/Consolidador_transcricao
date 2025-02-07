import customtkinter
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import *
import os
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme('green')

root = customtkinter.CTk()
root.geometry("500x350")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill='both', expand=True)

label = customtkinter.CTkLabel(master=frame, text="Transcriptor")
label.pack(pady=12, padx=10)

# Função para executar quando o botão for clicado
def transcrever():
    #teste
    return "OK"

def lidar_com_drop(evento):
    arquivos = evento.data
    if len(arquivos) != 1:
        customtkinter.CTkFrame(text="Apenas um arquivo por vez")
        return

    caminho_do_arquivo = arquivos[0]
    tipo_do_arquivo = os.path.splitext(caminho_do_arquivo)[1].lower()
    
    if tipo_do_arquivo in ['.mp3','.mp4']:
        customtkinter.CTkCanvas(master = frame, text='Arquivo aceito\nIniciando transcrição')
        customtkinter.CTkProgressBar(master=frame)
        

button = customtkinter.CTkButton(master=frame, text="Transcrever", command=transcrever)
button.pack()

root.mainloop()
