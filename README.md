pythonServ.py is a python socket server listening on 9999 port and it will receive remote cmds from the 9999 port and spawn a thread to execute the cmd locally and send back the cmd output to remote. 
This is used for frontend web session to execute the backend application in the CCDIR directory and read the output after the execution.
This is a quick rollout so there is no Exception handling at the moment. Will add the Exception handling later.

Example (run 'ls' on remote machine and get the output back):

1.make sure you have '/u/ccr.14/lib' '/u/ccr.14/std/binl/' directory;
2.cp your 'ls' program into '/u/ccr.14/std/binl/' directory;
3.in Terminal 1, run './pythonServ.py 192.168.1.106 9999'
  You will see 'Server listening on 192.168.1.106 9999'
4.in the other machine, you can write your own programs to connect to socket port 9999 to send/recv cmd and output. Or you can use 'telnet 192.168.1.106 9999' to connect and issue 'ls' command.

Sample Outputs:

-------------------------------------------------------------------

[root@localhost pythonServer]# telnet 192.168.1.106 9999
Trying 192.168.1.106...
Connected to 192.168.1.106.
Escape character is '^]'.
ls
pythonServ.py
README.md
Connection closed by foreign host.

--------------------------------------------------------------------

[root@localhost pythonServer]# telnet 192.168.1.106 9999
Trying 192.168.1.106...
Connected to 192.168.1.106.
Escape character is '^]'.
ls -lrt
total 8
-rw-r--r-- 1 root root  329 Jun 27 09:12 README.md
-rwxrwxr-x 1 root root 1805 Jun 27 09:37 pythonServ.py
Connection closed by foreign host.

------------------------------------------------------------------





