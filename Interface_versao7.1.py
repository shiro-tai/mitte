#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tkinter as tk


def salvar_screenshot():
    import time
    import pyautogui
    from PIL import Image, ImageOps

   
    janela.iconify()
    
    time.sleep(3)
    screenshot = pyautogui.screenshot()

    # Converter a captura de tela para escala de cinza
    # No lugar dessa linha vai entrar nosso código do daltonismo
    screenshot_gray = ImageOps.grayscale(screenshot)

  
    screenshot_gray.save('imagem_processada.png')

   
    janela.deiconify()


def sair():
    janela.quit()
    janela.destroy()


janela = tk.Tk()
janela.title("Captura de Tela em Escala de Cinza")
janela.geometry("500x200")

botao_salvar = tk.Button(janela, text="Capturar e Salvar imagem processada", command=salvar_screenshot)
botao_salvar.pack(pady=20)


botao_sair = tk.Button(janela, text="Sair", command=sair)
botao_sair.pack(pady=20)


janela.mainloop()


# In[ ]:




