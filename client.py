import services
from config import data as config_data
import threading
from service_states import UserState
import hashlib
import Crypto

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
        h_obj = Crypto.Hash.SHA3_256.new()
        h_obj.update(command_string)
        return  ",".join(command_string,h_obj.hexdigest())
    else:
        print("Invalid command")
        return None


def login():
    print("You have to log in! Enter your password!")
    password=input()
    actuals.AES_key = Crypto.Random.get_random_bytes(32)
    actuals.order_count = 0
    message = ",".join(password,actuals.AES_key,actuals.order_count, services.current_time_milis())
    h_obj = Crypto.Hash.SHA3_256.new()
    h_obj.update(message)
    message_with_hash = ",".join(message,h_obj.hexdigest())
    #TODO: MÁTÉ RSA ELKÜLDÉSE




class actuals:
    AES_key=None
    order_count = None

def main():
    data=""
    user_state= UserState.NOT_LOGED_IN
    login()

    while order != "Exit":
        actuals.command_count+=1
        order = orders()
        if order is not None:
            #Válaszüzenetre váró szál indítása
            answer_cathcing_thread = threading.Thread(target=services.listening, args=(config_data.client_port,))
            answer_cathcing_thread.start()


            #Adatok elküldése a szervernek
            services.senddata(config_data.localhost,config_data.server_port)


            #Megvárjuk a választ
            answer_cathcing_thread.join()


if __name__ == "__main__":
    main()
