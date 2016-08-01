#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import socket 
import struct
import time
from contextlib import closing

BUFFER_SIZE = 256 * 1024
FBI_PORT = 5000

def convert_bytes_to_string(size):
    units=['B','KB','MB','GB','TB']
    pos=0
    while(size>=1024.0 and pos<len(units)-1):
        pos+=1
        size/=1024.0
    return '%.2f%s'%(size,units[pos])

def send_files(files, ip):
    with closing(socket.create_connection((ip, FBI_PORT),2)) as sock:
        sock.settimeout(None)
        counter=struct.pack('!i', len(files))
        sock.send(counter)
        for filename in files:
            start=time.time()
            filesize=os.stat(filename).st_size
            info=struct.pack('!q', filesize)
            with open(filename, 'rb') as f:
                ack=sock.recv(1)
                if ack == 0:
                    raise Exception('Send cancelled by remote')
                sock.send(info)                
                transfered=0
                while transfered<filesize:
                    data=f.read(BUFFER_SIZE)
                    if not data:
                        raise Exception('Cannot read file \'%s\''%filename)
                    else:
                        transfered+=sock.send(data)
                        current=time.time()
                        progress = transfered*100/filesize
                        speed = (transfered/1024.0)/(current-start)
                        yield(filename,convert_bytes_to_string(transfered),convert_bytes_to_string(filesize),progress,speed)
        
def main(args):
    ip = args[1]
    files = args[2:]
    print 'ip = ' + ip
    print 'files = ' + str(files).strip('[]')
    try:
        print 'Sending files...'
        current=''
        for progress in send_files(files, ip):
            if current!=progress[0]:
                current=progress[0]
                print 'Transfer file \'%s\''%current
            print '%s/%s    %3d%%    %.2fKB/s'%progress[1:]
        print 'All files sent successfully'
        return 0
    except Exception as e:
        print 'Transfer failed : %s'%e
        return -1
        

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
