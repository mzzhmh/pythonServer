#!/usr/local/bin/python

#import xml.etree.ElementTree as ET
import sys
import requests
import json
from pprint import pprint

showJSON=False

if len(sys.argv) == 5:
	api_key = sys.argv[2]
	domain = sys.argv[1]
	password = sys.argv[3]
	agentList = sys.argv[4]
elif len(sys.argv) == 6 and sys.argv[5]=="-v":
	api_key = sys.argv[2]
        domain = sys.argv[1]
        password = sys.argv[3]
        agentList = sys.argv[4]
	showJSON = True
else:
	print "Usage: "+sys.argv[0]+" <companyName> <admin login name> <admin password> <Agents.txt>"
	print "[This is used for creating the Agents in <companyName> from the Agents.txt file]"
	print "OR"
	print "Usage: "+sys.argv[0]+" <companyName> <admin login name> <admin password> <Agents.txt> -v"
	print "[Just printing the JSON packet which is used create the Agents in <companyName> from the Agents.txt file]"
	sys.exit(1) 

outfile=open("./freshdeskAgents.log", 'w+')
agentfile=open(agentList, 'r')
	
for email in agentfile:
	email = email.rstrip()
	url = "https://"+ domain +".freshdesk.com/api/v2/contacts"+"?email="+email
	#print url
        r = requests.get(url, auth = (api_key, password))

        if r.status_code == 200:
	       outfile.write(r.content+"\n")

	       #if find contact, let us make it Agent.
	       if (len(r.text.lstrip("[").rstrip("]")) > 0):
               		print "Find the contact successfully, the response is given below:" + r.content
    	       		data = json.loads(r.text)
	       		#print data[0]["id"]

               		headers = { "Content-Type" : "application/json" }
	       		newurl = "https://"+ domain +".freshdesk.com/api/v2/contacts/"+str(data[0]["id"])+"/make_agent"
	       		#print newurl
			if(showJSON):
				print "THE URL that creates the Agent:\n"
				print newurl
				print "\n"
			else:
	       			r = requests.put(newurl, auth = (api_key, password),headers = headers)

	       			if r.status_code == 200:
					print "Make agents successfully, the response is given below:" + r.content
               				outfile.write(r.content+"\n")
	       			else:
					print "Failed to make agent, errors are displayed below,"
               				response = json.loads(r.content)
               				print response["errors"]
               				outfile.write(email+": \n")
               				outfile.write(r.content)
               				outfile.write("\n")
	       else:
               		print "Maybe it is in Agent list."
			agenturl = "https://"+ domain +".freshdesk.com/api/v2/agents"+"?email="+email
			r = requests.get(agenturl, auth = (api_key, password))
			if r.status_code == 200:
				if (len(r.text.lstrip("[").rstrip("]")) > 0):
					print "Already in Agent list, Do NOT NEED to CREATE! <"+email+">\n"
				else:
					print "CAN NOT FIND in Contact and Agent list, please create a contact first! <"+email+">\n"
        else:
               print "Failed to find contact, errors are displayed below,"
               print r.content
	       outfile.write(email+": \n")
	       outfile.write(r.content)
	       outfile.write("\n")


#here, we should have the agents created. let's get the agentID map
agentfile.close()
agentfile=open(agentList, 'r')
agentMap=open("./newAgentIDMap",'w+')
for email in agentfile:
        email = email.rstrip()
	agenturl = "https://"+ domain +".freshdesk.com/api/v2/agents"+"?email="+email
        #print agenturl
        r = requests.get(agenturl, auth = (api_key, password))
	j = json.loads(r.content)
	newAgtID=j[0]['id']
	agtIDstr=email+" "+str(newAgtID)+"\n"
	print agtIDstr
	agentMap.write(agtIDstr)
       ##make agent if neccessary
##        if(customerEmail == "mark@creativecomputing.com.au") or (customerEmail == "jon@creativecomputing.com.au") or (customerEmail == "jenny@crecom.com.au") or (customerEmail == "kafu@crecom.com.au") or (customerEmail == "bernie@creativecomputing.com.au"):
##		headers = { "Content-Type" : "application/json" }
##		agent_info = { }

