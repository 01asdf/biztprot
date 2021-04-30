import shutil
import services
from config import data as config_data
import os
from os.path import exists as exists
import pathlib


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
