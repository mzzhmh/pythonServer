#!/usr/bin/python

from thread import *
import socket
import sys
from subprocess import Popen, PIPE
import os

def clientthread(conn,addr):
    reply = ""
    cmd = ""
    threadID=str(get_ident())
    print threadID+':Accept Connection from ' + addr[0] + ':' + str(addr[1])
    buffer=""

	#setup the ccdir and ld library
    os.environ['CCDIR'] = '/u/ccr.14/'
    os.environ['LD_LIBRARY_PATH'] = '/u/ccr.14/lib:/lib:/usr/lib'
    binPath="/u/ccr.14/std/binl/"


	#read the command from the web perl
    while True:
		buffer = conn.recv(1024)
		if len(buffer)>0:
			print threadID+':Received STRING: '+buffer
			break

	#parse the cmd
    cmd = buffer.split(" ")[0]
    args = " ".join(buffer.split(" ")[1:])

    print threadID+":CMD:"+binPath+cmd
    print threadID+":ARGS:"+args

	#execute the control cmd
    process = Popen([binPath+cmd,args], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    print threadID+":exit code:"+str(exit_code)
    print threadID+":output:"+output
    print threadID+":err:"+str(err)
    
    if(len(output)):
        reply = output

	#send back the output and exit this thread.
    conn.sendall(reply)
    conn.close()

host = 'sam'
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host, port))
s.listen(128)
print "Server listening on %s %d" %(host, port)
while(1):
	conn, addr = s.accept()
	start_new_thread(clientthread ,(conn,addr))
s.close()


