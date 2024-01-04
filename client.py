import socket
import subprocess
import shlex

host = "localhost"
server = "localhost"
control_port = 8021
data_port = 8020

def send(request):
    try:
        client_ctrl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_ctrl.settimeout(1)
        client_ctrl.connect((server, control_port))
        client_ctrl.sendall(request.encode())
        response = client_ctrl.recv(1024).decode()
        client_ctrl.close()

    except:
        response = "server is offline!!"

    return response
    
def main():



    while True:
        request = input().strip()
        response = send(request)
        if response == "server is offline!!":
            print(response)
            break


        if "RETR" in request.upper():
            client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_data.bind((host, data_port))
            client_data.listen(1)
            file_name = request.strip().split()[1].split("/")[-1]
            command = 'mkdir ./download/' 
            response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
            command = 'touch ' + file_name
            response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
            with open(f'./download/{file_name}', 'ab') as f:
                while True:
                    server_socket, server_address = client_data.accept()
                    server_host = socket.gethostbyaddr(server_address[0])[0]
                    data = server_socket.recv(1024).decode()
                    f.write(data)
                    
                    #TODO when is file finished?
                    server_socket.sendall(response.encode())
                    server_socket.close()
                    break


        elif "STOR" in request.upper():
            pass

        
        print(response)
    



if __name__ == "__main__":
    main()
        