import socket
import routing

HOST = "192.168.3.49" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)
                
                if data == "right"| data == "68":
                    routing.ct_right()
                    #client.sendall("right")
                    dst = routing.get_distance(0)
                    client.sendall(str(dst))
                if data == "left"| data =="65":
                    routing.ct_left()
                    #client.sendall("left")
                    dst = routing.get_distance(0)
                    client.sendall(str(dst))
                    
                if data == "back"| data=="83":
                    routing.move_back()
                    #client.sendall("back")
                    dst = routing.get_distance(0)
                    client.sendall("dist " + str(dst))
                if data == "forward"| data=="87":
                    routing.move_back()
                    #client.sendall("back")
                    dst = routing.get_distance(0)
                    client.sendall(str(dst))
                if "speed" in data:
                    try:
                        ns =  data.strip("speed ")
                        ns = int(ns)
                        routing.speed = ns
                        routing.forward()
                        #client.sendall("forward")
                        dst = routing.get_distance(0)
                        client.sendall(str(dst))
                    except:
                        client.sendall("Sorry no interger for speed found")
                    
                
                
    except: 
        print("Closing socket")
        client.close()
        s.close()    