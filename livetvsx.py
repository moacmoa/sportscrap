from classes.LivetvSxAllEventsPage import LivetvSxAllEventsPage

import json, os, datetime, sys
import ftplib

url="http://livetv.sx/enx/allupcoming/"

jsonFile="livetvsx.json"
localdir="/tmp"
localJsonFile=os.path.join(localdir, jsonFile)
configFile=os.path.join(os.environ["HOME"], ".p2pLivesParser")
if os.path.isfile(configFile):
	with open(configFile) as f:
		content=f.read()
	lines=content.split("\n")
	lines=[l for l in lines if l.strip()]
	config={}
	for line in lines:
		key, val = line.split("=")
		config[key]=val
else:
	print("Veuillez créer un fichier \"{}\" et y entrer les informations suivantes :".format(configFile))
	print("ftpserver=ftp.xxxxxxxx.com")
	print("ftplogin=xxxxxxxxx")
	print("ftppassword=xxxxx")
	print("serverdir=/xxxxx")
	sys.exit()

allEventsPage=LivetvSxAllEventsPage(url)
sports=allEventsPage.getSports()

for sport in sports:
	matches=sport.getMatches(deltahours=4)
	print("==============================")
	print(sport.name)
	print("==============================")
	for match in matches:
		links=match.getLinks()
		print("{} ({}) - {}".format(match.name, match.competition, match.datetime))
		for link in links:
			print("\t"+link.makeTitle())
		print("---------------------------------")
with open(localJsonFile, "w") as f:
	dic=allEventsPage.getDictForJson()
	dic["datetime"]=str(datetime.datetime.now())
	f.write(json.dumps(dic))

session = ftplib.FTP(config["ftpserver"], config["ftplogin"], config["ftppassword"])
file = open(localJsonFile,'rb')
session.storbinary('STOR '+os.path.join(config["serverdir"], jsonFile), file)
file.close()
session.quit()