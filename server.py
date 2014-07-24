import socket
import threading
from flush_module import *
from chkdisk import *
import os


def flusher(perc,List):
            for i in List:
               os.system('mount -t xfs -L %s /srv/node/%s'%(i,i))
	    fp = open('/usr/bin/flushConfig','w')
	    fp.write('true')
	    fp.close()
            flush()
            os.system('rm -rf /srv/node/ssd/objects/*')
            for i in range(ord('c'),ord('e')):
                 os.system('umount /dev/sd%s'%(chr(i)))
                 os.system('hdparm -y /dev/sd%s'%(chr(i)))
	    fp = open('/usr/bin/flushConfig','w')
            fp.write('false')
            fp.close()

def main():
	f = open('/usr/bin/spinDownDevices','r')
        Str = f.read()
        List = Str.split('\n')
        List.remove('')
        f.close()
	serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serv.bind(('',12321))
	while 1:
		serv.listen(1)
		conn, addr = serv.accept()
		data = conn.recv(512)
		if data == '*!':
			perc = check('/dev/sde')
		 	if perc > 8:
				 t = threading.Thread(target=flusher,args = (perc,List))
				 t.start()
		#	    for i in List:
		#		os.system('mount -t xfs -L %s /srv/node/%s'%(i,i))	
		#	    flush()
		#	    os.system('rm -rf /srv/node/ssd/objects/*')
		#	    for i in range(ord('c'),ord('e')):
		#		os.system('umount /dev/sd%s'%(chr(i)))
		#		os.system('hdparm -y /dev/sd%s'%(chr(i)))
		conn.send('done')

if __name__ == '__main__':
	main()


