import socket
import subprocess
import shlex

server = 'localhost'
DATA_PORT = 8020 
CTRL_PORT = 8021
BUFFER_SIZE = 1024

def send(request):
    try:
        control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        control_socket.settimeout(2)
        control_socket.connect((server, CTRL_PORT))
        control_socket.sendall(request.encode())
        response = control_socket.recv(1024).decode()
        control_socket.close()

    except:
        response = 'server is offline!!'

    return response
    
def main():
    request = 'HELP'
    response = send(request)
    print(response)
    while True:
        request = input().strip()
        response = send(request)
        if response == 'server is offline!!':
            print(response)
            break

        if response == 'Ready Retr':
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.settimeout(2)
            data_socket.connect((server, DATA_PORT))

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
                        data = data_socket.recv(BUFFER_SIZE).decode()
                        if not data:
                            break
                        f.write(data)

                data_socket.close()

                control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                control_socket.settimeout(2)
                control_socket.connect((server, CTRL_PORT))
                response = control_socket.recv(1024).decode()
                control_socket.close()

            except:
                response = '400 Connection loss'


        elif response == 'Ready Stor':
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.settimeout(2)
            data_socket.connect((server, DATA_PORT))

            file_name = request.split()[1]
            try:
                with open(file_name, 'r') as f:
                    data = f.read(BUFFER_SIZE)
                    while data:
                        data_socket.sendall(data.encode())
                        data = f.read(BUFFER_SIZE)

                data_socket.close()

                control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                control_socket.settimeout(2)
                control_socket.connect((server, CTRL_PORT))
                response = control_socket.recv(1024).decode()
                control_socket.close()

            except:
                response = '400 Connection loss'

        elif response == 'Not Ready':
                control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                control_socket.settimeout(2)
                control_socket.connect((server, CTRL_PORT))
                response = control_socket.recv(1024).decode()
                control_socket.close()

        elif response == '200 Goodnight!':
            print(response)
            break
        
        print(response)
    

if __name__ == '__main__':
    main()
        
