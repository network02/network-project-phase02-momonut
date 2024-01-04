import socket

def main():
    host = "localhost"
    server = "localhost"
    control_port = 21
    data_port = 20


    is_online = True
    try:
        client_ctrl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_ctrl.settimeout(1)
        client_ctrl.connect((server, control_port))
    except:
        response = "server is offline!!"
        is_online = False

    while is_online:
        request = input().strip()
        try:
            client_ctrl.sendall(request.encode())
            response = client_ctrl.recv(1024).decode()

        except:
            response = "server is offline!!"
            is_online = False
            break

        if "RETR" in request.to_upper():
            client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_data.bind((host, data_port))
            client_data.listen(1)
            while True:
                server_socket, server_address = client_data.accept()
                server_host = socket.gethostbyaddr(client_address[0])[0]
                request = client_socket.recv(1024).decode()
                client_socket.sendall(response.encode())
                client_socket.close()


        elif "STOR" in request.to_upper():
            pass

        
        print(response)
    
    client.close()



if __name__ == "__main__":
    main()
        