import socket
import routing

HOST = "192.168.5.129" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    #try:
    #client, clientInfo = s.accept()
    while 1:
        print("top")
        client, clientInfo = s.accept()
        print("server recv from: ", clientInfo)
        data = client.recv(1024)      # receive 1024 Bytes of message in binary format
        if data != b"":
            print(data)
            data = data.decode("utf-8")
            
            if "right" in data:
                routing.ct_right()
                #client.sendall(bytes("right")
                dst = routing.get_distance(0)
                print("right")
                client.sendall(bytes(str(dst),"utf-8"))
                routing.fc.stop()
                
            if "left" in data:
                routing.ct_left()
                #client.sendall(bytes("left")
                dst = routing.get_distance(0)
                print("left")
                client.sendall(bytes(str(dst),"utf-8"))
                routing.fc.stop()
                
            if "back" in data:
                routing.move_back()
                #client.sendall(bytes("back")
                dst = routing.get_distance(0)
                print("back")
                client.sendall(bytes(str(dst),"utf-8"))
               
            if "forward" in data:
                routing.forward()
                #client.sendall(bytes("back")
                dst = routing.get_distance(0)
                print("forward")
                client.sendall(bytes(str(dst),"utf-8"))
            if data == "stop":
                print("stopping")
                routing.fc.stop()
                dst = routing.get_distance(0)
                client.sendall(bytes(str(dst),"utf-8"))
                
            if "speed" in data:
                try:
                    if "set" in data:
                        ns =  data.strip("set speed ")
                        ns = int(ns)
                        print("change speed")
                        routing.speed = ns
                        #routing.forward()
                    #client.sendall(bytes("forward")
                    dst = routing.get_distance(0)
                    client.sendall(bytes,(str(dst)),"utf-8")
                except:
                    print("getting speed")
                    sp = routing.speed
                    client.sendall(bytes(str(sp),"utf-8"))
                    
            if "temp" in data:
                print("getting temperature")
                tp = routing.get_temp()
                client.sendall(bytes(str(tp),"utf-8"))
                
            if "cpu" in data:
                print("getting temperature")
                cpu = routing.get_cpu_percent()
                client.sendall(bytes(str(cpu),"utf-8"))
                    
                
                
    #except: 
        #print("Closing socket")
        #client.close()
        #s.close()    