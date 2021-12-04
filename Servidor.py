import logging
import socket
from threading import Thread

from flask import Flask

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True
servidor = None

class ServidorArduinos(Thread):
    def __init__(self, host='0.0.0.0', port=6000):
        Thread.__init__(self)
        self.ip = host
        self.port = port
        self.arduinos = []
        self.start()

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # esto inicia el servidor
        serversocket.bind((self.ip, self.port))  # el bind me prende el servidor
        serversocket.listen(5)

        while True:
            socketCliente, direccionCliente = serversocket.accept()
            print('Arduino Conectado')
            self.arduinos.append(socketCliente)

    def enviarMensaje(self, mensaje):
        for arduino in self.arduinos:
            arduino.send(mensaje.encode())


@app.route('/<message>')
def sonido(message):
    print(f'Mensaje enviado al Arduino: {message}')
    servidor.enviarMensaje(message)
    return 'Ok'

if __name__ == '__main__':
    # Iniciamos el servidor socket que va a ser consumido por el arduino en el puerto 6000
    servidor = ServidorArduinos(host='0.0.0.0', port=6000)
    # Iniciamos la API REST que va a ser consumida por la aplicacion movil en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
