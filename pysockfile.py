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

def send_file(files, ip):
    with closing(socket.create_connection((ip, FBI_PORT),2)) as sock:
        sock.settimeout(None)
        counter=len(files)
        counterinfo=struct.pack('!i', counter)
        sock.send(counterinfo)
        print 'Sending files...'
        for filename in files:
            filesize=os.stat(filename).st_size
            fbiinfo=struct.pack('!q', filesize)                      
            with open(filename, 'rb') as f:
                ack=sock.recv(1)
                if ack == 0:
                    print 'Send cancelled by remote'
                    return
                print 'Sending info for \'%s\'...'%filename
                sock.send(fbiinfo)                
                loop=True
                i=0
                print 'Sending data for \'%s\'...'%filename 
                while loop:
                    buf=f.read(BUFFER_SIZE)
                    if not buf:
                        print 'File \'%s\' sent successfully'%filename
                        loop=False
                    else:
                        i+=sock.send(buf)
                        print '%d/%d'%(i,filesize)
        print 'All files sent successfully'
        
def main(args):
    ip = args[1]
    files = args[2:]
    print 'ip = ' + ip
    print 'files = ' + str(files).strip('[]')
    send_file(files, ip)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
