from Crypto.Cipher import AES
def sendMessage(socket,string,enc_type,key=bytes(),BUFFER_SIZE=int(4096)):
    bin_rep = string.encode()
    if(enc_type=="AES"):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(bin_rep)
        socket.send(cipher.nonce,tag,ciphertext);
    if(enc_type=="RSA"):
        #RSA encrypt a privát kulccsal
        pass
        socket.send(ciphertext);
    if(enc_type=="RAW"):
        socket.send(bin_rep) #Kiküldés nyers formában

def sendFile_AES(socket,filename,key=bytes(),BUFFER_SIZE=int(4096)): #előtte üzenetet kell küldeni(?)
    # filesize = os.path.getsize(filename)
    with open(filename, mode='rb') as file: # b is important -> binary
        data = file.read()

    encfile = "enc.bin"
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    file_out = open(encfile, "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()
    with open(encfile, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            socket.sendall(bytes_read)
    print(filename+" elkuldve!")

def onReceive(bindata,enc_type,key=bytes()):
    if(enc_type=="AES"):
        cipher = AES.new(key, AES.MODE_EAX)
        raw = cipher.decrypt(bindata)
        return raw.decode()
    if(enc_type=="RSA"):
        pass #RSA decrypt a privát kulccsal
        #return decrypted
    if(enc_type=="RAW"):
        return bindata.decode()

def waitForFile(client_socket,filename,directory,key=bytes(),BUFFER_SIZE=int(4096)):
    with open('todec.bin', "wb") as f: #directory-t is bele kell tenni
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
    file_in = open("todec.bin", "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(directory+"/"+filename, "wb") as f2:
       f2.write(data)
    print("Fajl erkezett "+filename+" neven!")

def waitForMessage(clientsocket, BUFFER_SIZE=int(4096)):
    rec = clientsocket.recv(BUFFER_SIZE)
    return rec
