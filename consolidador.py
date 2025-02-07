import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import os
import openpyxl
from dotenv import load_dotenv
import numpy as np
from openai import OpenAI
from pdfminer.high_level import extract_text
import win32com.client

load_dotenv()
openai_api = os.getenv("OPENAI_API_KEY")

# Function to select directories
def selecionar_Dirarizada():
    file_path = filedialog.askopenfile(filetypes=[("Text files", "*.txt")])
    if file_path:
        dir_Dirarizada.set(file_path.name)
        
def selecionar_Nao_dia():
    file_path = filedialog.askopenfile(filetypes=[("Text files", "*.txt")])
    if file_path:
        dir_Nao_dia.set(file_path.name)




# Function to process the resume and Nao_dia profile using OpenAI's GPT
def gpt_process(Dirarizada_text, Nao_dia_text):
    client = OpenAI(api_key=openai_api)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": 'system', 'content': 'Você é um especialista de transcrições na empresa Quick Soft. Oferecemos produtos para FIDC. Os produtos são o Qcertifica, Qprof, Qconecta, Qregistro e Qgestora. Você não deve responder nada além do que foi pedido pelo usuário.'},
                {'role': 'user', 'content': '''Vou te enviar duas versões de uma mesma transcrição: uma versão diarizada e uma versão completa e não diarizada. Sua tarefa é utilizar a versão completa e não diarizada para corrigir a versão diarizada, conforme as instruções abaixo:
1. Adicione qualquer fala que esteja faltando na versão diarizada, conforme a versão completa. Indique falas faltantes com a tag 'SPEAKER FALTANTE:' e transcreva a fala completa.
2. Caso encontre erros de transcrição na versão diarizada (como falas incorretas ou palavras trocadas ou palavras faltando), corrija esses erros conforme a versão completa.
3. Não altere nada além das falas faltantes e das correções de erros conforme indicado. Não adicione comentários ou outras informações.
4. Seja bastante rigoroso com os requisitos de forma que a versão nova tenha todas as falas e palavras da não diarizada.
Está claro? Aguarde as versões para realizar o ajuste.
                '''},
                {'role': 'assistant','content': 'Claro, qual versão diarizada?'},
                {'role': 'user', 'content': Dirarizada_text},
                {'role': 'assistant','content': 'Claro, qual versão não diarizada?'},
                {'role': 'user', 'content': Nao_dia_text}
            ]
        )

        analise = response.choices[0].message.content
        return analise
    except:
        return 'Algo deu errado. Tente novamente.'
    
# Function to process the inputs and generate output
def processar(dir_Dirarizada, dir_Nao_dia):

    
    with open(dir_Dirarizada.get(), 'r', encoding='utf-8') as file:
        Dirarizada_text = file.read()
    with open(dir_Nao_dia.get(), 'r', encoding='utf-8') as file:
        Nao_dia_text = file.read()

    resposta = gpt_process( Dirarizada_text, Nao_dia_text)
    
    with open('transcrição unificada.txt', 'w', encoding='utf-8') as file:
        file.write(resposta)



################################ FRONTEND CTK ################################

# Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme('green')

app = ctk.CTk()
app.geometry("500x300")
app.title("Consolidador de Transcrições")


# Frame for selecting resume and Nao_dia profile (pdf)
mid_frame = ctk.CTkFrame(app)
mid_frame.pack(fill=X, padx=5)

top_mid_frame = ctk.CTkFrame(mid_frame)
top_mid_frame.pack(side=TOP, fill=X, pady=5, padx=5)

# Button to select resume
dir_Dirarizada = ctk.StringVar()
seletor_Dirarizada = ctk.CTkButton(top_mid_frame, text="Selecione o Dirarizada", command=selecionar_Dirarizada)
seletor_Dirarizada.pack(padx=10, pady=10, side=LEFT, expand=True)

# Button to select Nao_dia profile
dir_Nao_dia = ctk.StringVar()
seletor_Nao_dia = ctk.CTkButton(top_mid_frame, text="Selecione o Nao_dia", command=selecionar_Nao_dia)
seletor_Nao_dia.pack(padx=10, pady=10, side=RIGHT, expand=True)

bot_mid_frame = ctk.CTkFrame(mid_frame)
bot_mid_frame.pack(side=BOTTOM, fill=X, pady=5, padx=5)

# Button to process the inputs
botao_processar = ctk.CTkButton(bot_mid_frame, text="Processar", command=lambda: processar(dir_Dirarizada, dir_Nao_dia))
botao_processar.pack(padx=10, pady=10, side=RIGHT, expand=True)

app.mainloop()
