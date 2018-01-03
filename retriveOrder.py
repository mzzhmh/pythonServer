#!/usr/local/bin/python
import mysql.connector
import sys
dump = "seqNum,OrdID,CustID,OrdStat,firtName,lastName,Address,Postcode,Email,ProductList\n"
if len(sys.argv)!=2:
	print sys.argv[0] + " start_ord_id (e.g. 10)"
	sys.exit(1)

ordNum = sys.argv[1]

cnx = mysql.connector.connect(user='root', password='11QQaa!!',
                              host='127.0.0.1',
                              database='cubecart')
cursor = cnx.cursor()
query = ("SELECT * FROM CubeCart_order_summary where id>="+ordNum+";")
#print query
cursor.execute(query)
results = cursor.fetchall()
for row in results:
	seq = row[0]
	orderNum = row[1]
	custId = row[3]
	status = row[4]
	firstName = row[18]
	lastName = row[19]
	address = row[21]+" "+row[23]
	postcode = row[25]
	email = row[39]

	#from the orderNum we need to get all the product 
	prodstr = ""
	newquery = ("SELECT * FROM CubeCart_order_inventory where cart_order_id=\""+orderNum+"\";")
	cursor.execute(newquery)
	#print newquery
	newresults = cursor.fetchall()
	for prodrow in newresults:
	#	print prodrow
		prodstr = prodstr + prodrow[2] + "|"
	prodstr = prodstr[:-1]
	ourRes = ""
	ourRes = str(seq)+","+str(orderNum)+","+str(custId)+","+str(status)+","+firstName+","+lastName+","+address+","+postcode+","+email+","+prodstr
#	print ourRes
	dump = dump + ourRes + "\n"

print dump

text_file = open("Output.csv", "w")

text_file.write(dump)

text_file.close()

cursor.close()
cnx.close()
