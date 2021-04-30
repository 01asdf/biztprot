import base64
import shutil
import socket
import Crypto
import services
from config import data as config_data
import os
from os.path import exists as exists
from Crypto.Hash import SHA3_256

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Server_functions import onReceive, sendMessage, sendFile_AES, waitForMessage, waitForFile


def make_folder(folder_path):
    if not exists(folder_path):
        os.makedirs(folder_path)

def delete_folder(folder_path):
    if exists(folder_path) and has_acces_to_file(folder_path):
        shutil.rmtree(folder_path)

def source_directory():
    return os.getcwd()

def list_directory(path):
    if exists(path):
        return os.listdir(path)
    else:
        return []

def rsa_decode(encryptedRSAmessage): # bináris üzenetet vár, visszatér a dekódolt stringgel
    privkey_file = open('privatekey.pem','r')
    RSAkey = RSA.import_key(privkey_file.read())

    cipher_rsa = PKCS1_OAEP.new(RSAkey)
    decryptedMessage = cipher_rsa.decrypt(encryptedRSAmessage)    
    return decryptedMessage.decode()

def has_acces_to_file(path):
    if source_directory()+"/"+actuals.user in path:
        return True
    return False

class actuals:
    user = None
    path = source_directory()
    roote_path = source_directory()
    last_order_count = None
    AES_key = None
    socket = None
    waited_file=None

def path_remove(path):
    char ='1'
    while char !='/':
        char = path[len(path)-1]
        path=path[:len(path)-1]
    return path

def to_directory(path):
    if path == ".." and actuals.path!= actuals.roote_path+"/"+actuals.user:
        actuals.path = path_remove(actuals.path)
        return
    elif has_acces_to_file(actuals.path+"/"+path) and path != "..":
        actuals.path = actuals.path+"/"+path

def login_directory():
    make_folder(actuals.user)
    actuals.path = actuals.path+"/"+actuals.user

def deletefile(path):
    if os.path.exists(path):
        os.remove(path)

def order_parse_and_doit(order):
    message=order.split(",")

    #Hash levétel és ellenőrzés
    hash = message.pop()
    h_obj = SHA3_256.new()
    h_obj.update(",".join(message).encode())
    if h_obj.hexdigest() != hash:
        return "Error: Hash"

    #Timestamp ellenőrzés
    timestamp = int(message.pop())
    if timestamp + 10*1000 < services.current_time_milis():
        return "Error: To old message"

    order_count = int(message.pop())
    if order_count != actuals.last_order_count+1:
        return "Error: Not the next order"
    else:
        actuals.last_order_count = order_count

        if message[0] == "MKD":
            make_folder(actuals.path+"/"+message[1])
            return "Done"
        if message[0] == "RMD":
            delete_folder(actuals.path+"/"+message[1])
            return "Done"
        if message[0] == "GWD":
            return actuals.path.replace(actuals.roote_path,"")
        if message[0] == "CWD":
            to_directory(message[1])
            return "Done"
        if message[0] == "LST":
            list = list_directory(actuals.path)
            if len(list) !=0:
                return ",".join(list)
            else:
                return "Empty"
        if message[0] == "UPL":
            actuals.waited_file=message[1]
            return "WAIT FILE"
        if message[0] == "DNL":
            actuals.waited_file=message[1]
            return "SENDING FILE"
        if message[0] == "RMF":
            deletefile(actuals.path+"/"+message[1])
            return "Done"
        else:
            return "Unknown command"

def message_to_client(string):
    sendMessage(actuals.socket,string,"AES",actuals.AES_key)

def login(login_message):
    message=login_message.split(",")
    hash = message.pop()
    h_obj = SHA3_256.new()
    h_obj.update(",".join(message).encode())
    if h_obj.hexdigest() != hash:
        return "Error: Hash"
    #Timestamp ellenőrzés
    timestamp = int(message.pop())
    if timestamp + 10*1000 < services.current_time_milis():
        return "Error: To old message"

    order_count = int(message.pop())
    if order_count != 0:
        return "Error: Not the next order"
    actuals.last_order_count = 0
    aes_string=message.pop()
    AES_key=base64.b64decode(aes_string.encode())
    if len(aes_string) != 44:
        return "Error:  AES key not 256 bit long"

    actuals.AES_key = AES_key

    #Csak a jelszó maradt a messageben
    h_obj = SHA3_256.new()
    h_obj.update(",".join(message).encode())
    actuals.user = h_obj.hexdigest()
    login_directory()

    return "Logged in"



def main():
    while True:
        # device's IP address
        SERVER_HOST = "0.0.0.0"
        SERVER_PORT = config_data.server_port
        # receive 4096 bytes each time
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"
        # create the server socket
        # TCP socket
        s = socket.socket()
        # bind the socket to our local address
        s.bind((SERVER_HOST, SERVER_PORT))
        # enabling our server to accept connections
        # 5 here is the number of unaccepted connections that
        # the system will allow before refusing new connections
        s.listen(5)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        # accept connection if there is any


        #A client_socket a csatlakozott kliensel nyitott kapcsolat
        client_socket, address = s.accept()
        actuals.socket = client_socket

        #Amíg valaki be nem jelentkezik
        while actuals.user == None:
            login_binari = waitForMessage(actuals.socket)
            login_string = rsa_decode(login_binari)

            l=login(login_string)
            message_to_client(l)
            print("LOGED IN")

        #Amíg a user ki nem lép
        while True:
            order_binary = waitForMessage(actuals.socket)
            if order_binary != b'':
                order_string = onReceive(order_binary, "AES", actuals.AES_key)
                #adat feldolgozása

                answer=order_parse_and_doit(order_string)


                if answer == "Exit":
                    actuals.user=None
                    actuals.path = source_directory()
                    actuals.AES_key = None
                    actuals.socket.close()
                    actuals.socket=None
                    break
                message_to_client(answer)
                if answer == "SENDING FILE":
                    sendFile_AES(actuals.socket, actuals.waited_file, actuals.AES_key)
                    actuals.waited_file = None
                if answer == "WAIT FILE":
                    waitForFile(actuals.socket, actuals.waited_file, actuals.path, actuals.AES_key)
                    actuals.waited_file = None

if __name__ == "__main__":
    main()

