import bluetooth
import routing

hostMACAddress = "DC:A6:32:80:7D:87" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 0
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("listening on port ", port)
try:
    client, clientInfo = s.accept()
    while 1:   
        print("server recv from: ", clientInfo)
        data = client.recv(size)
        if data:
            print(data)
            #client.send(data) # Echo back to client
        
            data = data.decode("utf-8")
            
            if "dist" in data:
                dt = routing.get_distance(0)
                client.sendall(bytes(str(dt),"utf-8"))
except: 
    print("Closing socket")
    client.close()
    s.close()

