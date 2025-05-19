from keras.models import load_model  # TensorFlow é necessário para o Keras funcionar
import cv2  # Instalar opencv-python
import numpy as np

# Desabilitar notação científica para clareza
np.set_printoptions(suppress=True)

# Carregar o modelo
model = load_model("keras_model.h5", compile=False)

# Carregar os rótulos (labels)
class_names = open("labels.txt", "r").readlines()

# A CÂMERA pode ser 0 ou 1, dependendo da câmera padrão do seu computador
camera = cv2.VideoCapture(0)

# Definir o nome da janela e o tamanho desejado para a janela
window_name = "Imagem da Webcam"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Permite redimensionar a janela
cv2.resizeWindow(window_name, 640, 480)  # Ajuste o tamanho da janela aqui (por exemplo, 640x480)

while True:
    # Capturar a imagem da webcam
    ret, image = camera.read()

    # Verificar se a captura foi bem-sucedida
    if not ret:
        print("Falha ao capturar imagem da câmera.")
        break

    # Redimensionar a imagem para (224x224) para o modelo
    resized_image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Transformar a imagem em um array numpy e redimensioná-la para o formato de entrada do modelo
    input_image = np.asarray(resized_image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalizar o array da imagem
    input_image = (input_image / 127.5) - 1

    # Fazer a previsão com o modelo
    prediction = model.predict(input_image)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()  # Remover qualquer newline extra do rótulo
    confidence_score = prediction[0][index]

    # Exibir a classe e a pontuação de confiança na imagem
    label = f"{class_name}: {np.round(confidence_score * 100, 2)}%"

    # Desenhar um retângulo em toda a imagem (simulação de detecção de objeto)
    height, width, _ = image.shape
    cv2.rectangle(image, (10, 10), (width - 10, height - 10), (0, 255, 0), 2)

    # Adicionar o texto com o rótulo na imagem
    cv2.putText(image, label, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Mostrar a imagem com o rótulo na janela
    cv2.imshow(window_name, image)

    # Ouvir o teclado para teclas pressionadas
    keyboard_input = cv2.waitKey(1)

    # 27 é o código ASCII para a tecla ESC no teclado
    if keyboard_input == 27:
        break

# Liberar a câmera e fechar as janelas
camera.release()
cv2.destroyAllWindows()