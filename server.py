import socket 
import threading
target='127.0.0.1'
port=7000
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((target,port))
server.listen()
clients=[]
nicknames=[]
def broadcast(message):
    for client in clients:
        client.send(message)
    
#handling client
def handle(client):
    while True:
        try:
            message=client.recv(1024)
            if not message:
                return
            else:
                index=clients.index(client)
                broadcast(message)
        except:
            index=clients.index(client)
            nickname=nicknames[index]
            clients.remove(client)
            nicknames.remove(nickname)
            client.close()
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            break
def recieve():
    while True:
        # read the accept connection from the client
        
        client,address=server.accept()
        print(f"Connected with {str(address)}")     
        client.send('NICK'.encode('ascii'))
        nickname=client.recv(1024).decode('ascii')
        nicknames.append(nickname)   
        clients.append(client)
        print(f'Nickname of the client is {nickname}')
        # broadcast the client
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))
        thread=threading.Thread(target=handle,args=(client,))
        thread.start()
        
recieve()