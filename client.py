import os
import socket
import services
from config import data as config_data
import threading
from service_states import UserState
from datetime import datetime
import Crypto
from Crypto.Hash import SHA3_256
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Server_functions import onReceive, sendMessage, sendFile_AES, waitForMessage, waitForFile


#Ide jön a kliensoldali parancsok lekezelése
#Visszaadja a szervernek küldendő adatot
def orders():
    data=""
    input_string=""
    #Ha nincs a user bejelentkezve, akkor elkérjük a jelszót
    print("Enter your command!")
    input_string = input()
    command = input_string.split(' ')

    if command[0] == ["MKD", "RMD","GWD","CWD","LST","UPL","DNL","RMF"]:
        command_string = ",".join([command[0],command[1],str(actuals.order_count),str(services.current_time_milis())])
        h_obj = SHA3_256.new()
        h_obj.update(command_string)
        return  ",".join(command_string,h_obj.hexdigest())
    else:
        print("Invalid command")
        return None

class actuals:
    AES_key=None
    order_count = None
    socket = None

def main():

    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 # send 4096 bytes each time step
    # the ip address or hostname of the server, the receiver
    # the port, let's use 5001
    # the name of file we want to send, make sure it exists
    filename = "senddata.encripted.bin"
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket()
    s.connect((config_data.localhost, config_data.server_port))
    actuals.socket = s


    data=""
    user_state= UserState.NOT_LOGED_IN
    actuals.AES_key = Crypto.Random.get_random_bytes(32)

    print("Enter your password!")
    password = input()
    actuals.order_count = 0
    print("Connecting to server...")
    # sorszam, timestamp, aes, password
    # ezeket hasheljük, hashet vesszővel a végére
    initMessageWithoutHash = ",".join([password, actuals.AES_key, str(actuals.order_count), str(services.current_time_milis())])

    h_obj = SHA3_256.new()
    h_obj.update(initMessageWithoutHash.encode())
    initMessageHash = h_obj.hexdigest()
    initMessage = ",".join([initMessageWithoutHash, initMessageHash])

    pubkey_file = open('publickey.pem','r')
    RSApublicKey = RSA.import_key(pubkey_file.read())
    pubkey_file.close()

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(RSApublicKey)
    encryptedInitMessage = cipher_rsa.encrypt(initMessage.encode())

    actuals.socket.send(encryptedInitMessage)
    answer = waitForMessage(actuals.socket)

    while order != "Exit":
        actuals.command_count+=1
        order = orders()
        if order is not None:
            sendMessage(actuals.socket, order, "AES", actuals.AES_key)


if __name__ == "__main__":
    main()
