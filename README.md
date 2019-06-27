pythonServ.py is a python socket server listening on 9999 port and it will receive cmds from another server on the local 9999 port and spawn a thread to execute the cmd locally and send back the cmd output to the remote server. 

This is used for remote frontend web session to execute the customized backend server side applications in the /u/ccr.14/std/binl/ directory locally and send back the output after the execution.

This is a quick rollout so there is no Exception handling at the moment. Will add the Exception handling later.


<br />
<br />

Examples (receive and run the 'ls' and 'ifconfig' from the remote machine; run it locally then send the output back):


1.make sure the machine has '/u/ccr.14/lib' '/u/ccr.14/std/binl/' directory;

2.cp the 'ls' and 'ifconfig' program into '/u/ccr.14/std/binl/' directory;

3.in local machine Terminal, run './pythonServ.py 192.168.1.106 9999'

  You will see :
  
  'Server listening on 192.168.1.106 9999'
  
4.in the remote machine, you can write your own programs to connect to the socket port 9999 to send/recv cmds and outputs. Or you can use 'telnet 192.168.1.106 9999' to connect and issue 'ls' command for testing.


<br />
<br />



Sample Outputs (from the remote machine):


-------------------------------------------------------------------


[root@localhost]# telnet 192.168.1.106 9999

Trying 192.168.1.106...

Connected to 192.168.1.106.

Escape character is '^]'.

ls -lrt

total 8

-rw-r--r-- 1 root root  329 Jun 27 09:12 README.md

-rwxrwxr-x 1 root root 1805 Jun 27 09:37 pythonServ.py

Connection closed by foreign host.


------------------------------------------------------------------



[root@localhost ~]# telnet 192.168.1.106 9999

Trying 192.168.1.106...

Connected to 192.168.1.106.

Escape character is '^]'.

ifconfig -a


docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500

        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:1d:d4:4c:db  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


em1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500

        inet 192.168.1.106  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a128:61cf:2d6a:867e  prefixlen 64  scopeid 0x20<link>
        ether 34:17:eb:a1:ce:db  txqueuelen 1000  (Ethernet)
        RX packets 24997  bytes 17492928 (16.6 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 16938  bytes 2125935 (2.0 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 20  memory 0xf7c00000-f7c20000


lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536

        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 271  bytes 16575 (16.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 271  bytes 16575 (16.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


virbr0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500

        inet 192.168.122.1  netmask 255.255.255.0  broadcast 192.168.122.255
        ether 52:54:00:b3:fc:ab  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


virbr0-nic: flags=4098<BROADCAST,MULTICAST>  mtu 1500

        ether 52:54:00:b3:fc:ab  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


Connection closed by foreign host.


-------------------------------------------------------------------------------------------------
<br />
<br />
<br />
<br />




