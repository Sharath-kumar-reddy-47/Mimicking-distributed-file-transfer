import socket
import time
import pickle
from collections import OrderedDict

# vayu_server
server1_ip = "10.17.6.5"
server1_port = 9801

# master server
server2_ip = '10.194.39.228'
server2_port = 2842
server1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buffer = set()
conn = 0
while conn<10:
        try:
            server1_socket.connect((server1_ip, server1_port))
            break
        except ConnectionRefusedError:
            print("Server is not available. Retrying...")
            conn+=1
while conn<10:
        try:
            server2_socket.connect((server2_ip, server2_port))
            break
        except ConnectionRefusedError:
            print("Server is not available. Retrying...")
            conn+=1
start_time = time.time()
dic = OrderedDict()
while True:
    # Send data to the server
    message = "SENDLINE\n"
    server1_socket.send(message.encode('utf-8'))

    # Receive data from the server
    count = 0
    code = ""
    while count != 2:
        row_data = server1_socket.recv(1024)
        code += row_data.decode('utf-8')
        count = code.count('\n')
    print(code)

    lines = code.split('\n')
    li = lines[0]
    line = lines[1]
    if li != '-1' and li not in buffer:
        buffer.add(li)
        server2_socket.send(code.encode('utf-8'))
        response = server2_socket.recv(1024).decode('utf-8')
        print(response)
        if int(response) == 0:
            # d1 = server2_socket.recv(1024)
            c = 0
            file = b''
            while True:
                row_data = server2_socket.recv(1024)
                if not row_data:
                    break
                file += row_data
            dic = pickle.loads(file)
            print(dic)
            print(len(dic))
            msg = 'SUBMIT\n'
            server1_socket.send(msg.encode('utf-8'))
            idk = '2023JCS2561@asap\n'
            server1_socket.send(idk.encode('utf-8'))
            total_data = '1000\n'
            server1_socket.send(total_data.encode('utf-8'))
            size = len(dic)
            if size == 1000:
                dic['1000'] = "this is dammy line"

            for key in dic.keys():
                k = key+'\n'
                v = dic[key]+'\n'
                c += 1
                if c > 1000:
                    resp = server1_socket.recv(1024).decode('utf-8')
                    print(resp)
                    break
                server1_socket.send(k.encode('utf-8'))
                server1_socket.send(v.encode('utf-8'))
            server1_socket.close()
            break

end_time = time.time()
elapsed_time = end_time - start_time

print(elapsed_time)
