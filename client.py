import services
from config import data as config_data
import threading
from service_states import UserState
from datetime import datetime
from Crypto.Hash import SHA3_256
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


#Ide jön a kliensoldali parancsok lekezelése
#Visszaadja a szervernek küldendő adatot
def orders(user_state):
    data=""
    input_string=""
    #Ha nincs a user bejelentkezve, akkor elkérjük a jelszót
    if user_state != UserState.LOGED_IN:
        print("You have to log in! Enter your password!")
        input_string=input()
        data=input_string
    else:
        print("Enter your command!")
        input_string = input()

    return data


def main():
    data=""
    user_state= UserState.NOT_LOGED_IN

    # TODO induláskor generáljuk egy AES keyt
    AESkey = "Én vagyok a 256 bit hosszú AES key ..... ......"

    print("Enter your password!")
    password = input()
    
    print("Connecting to server...")
    # sorszam, timestamp, aes, password
    # ezeket hasheljük, hashet vesszővel a végére
    initMessageWithoutHash = ",".join([str(0), str(services.current_time_milis()), AESkey, password])

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

    print(encryptedInitMessage)

    # TESZT: üzenetetet ezekkel fájlba írjuk, rsareadtest.py fájlt futtatva beolvashatjuk
    fff = open('rsaencryptedmsg','wb')
    fff.write(encryptedInitMessage)
    fff.close()
    ## TESZT VÉGE



    # TODO elküldeni ezt a szerver felé, és várni a nyugtát

    


    print("Connected to server!")

    while order != "Exit":
        order = orders(user_state)

        #Válaszüzenetre váró szál indítása
        answer_cathcing_thread = threading.Thread(target=services.listening, args=(config_data.client_port,))
        answer_cathcing_thread.start()


        #Adatok elküldése a szervernek
        services.senddata(config_data.localhost,config_data.server_port)

        #Megvárjuk a választ
        answer_cathcing_thread.join()


if __name__ == "__main__":
    main()
