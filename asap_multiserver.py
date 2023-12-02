import socket
import threading
import time
import pickle
from collections import OrderedDict
import matplotlib as plt


lock = threading.Lock()

# Define the server address and port
server_ip = '10.194.'
server_port = 2838

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the server address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections (up to 5 clients)
server_socket.listen(3)
print(f"Server listening on {server_ip}:{server_port}")

buffer = set()
dic = OrderedDict()

vayu_ip = "10.17.7.218"
vayu_port = 9801

start_time = time.time()


def receive_from_vayu():
    vayu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vayu_socket.connect((vayu_ip, vayu_port))

    while True:
        # Send data to the server
        message = "SENDLINE\n"
        vayu_socket.send(message.encode('utf-8'))
        # Receive data from the server
        count = 0
        deCode = ""
        while count != 2:
            row_dat = vayu_socket.recv(1024)
            deCode += row_dat.decode('utf-8')
            count = deCode.count('\n')
        print(deCode)
        # data = vayu_socket.recv(99999).decode('utf-8')

        lines = deCode.split('\n')
        l = lines[0].split()[-1]

        if l != '-1' and l not in buffer:
            with lock:
                dic[lines[0]] = lines[1]
                buffer.add(l)
        with lock:
            if len(buffer) >= 10:
                c = 0
                msg = 'SUBMIT\n'
                vayu_socket.send(msg.encode('utf-8'))
                idk = '2023JCS2542@Shan\n'
                vayu_socket.send(idk.encode('utf-8'))
                total_data = '1000\n'
                vayu_socket.send(total_data.encode('utf-8'))
                size = len(dic)
                if size == 1000:
                    dic['1000'] = "this is dammy line"
                for key in dic.keys():
                    k = key + '\n'
                    v = dic[key] + '\n'
                    c += 1
                    if c > 1000:
                        resp = vayu_socket.recv(1024).decode('utf-8')
                        print(resp)
                        break
                    vayu_socket.send(k.encode('utf-8'))
                    vayu_socket.send(v.encode('utf-8'))

                vayu_socket.close()
                break


# Function to handle client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        with lock:
            count = 0
            data = ""
            while count != 2:
                row_data = conn.recv(1024)
                data += row_data.decode('utf-8')
                count = data.count('\n')
            salines = data.split('\n')
            if salines[0] not in buffer:
                dic[salines[0]] = salines[1]
            buffer.add(salines[0])
        length = len(buffer)
        print(dic, len(dic))
        print(length)
        print(buffer)
        with lock:
            if length >= 10:
                response_message = b'0'
                conn.send(response_message)
                pickle_data = pickle.dumps(dic)
                conn.send(pickle_data)
                print(f"[DISCONNECTED] {addr} disconnected")
                conn.close()
                break

            else:
                response_message = b'1'  # encoding 1 as a byte
                conn.send(response_message)


server = threading.Thread(target=receive_from_vayu, args=())
server.start()

# Accept a client connection
conn1, addr1 = server_socket.accept()
print(f"Accepted connection from {addr1}")

# Start a new thread to handle the client
client_handler1 = threading.Thread(target=handle_client, args=(conn1, addr1))
client_handler1.start()

# Accept a client connection
conn2, addr2 = server_socket.accept()
print(f"Accepted connection from {addr2}")

# Start a new thread to handle the client
client_handler2 = threading.Thread(target=handle_client, args=(conn2, addr2))
client_handler2.start()

conn3, addr3 = server_socket.accept()
print(f"Accepted connection from {addr3}")

# Start a new thread to handle the client
client_handler3 = threading.Thread(target=handle_client, args=(conn3, addr3))
client_handler3.start()

client_handler1.join()
client_handler2.join()
client_handler3.join()
server.join()

end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time)
x = [0,1,3]
y = [4,2,9]
plt.plot(x, y)
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.title('Title of the Plot')
plt.legend(['Line 1'])
plt.grid(True)

plt.show()  # Display the plot
