import socket
import tqdm
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


#<crypto>

data = bin(0)
with open('data.csv', mode='rb') as file: # b is important -> binary
    data = file.read()
key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)
file_out = open("enc.bin", "wb")
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
file_out.close()

#</crypto>


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
# the ip address or hostname of the server, the receiver
host = "192.168.0.144"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "enc.bin"
# get the file size
filesize = os.path.getsize(filename)
# create the client socket
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()
