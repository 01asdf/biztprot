import shutil
import socket
import Crypto
import services
from config import data as config_data
import os
from os.path import exists as exists
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import Server_functions


def make_folder(folder_path):
    if not exists(folder_path):
        os.makedirs(folder_path)

def delete_folder(folder_path):
    if exists(folder_path):
        shutil.rmtree(folder_path)

def source_directory():
    return os.getcwd()

def list_directory(path):
    return os.listdir(path)

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


def to_directory(path):
    if has_acces_to_file(path):
        actuals.path = path




def order_parse_and_doit(order):
    #Hash levétel és ellenőrzés
    message=order.split(",")
    hash = message.pop()
    h_obj = Crypto.Hash.SHA3_256.new()
    h_obj.update(",".join(message))
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
            make_folder(actuals.path+"/"+order[1])
            return "Done"
        if message[0] == "RMD":
            delete_folder(actuals.path+"/"+order[1])
            return "Done"
        if message[0] == "GWD":
            return actuals.path
        if message[0] == "CWD":
            print()
            #TODO
        if message[0] == "LST":
            return "List,"+",".join(list_directory(actuals.path))
        if message[0] == "UPL":
            #TODO: lecserélni szabi függvényére
            services.listening(1)
            return "Done"
        if message[0] == "DNL":
            #TODO: lecserélni szabi függvényére
            services.senddata(1,1)
        if message[0] == "RMF":
            delete_folder(actuals.path+"/"+order[1])
        else:
            return "Unknown command"


def login():
    while True:
        #TODO: Szabi függcénye várakozik
        login_message=""

        message=login_message.split(",")
        hash = message.pop()
        h_obj = Crypto.Hash.SHA3_256.new()
        h_obj.update(",".join(message))
        if h_obj.hexdigest() != hash:
            print()
            #TODO: Szabi String üzenet: HASH ERROR

        #Timestamp ellenőrzés
        timestamp = int(message.pop())
        if timestamp + 10*1000 < services.current_time_milis():
            #TODO: Szabi
            return "Error: To old message"

        order_count = int(message.pop())
        if order_count != 0:
            #TODO szabi
            return "Error: Not the next order"
        actuals.last_order_count = 0

        AES_key = message.pop()
        if len(AES_key) != 32:
            print()
            #TODO: Szabi serror

        #Csak a jelszó maradt a messageben
        h_obj = Crypto.Hash.SHA3_256.new()
        h_obj.update(",".join(message))
        actuals.user = h_obj.hexdigest()
        to_directory(actuals.user)



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

        



        login()
        while True:
            if actuals.user == None:
                login()
            order = services.listening(config_data.server_port)
            #adat feldolgozása

            answre=order_parse_and_doit(order)

            #TODO: SZABI STRING KÜLDŐJE
            services.senddata(config_data.localhost,config_data.client_port)

if __name__ == "__main__":
    main()

