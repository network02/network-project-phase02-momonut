import socket
import subprocess
import shlex
from time import sleep

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

        if response == 'Ready':
            client_data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_data.settimeout(2)
            sleep(2)
            client_data.connect((server, DATA_PORT))

            file_name = './downloads/' + request.split()[1].split('/')[-1]
            command = 'mkdir -p ./downloads/' 
            subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
            command = 'rm -rf ' + file_name
            subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
            command = 'touch ' + file_name
            subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
            try:
                with open(file_name, 'a') as f:
                    while True:
                        data = client_data.recv(1024).decode()
                        if not data:
                            break
                        f.write(data)

                client_data.close()
                response = '200 File Sent' 

            except:
                response = '400 Connection loss'

        elif 'STOR' in request.upper():
            pass
        
        elif response == '200 Goodnight!':
            print(response)
            break
        
        print(response)
    

if __name__ == '__main__':
    main()
        
