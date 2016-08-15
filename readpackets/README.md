# Introduction
--------------

What is raw sockets?
--------------------
A raw socket is used to recieve raw packets. This means packets received at 
the ethernet layer will directly pass to the raw socket. In other words, a raw
socket bypasses the normal TCP/IP processing and sends the packets to the 
specific user application

Raw socket vs other sockets
---------------------------
Other sockets like stream sockets and datagram sockets receive data from the 
transport layer that contains no headers but only the payload. This means that
there is no information about the source IP address and MAC address. If 
applications running on the same machine or on different machines are 
communicating, then they are only exchanging data.

The purpose of a raw socket is completely different. A raw socket allows an
application to directly access lower level protocols, which means a raw socket
receives un-extracted packets. There is no need to provide the port and IP
address to a raw socket, unlike in the case of datagram and stream sockets.

Applications of a raw socket
----------------------------
To develop a packet sniffer, only processes with an effective user ID of 0
are allowed to open raw sockets. So, during the execution of the program, you
have to be the root user

Reference:
----------
[Guide to Raw Sockets](http://opensourceforu.com/2015/03/a-guide-to-using-raw-sockets/)
