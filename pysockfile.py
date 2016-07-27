#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sockfile.py
#  
#  Copyright 2016
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 

import os
import socket 
import struct
from contextlib import closing

BUFFER_SIZE = 256 * 1024
FBI_PORT = 5000

def send_file(filename, ip):
    filesize = os.stat(filename).st_size
    nbfiles = struct.pack("!i", 1)
    fbiinfo = struct.pack("!q", filesize)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with open(filename, "rb") as f:
        with closing(socket.socket()) as sock:
            sock.connect((ip, FBI_PORT))
            sock.send(nbfiles)                
            ack = sock.recv(1)
            if ack == 0:
                print "Send cancelled by remote"
                return
            sock.send(fbiinfo)                
            loop = True
            i = 0
            nbchunks = filesize/BUFFER_SIZE;
            if filesize%BUFFER_SIZE > 0:
                nbchunks=nbchunks+1
            while loop:
                buf = f.read(BUFFER_SIZE)
                if not buf:
                    print "File \"" + filename + "\" sent successfully"
                    loop = False
                else:
                    sock.send(buf)
                    i=i+1
                    print( "%d/%d"%(i,nbchunks) )
        
def main(args):
    ip = args[1]
    filename = args[2]
    print "ip = " + ip
    print "filename = " + filename
    send_file(filename, ip)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
