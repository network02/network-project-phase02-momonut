import socket
import subprocess
import shlex
#commands

ORDINARY = 3
PRIVILAGED = 2
ADMIN = 1

users = []
online_users = []
class User:
    def __init__(self):
        pass

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_privilage(self, privilage):
        self.privilage = privilage

    def add_user(self, username, password, privilage):
        self.set_username(username)
        self.set_password(password)
        self.set_privilage(privilage)
        users.append(self)

    def authenticate(self):
        for user in users:
            if self.username == user.username and self.password == user.password:
                self.set_privilage(user.privilage)
                online_users.append(self)
                return True

        return False

    def quit(self):
        online_users.remove(self)
        

def add_fake_users():
    user = User()
    user.add_user('mohammad', 1234, ADMIN)
    user = User()
    user.add_user('pouya', 123456, ORDINARY) 

def handle_user(request, user):
    request_parts = request.strip().split()
    username = request_parts[1]
    user.set_username(username)
    response = 'Username Set'
    return response

def handle_pass(request, user):
    request_parts = request.strip().split()
    password = request_parts[1]
    user.set_password(password)
    login = user.authenticate()
    if login:
        response = 'Login Successfull'
    else:
        response = 'Login Failed'
    return response

def handle_list(request):
    request_parts = request.strip().split()
    if len(request_parts) > 1: 
        path = request_parts[1]
    else:
        path = ''
    command = f'ls {path} -l'
    response = subprocess.run(shelx.split(command))
    return response

def handle_retr(request, client_host):
    request_parts = request.strip().split()
    path = subprocess.run(shelx.split('pwd'))
    file_name = path + equest_parts[1] 
    port = 20 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((client_host, port))

    #TODO try exception
    with open(file_name, 'rb') as f:
        data = f.read(1024)
        while data:
            s.send(data)
            data = f.read(1024)

    s.close()
    rosponse = 'File Sent'
    return response

def handle_stor(request, client):
    pass

def handle_mkd(request):
    request_parts = request.strip().split()
    path = request_parts[1]
    command = 'mkdir ' + path 
    response = subprocess.run(shlex.split(command))
    return response 

def handle_rmd(request):  
    request_parts = request.strip().split()
    dir = request_parts[1]
    command = 'rmdir ' + dir
    response = subprocess.run(shlex.split(command))
    return response 

def handle_pwd(request):
    command = 'pwd'
    response = subprocess.run(shlex.split(command))
    return response 

def handle_cwd(request):
    request_parts = request.strip().split()
    dir = request_parts[1]
    command = 'cd ' + dir
    response = subprocess.run(shlex.split(command))
    return response 

def handle_dele(request):
    request_parts = request.strip().split()
    name = request_parts[1]
    command = 'rm -f' + name
    response = subprocess.run(shlex.split(command))
    return response 

def handle_cdup(request):
    command = 'cd ..'
    response = subprocess.run(shlex.split(command))
    return response 

def handle_quit(request, user):
    user.quit()
    response = "400"
    return response 


def main():
    host = "localhost"
    port = 21 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on http://{host}:{port}")

    add_fake_users()
    user = User()
    while True:
        client_socket, client_address = server_socket.accept()
        client_host = socket.gethostbyaddr(client_address[0])[0]
        request = client_socket.recv(1024).decode()

        if "USER" in request.to_upper():
            response = handle_user(request, user)
        elif "PASS" in request.to_upper():
            response = handle_pass(request, user)
        elif "LIST" in request.to_upper():
            response = handle_list(request, client_host)
        elif "RETR" in request.to_upper():
            response = handle_retr(request, client_host)
        elif "STOR" in request.to_upper():
            response = handle_stor(request)
        elif "MKD" in request.to_upper():
            response = handle_mkd(request)
        elif "RMD" in request.to_upper():
            response = handle_rmd(request)
        elif "PWD" in request.to_upper():
            response = handle_pwd(request)
        elif "CWD" in request.to_upper():
            response = handle_cwd(request)
        elif "DELE" in request.to_upper():
            response = handle_dele(request)
        elif "CDUP" in request.to_upper():
            response = handle_cdup(request)
        elif "QUIT" in request.to_upper():
            response = handle_quit(request)
        else:
            response = "400 Bad Request"

        client_socket.sendall(response.encode())
        client_socket.close()


if __name__ == "__main__":
    main()
        
        
#USER string
#PASS string
#LIST null | string
#RETR string
#STOR string
#MKD string
#RMD 
#PWD
#CWD string
#DELE string
#CDUP 
#QUIT
