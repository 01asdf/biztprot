import services
from config import data as config_data

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
