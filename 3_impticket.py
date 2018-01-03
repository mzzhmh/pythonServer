#!/usr/local/bin/python

#import xml.etree.ElementTree as ET
import lxml.etree as ET
import sys
import os
import argparse

showJSON=False

if len(sys.argv) == 5:
	api_key = sys.argv[2]
	domain = sys.argv[1]
	password = sys.argv[3]
	xmlfile = sys.argv[4]
	#if sys.argv[5] == "-v":
	#	showJSON=True
elif len(sys.argv) == 6 and sys.argv[5] == "-v":
	api_key = sys.argv[2]
        domain = sys.argv[1]
        password = sys.argv[3]
        xmlfile = sys.argv[4]
	showJSON=True
else:
        print "Usage: "+sys.argv[0]+" <companyName> <admin login name> <admin password> <Ticket01.log>"
	print "[Used for export the tickets in Ticket01.log into the <companyName> freshdesk server.]"
	print "OR"
	print "Usage: "+sys.argv[0]+" <companyName> <admin login name> <admin password> <Ticket01.log> -v"
        print "[Used for printing the JSON packets that export the tickets in Ticket01.log into the <companyName> freshdesk server.]"
        sys.exit(1)


emailToID={}
IDToemail={}
custMap=open("./custIDmap",'r')
for line in custMap:
	(custEmail,custID) = line.split()
	emailToID[custEmail] = custID
	IDToemail[custID] = custEmail
print "---------------- Customer Map ---------------------"
print emailToID
print "--------------------"
print IDToemail
print "---------------------------------------------------\n\n"

context = ET.iterparse(xmlfile, events=('start', 'end')) 
context = iter(context)
event, root = context.next()
notesMap= []  #e.g. sender=mark@creativecomputing.com.au, val=the reply from mark

for event, elem in context:
	if event == 'start' and elem.tag == "notes":
		notesMap=[] #clear the notesbuffer
	if event == 'end' and elem.tag == "helpdesk-note":
		body = elem.find("body").text
		fromWho = IDToemail[elem.find("user-id").text]
		tup = (fromWho,body)
		notesMap.append(tup)
	if event == 'end' and elem.tag == "helpdesk-ticket":
		desc = elem.find("description").text
		subj = elem.find("subject").text
		sts = elem.find("status").text
		ticketID = elem.find("display-id").text
		reqName = elem.find("requester-name").text
		agt = elem.find("responder-name").text
		pri = 2
		src = 1
		print "\n\n"
		print "####################### ONE TICKET ENTRY #########################\n"
		print "ID  :"+ticketID.encode('utf8')+"\n"
		print "From:"+reqName+"\n"
		print "TO  :"+agt+"\n"
		print "============= SUBJECT ======================\n"
		print subj.encode('utf8')+"\n"
		print "============= STATUS =====================\n"
		print sts.encode('utf8')+"\n"
		print "============= DESCRIPTION ==================\n"
		print desc.encode('utf8')+"\n"
		print "============================================\n"
		for tt in notesMap:
			print "Reply From:"+tt[0]+"\n"
			print "-----------------------------"
			print tt[1]+"\n"
			print "============================================\n"
		print "\n\n"

		root.clear()
		
