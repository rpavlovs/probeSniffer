
import mysql.connector as sql

def db_connect (host, user, pwd, db):
	try:
		cnx=sql.connect(user=user,password=pwd,host=host, database=db)
		return cnx
	except sql.Error as err:
		if err.errno==errorcode.ER_ACCESS_DENIED_ERROR:
			print ("Something is wrong with your user name or password")
		elif err.errno==errorcode.ER_BAD_DB_ERROR:
			print ("Database does not exists")
		else:
			print (err)
			cnx.close()
			sys.exit(1)

# after insert, delete and update operations you have to commit the data
def db_update (cnx, upddata):
	cursor=cnx.cursor()	
	cursor.execute(upddata)
	cnx.commit()
	
def db_query (cnx, query):
	cursor=cnx.cursor()	
	cursor.execute(query)
	return cursor
	
def db_insert (cnx, insertdata):
	cursor=cnx.cursor()
	cursor.execute(insertdata)
	cnx.commit()

def db_delete (cnx, deldata, table="signals"):
	cursor=cnx.cursor()
	cursor.execute(deldata)
	cnx.commit()
	# ignore thr following statement for now
	#if table is empty, reset auto_increment to 1
	#total=cursor.execute("select count(*) from {}".format(table))
	#print ("total= %d" % total)
	#if total==0:
	#	cursor.execute("alter table {} auto_increment=1".format(table))
	
	
def db_close (cnx):
	cursor=cnx.cursor()
	cursor.close()
	cnx.close()
	