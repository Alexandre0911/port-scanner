import socket
import threading
from queue import Queue



target = str(input('Target IP Address: ')).lower()
if target == 'localhost':
    target = '192.168.1.1'
else:
    target = target

queue = Queue()
open_ports = []



print('''\nScan Types:
[1] Simple Scan     ->      Port 1 to Port 1024
[2] Advanced Scan   ->      Port 1 to Port 65536
[3] Custom Scan     ->      Custom Port Range''')

ScanType = int(input('\nScan Type (1 ; 2 ; 3): '))
portnumber = 0
if ScanType == 1:
    portnumber = 1024
    port_list = range(1, portnumber)
elif ScanType == 2:
    portnumber = 65536
    port_list = range(1, portnumber)
elif ScanType == 3:
    min_port = int(input('Enter Minimum Port >>> '))
    max_port = int(input('Enter Maximum Port >>> '))
    port_list = range(min_port, max_port+1)


def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port) == False:
            print('\n\033[31mPort {} is closed!\033[m'.format(port))
        elif portscan(port) == True:
            print('\n\033[32mPort {} is open!\033[m'.format(port))
            open_ports.append(port)



fill_queue(port_list)

thread_list = []

print('\nNumber of Threads To Use: ', end='')
tn = int(input(''))



for t in range(tn):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()



print('\nOpen ports are: \033[34m{}\033[m'.format(open_ports))



with open('ports.txt', 'w+') as file:
    if target not in file.read():
        file.write('Ports Opened in {} >>>>> {}'.format(target, open_ports))
    else:
        print('The IP Address \033[34m{}\033[m was already scanned.')
    file.close()