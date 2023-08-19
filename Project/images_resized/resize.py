
import cv2

imagem_entrada = cv2.imread("Completa.png", cv2.IMREAD_COLOR)

imagem_Redimensionada = cv2.resize(imagem_entrada, (150, 112), interpolation= cv2.INTER_CUBIC)
cv2.imwrite("saida_150x112.jpg", imagem_Redimensionada)

imagem_Redimensionada = cv2.resize(imagem_entrada, (150, 156), interpolation= cv2.INTER_CUBIC)
cv2.imwrite("saida_150x156.jpg", imagem_Redimensionada)

imagem_Redimensionada = cv2.resize(imagem_entrada, (160, 206), interpolation= cv2.INTER_CUBIC)
cv2.imwrite("saida_160x206.jpg", imagem_Redimensionada)

imagem_Redimensionada = cv2.resize(imagem_entrada, (294, 235), interpolation= cv2.INTER_CUBIC)
cv2.imwrite("saida_294x235.jpg", imagem_Redimensionada)

imagem_Redimensionada = cv2.resize(imagem_entrada, (420, 233), interpolation= cv2.INTER_CUBIC)
cv2.imwrite("saida_420x233.jpg", imagem_Redimensionada)

imagem_Redimensionada = cv2.resize(imagem_entrada, (375, 390), interpolation= cv2.INTER_CUBIC)
cv2.imwrite("saida_375x390.jpg", imagem_Redimensionada)

imagem_Redimensionada = cv2.resize(imagem_entrada, (612, 300), interpolation= cv2.INTER_CUBIC)
cv2.imwrite("saida_612x300.jpg", imagem_Redimensionada)

imagem_Redimensionada = cv2.resize(imagem_entrada, (1632, 1224), interpolation= cv2.INTER_CUBIC)
cv2.imwrite("saida_1632x1224.jpg", imagem_Redimensionada)
