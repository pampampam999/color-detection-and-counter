import socket  
import sys



TOSENDSERVER = socket.socket() 
host = socket.gethostname()
port = 8800

TOSENDSERVER.connect((host, port))

selectedFile = input("Pilih file (contoh : TikTok.mp4) : ")
try:
	tosend_file = open(selectedFile,'rb')
	print ("File opened")
except Exception as fileerror:
	print ("Cannot open this file check this error: %s " % str(fileerror))
Filetosend = tosend_file.read(4069)
while (Filetosend):
    print ("Sending your file...")
    TOSENDSERVER.send(Filetosend)
    Filetosend = tosend_file.read(4096)
tosend_file.close()
print ("File sended sucessfully\n clossing...")
TOSENDSERVER.close()
sys.exit('Closed by system')










import sys
import socket



RECVSERVER = socket.socket()         
host = socket.gethostname() 
port = 8800
RECVSERVER.bind((host, port))


RECVSERVER.listen(5)          
while True:
    c, addr = RECVSERVER.accept() 
    print ("File will recv from: ", addr)
    print ("Start recv...")
    FILETORECV = c.recv(4096)
    hasil = input("Masukkan Nama File Hasil Konverter (contoh : Hasil.mp4) : ")
    recv_file = open(hasil,'wb')
    while (FILETORECV):
        print ("Receiving...")
        recv_file.write(FILETORECV)
        FILETORECV = c.recv(4096)
    recv_file.close()
    print ("File recv or converted sucessfully.")
    c.send('Message from client: File received sucessfully. tnx'.encode())
c.close()
sys.exit('closed by system')