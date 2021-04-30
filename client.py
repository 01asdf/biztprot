import services
from config import data as config_data
import threading

#Ide jön a kliensoldali parancsok lekezelése
#Visszaadja a szervernek küldendő adatot
def orders():
    print()

def main():
    data_to_send = orders()

    #Válaszüzenetre váró szál indítása
    answer_cathcing_thread = threading.Thread(target=services.listening, args=(config_data.client_port,))
    answer_cathcing_thread.start()


    #Adatok elküldése a szervernek
    services.senddata(config_data.localhost,config_data.server_port)

    #Megvárjuk a választ
    answer_cathcing_thread.join()


if __name__ == "__main__":
    main()
