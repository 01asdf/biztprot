from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


msgfile = open('rsaencryptedmsg','rb')
encryptedMessage = msgfile.read()

privkey_file = open('privatekey.pem','r')
RSAkey = RSA.import_key(privkey_file.read())

cipher_rsa = PKCS1_OAEP.new(RSAkey)
decryptedMessage = cipher_rsa.decrypt(encryptedMessage)

print(decryptedMessage.decode())
splitted =  decryptedMessage.decode().split(",")
sorszam = splitted[0]
timestamp = splitted[1]
aeskey = splitted[2]
password = splitted[3]
sha3hash = splitted[4]

print(sorszam)
print(timestamp)
print(aeskey)
print(password)
print(sha3hash)

