import shutil
import services
from config import data as config_data
import os
from os.path import exists as exists
import pathlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


def make_folser(folder_path):
    if not exists(folder_path):
        os.makedirs(folder_path)

def delete_folder(folder_path):
    if exists(folder_path):
        shutil.rmtree(folder_path)

def source_directory():
    return pathlib.Path.absolute()

def list_directory(path):
    return os.listdir(path)

def rsa_decode(encryptedRSAmessage): # bináris üzenetet vár
    privkey_file = open('privatekey.pem','r')
    RSAkey = RSA.import_key(privkey_file.read())

    cipher_rsa = PKCS1_OAEP.new(RSAkey)
    decryptedMessage = cipher_rsa.decrypt(encryptedRSAmessage)

    return decryptedMessage.decode()


def main():
    while True:
        data = services.listening(config_data.server_port)
        #adat feldolgozása

        print("Datasend")
        print(services.current_time_milis())
        answer=""
        services.senddata(config_data.localhost,config_data.client_port)

if __name__ == "__main__":
    main()

