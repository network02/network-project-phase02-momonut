import socket
import subprocess
import shlex
import os
from time import sleep
#commands

ORDINARY = 2
ADMIN = 1
BAD_REQUEST = '400 Bad Request'
DEFAULT_DIR = f'/home/{os.getlogin()}/ftp'
LOG = f'/home/{os.getlogin()}/ftp/report.log'

host = "localhost"
ctrl_port = 8021 
data_port = 8020 

users = []
online_users = []
class User:
    def __init__(self):
        self.authorized = False
        self.current_dir = DEFAULT_DIR 

    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_privilage(self, privilage):
        self.privilage = privilage

    def set_current_dir(self, directory):
        self.current_dir = directory

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_current_dir(self):
        return self.current_dir

    def get_privilage(self):
        return self.privilage

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
                self.authorized = True
                break

    def quit(self):
        online_users.remove(self)
    
    def __str__(self):
        return f'username: {self.username}\npassword: {self.password}\nprivilage: {self.privilage}\nautorization: {self.authorized}\ndir: {self.current_dir}'


def add_fake_users():
    user = User()
    user.add_user('mohammad', '1234', ADMIN)
    user = User()
    user.add_user('p', '1', ADMIN) 

def handle_user(request, user):
    request_parts = request.strip().split()
    try:
        username = request_parts[1]
    except:
        return BAD_REQUEST

    user.set_username(username)
    response = 'Username Set'
    return response

def handle_pass(request, user):
    request_parts = request.strip().split()
    try:
        password = request_parts[1]
    except:
        return BAD_REQUEST

    user.set_password(password)
    user.authenticate()
    if user.authorized:
        response = 'Login Successfull'
    else:
        response = 'Login Failed'
    return response

def handle_list(request, directory):
    request_parts = request.strip().split()
    if len(request_parts) > 1: 
        path = request_parts[1]
    else:
        path = ''
    command = f'ls {path} -ltrh'
    response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, cwd=directory).stdout.decode()
    if 'total' not in response:
        command = f'cat {path}'
        response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, cwd=directory).stdout.decode()
    return response

def handle_retr(request, client_host, directory):
    request_parts = request.strip().split()
    file_name = directory + '/' + request_parts[1] 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((client_host, data_port))

    #TODO try exception
    with open(file_name, 'rb') as f:
        while data:
            data = f.read(1024)
            s.send(data.encode())

    s.close()
    response = 'File Sent'
    return response

def handle_stor(request, client, directory):
    pass

def handle_mkd(request, directory):
    request_parts = request.strip().split()
    try:
        path = request_parts[1]
    except:
        return BAD_REQUEST

    command = 'mkdir ' + path 
    response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, cwd=directory).stdout.decode()
    response = f'Directory cheeze "{path}" created' if not response else response
    return response 

def handle_rmd(request, directory):  
    request_parts = request.strip().split()
    try:
        path = request_parts[1]
    except:
        return BAD_REQUEST

    command = 'rmdir ' + path
    response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, cwd=directory).stdout.decode()
    response = f'Directory cheeze "{path}" removed' if not response else response
    return response 

def handle_pwd(directory):
    command = 'pwd'
    response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, cwd=directory).stdout.decode()
    return response 

def handle_cwd(request, user, directory):
    request_parts = request.strip().split()
    try:
        path = request_parts[1]
    except:
        return BAD_REQUEST
    
    if path[0] == '/':
        path = DEFAULT_DIR + path 
    else:
        path = directory + '/' + path
    try:
        os.chdir(path)
        path = os.getcwd()
        if 'ftp' not in path:
            response = BAD_REQUEST
        else:
            user.set_current_dir(path)
            response = f'You are in {path}' 
    except:
        response = 'Directory Not Found'

    return response 

def handle_dele(request, directory):
    request_parts = request.strip().split()
    try:
        name = request_parts[1]
    except:
        return BAD_REQUEST

    command = 'rm -rf ' + name
    response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, cwd=directory).stdout.decode()
    return response 

def handle_cdup(user, directory):
    return handle_cwd('cd ..', user, directory)

def handle_quit(user):
    user.quit()
    response = "Goodnight!"
    return response 

def handle_report(privilage):
    if privilage == ADMIN:
        command = 'cat ' + LOG 
        response = subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode()
    else:
        response = "Access Denied"

    return response


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, ctrl_port))
    server_socket.listen(1)
    print(f"Server is listening on http://{host}:{ctrl_port}")

    add_fake_users()
    user = User()
    while True:
        client_socket, client_address = server_socket.accept()
        client_host = socket.gethostbyaddr(client_address[0])[0]
        request = client_socket.recv(1024).decode()

        if 'USER' in request.upper():
            with open(LOG, 'a') as f:
                f.write(f'User: Unknown\nRequest: {request}\n')
            response = handle_user(request, user)
        elif 'PASS' in request.upper():
            with open(LOG, 'a') as f:
                f.write(f'User: Unknown\nRequest: {request}\n')
            response = handle_pass(request, user)

        elif user.authorized:
            with open(LOG, 'a') as f:
                f.write(f'User: {user.get_username()}\nRequest: {request}\n')

            current_dir = user.get_current_dir()
            if any(x in request.upper() for x in ['LIST', 'LS']):
                response = handle_list(request, current_dir)
            elif 'RETR' in request.upper():
                response = handle_retr(request, client_host, current_dir)
            elif 'STOR' in request.upper():
                response = handle_stor(request, client_host)
            elif any(x in request.upper() for x in ['MKD', 'MKDIR']):
                response = handle_mkd(request, current_dir)
            elif any(x in request.upper() for x in ['RMD', 'RMDIR']):
                response = handle_rmd(request, current_dir)
            elif 'PWD' in request.upper():
                response = handle_pwd(current_dir)
            elif 'CDUP' in request.upper():
                response = handle_cdup(user, current_dir)
            elif any(x in request.upper() for x in ['CWD', 'CD']):
                response = handle_cwd(request, user, current_dir)
            elif any(x in request.upper()for x in ['DELE', 'RM']):
                response = handle_dele(request, current_dir)
            elif any(x in request.upper() for x in ['QUIT']):
                response = handle_quit(user)
            elif 'REPORT' in request.upper(): 
                response = handle_report(user.get_privilage())
            else:
                response = BAD_REQUEST
        else:
            response = "Login First!"

        with open(LOG, 'a') as f:
            f.write(f'Response: {response}\n')
            f.write('--------------------------------\n')

        client_socket.sendall(response.encode())
        client_socket.close()


if __name__ == "__main__":
    main()
        
        
#USER string
#PASS string
#MKD string
#RMD 
#PWD
#CWD string
#DELE string
#CDUP 
#LIST null | string
#QUIT

#RETR string
#STOR string
# priority
