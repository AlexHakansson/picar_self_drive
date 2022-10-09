import socket
import routing

HOST = "192.168.5.129" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    #try:
    client, clientInfo = s.accept()
    while 1:
        #client, clientInfo = s.accept()
        print("server recv from: ", clientInfo)
        data = client.recv(1024)      # receive 1024 Bytes of message in binary format
        if data != b"":
            print(data)
            data = data.decode("utf-8")
            
            if data == "right"or data == "68":
                routing.ct_right()
                #client.sendall(bytes("right")
                dst = routing.get_distance(0)
                print("right")
                client.sendall(bytes(str(dst),"utf-8"))
            if data == "left"or data =="65":
                routing.ct_left()
                #client.sendall(bytes("left")
                dst = routing.get_distance(0)
                client.sendall(bytes(str(dst),"utf-8"))
                
            if data == "back"or data=="83":
                routing.move_back()
                #client.sendall(bytes("back")
                dst = routing.get_distance(0)
                client.sendall(bytes(str(dst),"utf-8"))
            if data == "forward"or data=="87":
                routing.move_back()
                #client.sendall(bytes("back")
                dst = routing.get_distance(0)
                client.sendall(bytes(str(dst),"utf-8"))
            if data == "Stop":
                routing.fc.stop()
                client.sendall(bytes(str(routing.speed),"utf-8"))
                
            if "speed" in data:
                try:
                    ns =  data.strip("speed ")
                    ns = int(ns)
                    routing.speed = ns
                    routing.forward()
                    #client.sendall(bytes("forward")
                    dst = routing.get_distance(0)
                    client.sendall(str(dst))
                except:
                    client.sendall(bytes(str(routing.speed),"utf-8"))
                    
                
                
    #except: 
        #print("Closing socket")
        #client.close()
        #s.close()    