import socket

HOST = "192.168.0.192"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print(f"Conectado a {HOST}:{PORT}")

    mensaje = client_socket.recv(4096).decode()
    print(mensaje, end="")  
    username = input()
    client_socket.sendall(username.encode())

    mensaje = client_socket.recv(4096).decode()
    print(mensaje, end="")
    password = input()
    client_socket.sendall(password.encode())

    respuesta = client_socket.recv(4096).decode()
    print(respuesta, end="")
    if "incorrectas" in respuesta.lower():
        exit(0) 

    while True:
        comando = input(" ----> ")
        client_socket.sendall(comando.encode())

        if comando.lower() == "salir":
            break

        data_total = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            data_total += data
            if len(data) < 4096:
                break

        if comando.startswith("get "):
            archivo = comando.split(maxsplit=1)[1]
            with open(archivo, "wb") as f:
                f.write(data_total)
            print(f"Archivo '{archivo}' recibido y guardado.")
        else:
            print(data_total.decode(errors="ignore"))
