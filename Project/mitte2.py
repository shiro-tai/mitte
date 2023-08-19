import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def processar_imagem():
    filepath = filedialog.askopenfilename()
    
    if not filepath:
        return
    
    # código Daltonismo começa aqui
    imagem1 = cv2.imread(filepath, cv2.IMREAD_COLOR)
    
    labImagem = cv2.cvtColor(imagem1, cv2.COLOR_BGR2Lab)
    # (.......)
    # termina aqui
    imagem_processada = Image.fromarray((labImagem * 255).astype('uint8'))
    imagem_tk = ImageTk.PhotoImage(imagem_processada)
    
    lbl_imagem.config(image=imagem_tk)
    lbl_imagem.imagem_tk = imagem_tk

root = tk.Tk()
root.title("Processamento de Imagem - Daltonismo")


root.geometry("800x600")  # tamanho da janela

btn_selecionar_imagem = tk.Button(root, text="Selecionar Imagem", command=processar_imagem)
btn_selecionar_imagem.pack(pady=20)

lbl_imagem = tk.Label(root)
lbl_imagem.pack()

btn_fechar = tk.Button(root, text="Fechar", command=root.quit)
btn_fechar.pack()

root.mainloop()