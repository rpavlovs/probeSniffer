#!/usr/bin/env python
from scapy.all import *
import sys

import time
import datetime
import sqlconnect as sqlc

host='10.75.4.46'
user='test'
pwd='test1234'
db='icwgates'
table='signals'
cnx=None

# Add some colouring for printing packets later
GREEN = '\033[92m'
END = '\033[0m'

interface = None
antena_id = None
target_addr = '78:31:c1:30:a1:e6'
cnx = None

def is_sequence_exist(seq):
        global table
	global cnx
        query=("select id from {} where id={}".format(table, seq))
        cursor=sqlc.db_query(cnx, query)
        row=cursor.fetchone()
        if row:
                return True
        else:
                return False

def get_antena_fileds(rssi):
	global antena_id
	if (antena_id == 0):
		return str(rssi) + ",null,null"
	elif (antena_id == 1):
                return "null," + str(rssi) + ",null"
	else:
                return "null,null," + str(rssi) 

def store_signal(seq, rssi):
	global cnx
	global table
	if is_sequence_exist(seq):
		upddata=("update {} set signal_ant{}={} where id={}".format(table, antena_id, rssi, seq))
		sqlc.db_update(cnx,upddata)
	else:
		
		insertdata=("insert ignore into {} values ({},{},now())".format(table, seq, get_antena_fileds(rssi)))
		sqlc.db_insert(cnx, insertdata)
	

def sniffProbes(p):
	src = p[Dot11].addr2
	subtype = p[Dot11].subtype
	seq = p[Dot11].SC

	if (src == target_addr and (subtype == 4 or subtype == 5)) :
		channel = int(ord(p[Dot11Elt:4].info))
        	rssi = (ord(p.notdecoded[-4:-3])-256)
		
		if (channel == 1) :
			print( GREEN
				+ time.strftime("%H:%M:%S")				+ '\t'
				+ 'SRC: ' 			+ str(src)		+ '\t'
				+ 'Channel: ' 			+ str(channel)		+ '\t'
				+ 'RSSI: ' 			+ str(rssi)		+ '\t'
				+ 'Seqence number: '		+ str(seq)		+ '\t'
				+ END )
			store_signal(seq, rssi)


def main():
	global cnx
	global interface
	global antena_id
	
	if len(sys.argv) != 3:
        	print 'Usage: ' + sys.argv[0] + ': interface antenna_id'
        	return
	
	interface = str(sys.argv[1])
	antena_id = str(sys.argv[2])	

	#connect to DB
	cnx=sqlc.db_connect(host,user,pwd,db)
	
	print "Antena " + str(antena_id) + ":"

	sniff(iface=interface, prn=sniffProbes)

	#close db
	sqlc.db_close(cnx)

if __name__ == "__main__":
    main()

