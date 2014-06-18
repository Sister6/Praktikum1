# import required module
import socket
import select
import sys
import pickle   # module for object serialization in python
from xml.etree import ElementTree
document = ElementTree.parse( 'cuaca.xml' )
# creating socket server object, bind, and listen
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 45086))
server_socket.listen(5)

# list to store accepted client
input_list = [server_socket]

try:
    while 1:
        # serving multiple client alternately; one socket in a time
        input, output, exception = select.select(input_list, [], [])
    
        for socket in input:
            # accept client and add it to list input
            if socket == server_socket:            
                client_socket, client_address = server_socket.accept()
                input_list.append(client_socket)
                print "Accepted client: ", client_address                           
            
            # handle sending and receiving message    
            else:                                        
                message = socket.recv(1024)                
                if message:
                    # unpickle message
                    message = pickle.loads(message)
                    print "Send to client : ", client_address, message
                    if message == 'semua':
                        msg = ''
                        cuaca = document.find('tahun')
                        for node in cuaca.getiterator():
                            msg += node.attrib['id']+' '+node.text+'\n'
                        message = pickle.dumps(msg)
                    else:
                    # pickle message and send it back to client    ..
                        tanggal = message.split( )
                        cuaca = document.find('tahun[@id="'+tanggal[2]+'"]/bulan[@id="'+tanggal[1]+'"]/tanggal[@id="'+tanggal[0]+'"]')
                        for node in cuaca.getiterator():
                            message = pickle.dumps(message+' - '+node.text)
                    socket.send(message)
                else:                    
                    socket.close()                    
                    input_list.remove(socket)

# when user press CTRL + C (in Linux), close socket server and exit
except (KeyboardInterrupt, SystemExit):
    server_socket.close()
    sys.exit(0)