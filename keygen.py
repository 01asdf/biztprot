from Crypto.PublicKey import RSA

key = RSA.generate(2048)
f = open('privatekey.pem','wb')
f.write(key.export_key('PEM'))
f.close()

#f = open('mykey.pem','r')
#key = RSA.import_key(f.read())

f = open('publickey.pem','wb')
f.write(key.publickey().export_key())
f.close()