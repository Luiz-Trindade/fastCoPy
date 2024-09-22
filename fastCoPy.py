"""
    The MIT License (MIT)
    
    Copyright © 2024 <Luiz Gabriel Magalhães Trindade>
    
    Permission is hereby granted, free of charge, to any person obtaining a copy of this 
    software and associated documentation files (the “Software”), to deal in the Software 
    without restriction, including without limitation the rights to use, copy, modify, 
    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
    permit persons to whom the Software is furnished to do so, subject to the following 
    conditions:
    
    The above copyright notice and this permission notice shall be included in all copies 
    or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
    PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
    OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    
    Fork this project to create your own MIT license that you can always link to. 
"""

#Importação de bibliotecas
from customtkinter import *
from tkinter import filedialog
from multiprocessing import Process as task, Pool
from time import time
import shutil
import os

#Variáveis
origem          = ""
destino         = ""
listaDeArquivos = []

#Funções
#Função para exibir um alerta 
def alert(message):
    toplevel = CTkToplevel(master=app)
    toplevel.title("Alerta")
    toplevel.geometry("500x200")
    toplevel.attributes("-topmost", True)

    toplevelLabel = CTkLabel(
        master=toplevel, 
        text=message,
        font=("Arial", 15, "bold"),
    )
    toplevelLabel.pack(padx=10, pady=10)

    closeButton = CTkButton(
        master=toplevel,
        text="Fechar",
        command=toplevel.destroy
    )
    closeButton.pack(pady=10)

    toplevel.grab_set()
    toplevel.mainloop()

#Função para setar a origem
def setarOrigem():
    global origem
    origem = origemEntry.get()

    if origem == "":
        origem = filedialog.askdirectory()
        origemEntry.delete(0, "end")
        origemEntry.insert(0, origem)
        origemEntry.configure(placeholder_text="Origem:")

#Função para setar o destino
def setarDestino():
    global destino
    destino = destinoEntry.get()

    if destino == "":
        destino = filedialog.askdirectory()
        destinoEntry.delete(0, "end")
        destinoEntry.insert(0, destino)
        destinoEntry.configure(placeholder_text="Destino:")

#Função que escaneia um diretório de origem e 
#coloca os arquivos dele em uma lista
def escanearArquivos():
    global origem, listaDeArquivos

    listaDeArquivos = []  
    
    if origem:
        with os.scandir(origem) as entradas:
            for entrada in entradas:
                if entrada.is_file():
                    listaDeArquivos.append(entrada.path)

#Função que realiza a cópia
def copiarArquivo(arquivo):
    global destino, listaDeArquivos
    listaDeArquivos.remove(arquivo)
    destinoArquivo = os.path.join(destino, os.path.basename(arquivo))
    shutil.copy(arquivo, destinoArquivo)

#Função que realiza a cópia com multiprocessamento
def multiProcessamento():
    global origem, destino, listaDeArquivos

    if (origem == "") or (destino == ""):
        alert("Informe a origem e o destino!")

    else:
        start = time()
        
        try:
            escanearArquivos()
            
            cpuCores = os.cpu_count()
            with Pool(processes=cpuCores) as pool:
                #Mapeia de acordo com o número de númcleos
                #as funções e argumentos
                pool.map(copiarArquivo, listaDeArquivos)

            end = time()
            totalTime = float((end - start) / 60)
            alert(f"Arquivos copiados com sucesso!\nTempo total: {totalTime:.2f}m")

        except Exception as error:
            alert(error)

#Função para confirmar
def confirmar():
    pass

#Interface gráfica
app = CTk()
app.title("fastCoPy ⚡📁")
app.geometry("500x260")
app.resizable(False, False)

#Escala dos widgets
set_widget_scaling(1.3)
set_appearance_mode("dark")

app.grid_columnconfigure(0, weight=3)  # Primeira linha maior
app.grid_columnconfigure(1, weight=3)  # Segunda linha menor

#Entrada de origem 
origemEntry = CTkEntry(
    master=app,
    placeholder_text="Origem:",
    width=200,
    corner_radius=0
)
#origemEntry.pack(padx=10, pady=10)
origemEntry.grid(row=0, column=0, columnspan=1, padx=10, pady=10)

#Botão para setar origem
origemButton = CTkButton(
    master=app,
    text="Setar Origem 📂",
    command=setarOrigem,
    corner_radius=0
)
#origemButton.pack(padx=10, pady=10)
origemButton.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

#Entrada de destino
destinoEntry = CTkEntry(
    master=app,
    placeholder_text="Destino:",
    width=200,
    corner_radius=0
)
#destinoEntry.pack(padx=10, pady=10)
destinoEntry.grid(row=1, column=0, columnspan=1, padx=10, pady=10)

#Botão para setar destino
destinoButton = CTkButton(
    master=app,
    text="Setar Destino 📁",
    command=setarDestino,
    corner_radius=0
)
#destinoButton.pack(padx=10, pady=10)
destinoButton.grid(row=1, column=1, columnspan=1, padx=10, pady=10)

#Botão para copiar
copiarButton = CTkButton(
    master=app,
    text="Copiar! 📄",
    command=multiProcessamento,
    width=400,
    corner_radius=0,
    fg_color="green"
)
#copiarButton.pack(padx=10, pady=10)
copiarButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

criadorLabel = CTkLabel(
    master=app,
    text = "© 2024 Luiz Trindade. Todos os direitos reservados."
)
criadorLabel.grid(row=4, column=0, columnspan=2, padx=10, pady=0)

licenseLabel = CTkLabel(
    master=app,
    text = "Licenciado sob a licença MIT."
)
licenseLabel.grid(row=5, column=0, columnspan=2, padx=10, pady=0)

app.mainloop()
