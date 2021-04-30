import services
from config import data as config_data
import threading
from service_states import UserState

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
