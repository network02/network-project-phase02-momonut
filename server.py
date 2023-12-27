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
    def __init__(self, username):
        self.set_username(username)

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_privilage(self, privilage):
        self.privilage = privilage

    def authenticate(self):
        for user in users:
            if self.username == user.username and self.password == user.password:
                self.set_privilage(user.privilage)
                online_users.append(self)
                return True

        return False

        
            
def handle_user(request):
    pass
def handle_pass(request):
    pass
def handle_list(request):
    pass
def handle_retr(request):
    pass
def handle_stor(request):
    pass
def handle_mkd(request):
    pass

def handle_rmd(request):  
    request_parts = request.strip().split()
    dir = request_parts[1]
    command = 'rmdir ' + dir
    s = subprocess.run(shlex.split(command))
    return s

def handle_pwd(request):
    command = 'pwd'
    s = subprocess.run(shlex.split(command))
    return s

def handle_cwd(request):
    request_parts = request.strip().split()
    dir = request_parts[1]
    command = 'cd ' + dir
    s = subprocess.run(shlex.split(command))
    return s

def handle_dele(request):
    request_parts = request.strip().split()
    name = request_parts[1]
    command = 'rm -f' + name
    s = subprocess.run(shlex.split(command))
    return s

def handle_cdup(request):
    command = 'cd ..'
    s = subprocess.run(shlex.split(command))
    return s

def handle_quit(request):
    s = "400"
    return s


def main():
    host = "localhost"
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode()

        if "USER" in request.to_upper():
            response = handle_user(request)
        elif "PASS" in request.to_upper():
            response = handle_pass(request)
        elif "LIST" in request.to_upper():
            response = handle_list(request)
        elif "RETR" in request.to_upper():
            response = handle_retr(request)
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