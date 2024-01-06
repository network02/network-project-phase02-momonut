import socket
import subprocess
import shlex

host = 'localhost'
server = 'localhost'
DATA_PORT = 8020 
CTRL_PORT = 8021

def send(request):
    try:
        client_ctrl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_ctrl.settimeout(2)
        client_ctrl.connect((server, CTRL_PORT))
        client_ctrl.sendall(request.encode())
        response = client_ctrl.recv(1024).decode()
        client_ctrl.close()

    except:
        response = 'server is offline!!'

    return response
    
def main():
    request = '!HELLO!'
    response = send(request)
    print(response)
    while True:
        request = input().strip()
        response = send(request)
        if response == 'server is offline!!':
            print(response)
            break

        if 'RETR' in request.upper():
            client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_data.bind((host, DATA_PORT))
            client_data.listen(1)
            print(f'listening on ftp://{host}:{DATA_PORT}')
            server_socket, server_address = client_data.accept()
            print(f'port {DATA_PORT} opened')

            file_name = request.strip().split()[1].split('/')[-1]
            command = 'mkdir -p ./downloads/' 
            response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
            command = 'rm -rf ' + file_name
            response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
            command = 'touch ' + file_name
            response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
            with open(f'./downloads/{file_name}', 'ab') as f:
                while True:
                    data = server_socket.recv(1024).decode()
                    if not data:
                        break
                    f.write(data)

            server_socket.close()

        elif 'STOR' in request.upper():
            pass
        
        elif response == '200 Goodnight!':
            print(response)
            break
        
        print(response)
    

if __name__ == '__main__':
    main()
        
