import cv2
import tkinter as tk
from PIL import Image, ImageTk, Image, ImageGrab
import time
import keyboard
import numpy as np
import math

anguloDeuterotopia = math.radians(-8.11)
L = 0
A = 1
B = 2
largura = 0
altura = 0
contOperacao = 0
anguloRotacao = 0

pixelOriginal = [0.0, 0.0, 0.0]
pixelVizinho = [0.0, 0.0, 0.0]
pixelOriginalDet = [0.0, 0.0, 0.0]
pixelVizinhoDet = [0.0, 0.0, 0.0]

distOriginalVizinho = 0.0
distOriginalVizinhoDet = 0.0
direcaoPerdaContraste = 0.0
newPixel = [0.0, 0.0, 0.0]
oldPixel = [0.0, 0.0, 0.0]
senoAngRotacao = 0.0
cossenoAngRotacao = 0.0


def projetorDeuteranotopia(imagem):
    imgH = imagem.shape[0]
    imgW = imagem.shape[1]
    imagDeut = imagem.copy()
    pixel = [0.0, 0.0, 0.0]
    pixel_new = [0.0, 0.0, 0.0]
    a = 1
    b = 2
    alpha = 0.0
    t = 0.0
    lambda_ = 0.0

    for i in range(imgH):
        for j in range(imgW):
            pixel = imagem[i, j]
            
            alpha = math.atan2(pixel[a], pixel[b])
            t = math.sqrt(math.pow(pixel[a], 2) + math.pow(pixel[b], 2))

            lambda_ = t * math.cos(math.fabs(anguloDeuterotopia - alpha))

            pixel_new[a] = lambda_ * math.sin(anguloDeuterotopia)
            pixel_new[b] = lambda_ * math.cos(anguloDeuterotopia)
            
            imagDeut[i, j] = [pixel[0],pixel_new[a],pixel_new[b]]
            

    return imagDeut



def processamento(labImagem_32FC3):
    global largura, altura, matrizPerdaContraste, contOperacao, anguloRotacao
    
    labImagem_32FC3_Simulado = projetorDeuteranotopia(labImagem_32FC3)
    
 
    altura = labImagem_32FC3.shape[0]
    largura = labImagem_32FC3.shape[1]
    variance = (2 / np.pi) * np.sqrt(2 * min(largura, altura))
    
    matrizPerdaContraste = np.zeros((altura * largura, 2))
    contOperacao = 0

    for ROW in range(altura):
        for COL in range(largura):
            pixelOriginal = labImagem_32FC3[ROW, COL]
            
            posicaoGaussiana = CalcDistriGauss(COL, ROW, largura, altura,variance)
      
            pixelVizinho = labImagem_32FC3[posicaoGaussiana[1], posicaoGaussiana[0]]
            
            pixelOriginalDet = labImagem_32FC3_Simulado[ROW, COL]
            
            pixelVizinhoDet = labImagem_32FC3_Simulado[posicaoGaussiana[1], posicaoGaussiana[0]]
            
            distOriginalVizinho = math.sqrt((pixelOriginal[A] - pixelVizinho[A]) ** 2 + (pixelOriginal[B] - pixelVizinho[B]) ** 2)       
            distOriginalVizinhoDet = math.sqrt((pixelOriginalDet[A] - pixelVizinhoDet[A]) ** 2 + (pixelOriginalDet[B] -pixelVizinhoDet[B]) **2) 


            if distOriginalVizinho == 0:
                
                direcaoPerdaContraste = 0
            else:
                
                direcaoPerdaContraste = (distOriginalVizinho - distOriginalVizinhoDet) / distOriginalVizinho

            matrizPerdaContraste[contOperacao][0] = (pixelOriginal[A] - pixelVizinho[A]) * direcaoPerdaContraste
            matrizPerdaContraste[contOperacao][1] = (pixelOriginal[B] - pixelVizinho[B]) * direcaoPerdaContraste
            
            contOperacao += 1

    matriztransposta = np.transpose(matrizPerdaContraste)
    
    
    matrizFinal = matriztransposta @ matrizPerdaContraste 
    
    autovalores, autovetores = np.linalg.eig(matrizFinal)
    
    
    if autovetores[0][0] > autovetores[1][0]:
        anguloRotacao = math.atan2(autovetores[0][0], autovetores[0][1])
    else:
        anguloRotacao = math.atan2(autovetores[1][0], autovetores[1][1])
    
    return rotacionaImagem(labImagem_32FC3, anguloRotacao)


def rotacionaImagem(imagemLab, angRotacao):
    global senoAngRotacao, cossenoAngRotacao

    imagemFinal = imagemLab.copy()

    senoAngRotacao = math.sin(angRotacao)
    cossenoAngRotacao = math.cos(angRotacao)

    altura = imagemLab.shape[0]
    largura = imagemLab.shape[1]

    for ROW in range(altura):
        for COL in range(largura):
            oldPixel = imagemLab[ROW, COL]

            newPixel[L] = oldPixel[L]
            newPixel[A] = oldPixel[B] * senoAngRotacao + oldPixel[A] * cossenoAngRotacao
            newPixel[B] = oldPixel[B] * cossenoAngRotacao - oldPixel[A] * senoAngRotacao

            imagemFinal[ROW, COL] = newPixel

    return imagemFinal



def CalcDistriGauss(coluna, linha, largura, altura,variance):    
    np.random.seed()    
    # Gerar amostras aleatórias seguindo a distribuição gaussiana
    deslocamento_coluna = np.random.normal(loc=0, scale= np.sqrt(variance))
    deslocamento_linha = np.random.normal(loc=0, scale= np.sqrt(variance))

        
    # Calcular as coordenadas do pixel vizinho
    vizinho_coluna = coluna + int(round(deslocamento_coluna))
    vizinho_linha = linha + int(round(deslocamento_linha))
    
    # Verificar se as coordenadas estão dentro dos limites da imagem
    vizinho_coluna = max(0, min(vizinho_coluna, largura - 1))
    vizinho_linha = max(0, min(vizinho_linha, altura - 1))

    neighborCoordinates = [vizinho_coluna,vizinho_linha]
        
    return neighborCoordinates 

def salvar_screenshot():
    janela.iconify()

    keyboard.press_and_release('windows+shift+s')
    time.sleep(5)
    pil_screenshot = ImageGrab.grabclipboard()
    numpy_screenshot = np.array(pil_screenshot)
    cv_screenshot = cv2.cvtColor(numpy_screenshot, cv2.COLOR_RGB2BGR)
    imagem1 = cv2.cvtColor(cv_screenshot, cv2.IMREAD_COLOR)
    imagem2 = cv2.normalize(imagem1, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    labImagem = cv2.cvtColor(imagem2, cv2.COLOR_BGR2Lab)

    imagem3 = processamento(labImagem)

    imagem4 = cv2.cvtColor(imagem3, cv2.COLOR_Lab2BGR)
    deutImagem = (cv2.normalize(imagem4, None, 0, 255, cv2.NORM_MINMAX)).astype('uint8')
    imagem_tk = tk.PhotoImage(data=cv2.imencode('.ppm', deutImagem)[1].tobytes())

    lbl_imagem.config(image=imagem_tk)
    lbl_imagem.imagem_tk = imagem_tk
    
    nova_largura = cv_screenshot.shape[1] + 100  # Adicione espaço extra
    nova_altura = cv_screenshot.shape[0] + 150 # Adicione espaço extra
    janela.geometry(f"{nova_largura}x{nova_altura}")

    janela.deiconify()


def sair():
    janela.quit()
    janela.destroy()


janela = tk.Tk()
janela.title("Captura de Tela em Escala de Cinza")
janela.geometry("800x650")

botao_salvar = tk.Button(janela, text="Capturar e Salvar imagem processada", command=salvar_screenshot)
botao_salvar.pack(pady=20)

lbl_imagem = tk.Label(janela)
lbl_imagem.pack()

botao_sair = tk.Button(janela, text="Sair", command=sair)
botao_sair.pack(pady=20)


janela.mainloop()