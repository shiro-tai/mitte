import cv2
import numpy as np
import time

anguloDeuterotopia = np.radians(-8.11)


def projetorDeuteranotopia(imagem):
    imgH, imgW, _ = imagem.shape
    imagDeut = np.zeros_like(imagem, dtype=np.float32)
    L, a, b = 0, 1, 2

    for i in range(imgH):
        for j in range(imgW):
            pixel = imagem[i, j]
            alpha = np.arctan2(pixel[a], pixel[b])
            t = np.sqrt(pixel[a] ** 2 + pixel[b] ** 2)
            lambda_val = t * np.cos(np.abs(anguloDeuterotopia - alpha))

            pixel[a] = lambda_val * np.sin(anguloDeuterotopia)
            pixel[b] = lambda_val * np.cos(anguloDeuterotopia)

            imagDeut[i, j] = pixel

    return imagDeut

start = time.time()

# Carrega a imagem
imagem8U = cv2.imread('Ishihara.jpg', cv2.IMREAD_COLOR)

# Converte para o tipo de imagem esperado pelo algoritmo
imagem = imagem8U.astype(np.float32) / 255.0

# Converte para o espaÃ§o de cores Lab
labImagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2Lab)

# Aplica o simulador de deuteranopia na imagem
deutImagem = cv2.cvtColor(projetorDeuteranotopia(labImagem), cv2.COLOR_Lab2BGR)

# Converte para o tipo de imagem de 8 bits (0-255)
deutImagem = (deutImagem * 255).astype(np.uint8)

cv2.imwrite('rgb_out.png', deutImagem)
print("Imagem Salva ............\n")
end = time.time()
tempo_total = round((end - start),3)
print("\nTempo total:",tempo_total)