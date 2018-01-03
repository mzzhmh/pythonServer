#!/usr/local/bin/python

import xml.etree.ElementTree as ET
import sys
import requests
import json

showJSON=False

if len(sys.argv) == 5:
	api_key = sys.argv[2]
	domain = sys.argv[1]
	password = sys.argv[3]
	xmlfile = sys.argv[4]
elif (len(sys.argv) == 3) and (sys.argv[1] == "-v"):
	showJSON=True
	xmlfile = sys.argv[2]
else:
	print "Usage: "+sys.argv[0]+" <companyName> <admin login name> <admin password> <User0.xml>\n[This is used for extracting contacts from xml file and inject them to the freshdesk server via RESTful API]"
	print "OR"
	print "Usage: "+sys.argv[0]+" -v <User0.xml>\n[This is used for just showing the JSON packets which will be sent to the freshdesk server]"
	sys.exit(1) 

tree = ET.parse(xmlfile)
root = tree.getroot()

outfile=open("./freshdeskCustomers.log", 'w+')

mapfile=open("./custIDmap",'w+')
	
for child in root:
	customerID = ""
	for cname in child.iter('name'):
		customerName = cname.text
	for email in child.iter('email'):
		customerEmail =  email.text
	for custID in child.iter('id'):
		customerID = custID.text

	tmpstr = customerEmail + " " + customerID + "\n"
	mapfile.write(tmpstr)
	
	contact_info = { "name" : customerName, "email" : customerEmail, "phone" : "", "mobile" : "", "address" : "" }
	if(showJSON):
		print contact_info
		print "\n"
	else:
		headers = { "Content-Type" : "application/json" }
        	r = requests.post("https://"+ domain +".freshdesk.com/api/v2/contacts", auth = (api_key, password), data = json.dumps(contact_info), headers = headers)

        	if r.status_code == 201:
               		print "Contact created successfully, the response is given below" + r.content
               		print "Location Header : " + r.headers['Location']
	       		outfile.write(r.content+"\n")
        	else:
               		print "Failed to create contact, errors are displayed below,"
               		response = json.loads(r.content)
               		print response["errors"]
	       		outfile.write(customerName+": \n")
	       		outfile.write(r.content)
	       		outfile.write("\n")

               		print "x-request-id : " + r.headers['x-request-id']
               		print "Status Code : " + str(r.status_code)

       ##make agent if neccessary
##        if(customerEmail == "mark@creativecomputing.com.au") or (customerEmail == "jon@creativecomputing.com.au") or (customerEmail == "jenny@crecom.com.au") or (customerEmail == "kafu@crecom.com.au") or (customerEmail == "bernie@creativecomputing.com.au"):
##		headers = { "Content-Type" : "application/json" }
##		agent_info = { }

