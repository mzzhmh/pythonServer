#!/usr/local/bin/python

import xml.etree.ElementTree as ET
import sys
import os

if len(sys.argv) != 2:
	print "Usage: "+sys.argv[0]+" <Ticket0.xml>"
	print "[It is used for filtering the spam tickets and put the real tickets into <userfile.log>]"
	sys.exit(1)
elif sys.argv[1]=="-h" or sys.argv[1]=="--help":
	print "Usage: "+sys.argv[0]+" <Ticket0.xml>"
        print "[It is used for filtering the spam tickets and put the real tickets into <userfile.log>]"
        sys.exit(1)

xmlfile = sys.argv[1]
context = ET.iterparse(xmlfile, events=('start', 'end')) 
context = iter(context)
event, root = context.next()

logfile = "./"+xmlfile.replace("xml","log")

outfile=open(logfile, 'w')
outfile.close()

outfile=open(logfile, 'a+')

outfile.write("<root>\n")

for event, elem in context:
	if event == 'end' and elem.tag == "helpdesk-ticket":
		deleteElem = elem.find("deleted")
		if(deleteElem.text == "true"):
			root.clear()
			continue
		else:
			spamElem = elem.find("spam")
			if (spamElem.text == "true"):
				root.clear()
				continue
			else:
				outfile.write(ET.tostring(elem))
				root.clear()
				continue

outfile.write("</root>")
outfile.close()
