# coding: utf-8

from classes.PageWeb import PageWeb
from classes.Link import Link
from bs4 import BeautifulSoup
import re

class LivetvSxMatchPage(PageWeb):
	def getLinks(self):
		self.links=[]
		self.url=self.url.replace("/frx/", "/enx/")
		#Récupération du code HTML de la page
		if not self.html:
			self.get()
		
		#Souping
		# print("[INFO] Souping")
		soup=BeautifulSoup(self.html, "lxml")
		
		#Récupération du nom du match
		h1=soup.findAll("h1",  { "class": "sporttitle" })[0]
		b=h1.findNext("b")
		self.name=b.text.strip().encode("utf-8")
		
		#Récupération des infos championnat et date/heure
		meta=soup.findAll("meta",  { "itemprop": "startDate" })[0]
		b=meta.findNext("b")
		infos=b.text.strip().encode("utf-8")
		self.competition=".".join(infos.split(".")[:-2]).strip()
		
		# print("{} : {}".format(self.name, self.infos))
		# print(self.name)
		# print(self.competition)
		# print(self.datetime)
		
		#On cherche les tables correspondnts à des liens streaming
		# print("[INFO] Finding tables")
		linktables=soup.findAll("table", { "class": "lnktbj" })
		# print("[INFO] {} tables fond".format(len(linktables)))
		
		#On parcoure les tables trouvées
		for linktable in linktables:
			#Si y a "onclick" dans la balise <a>
			if "onclick=" in linktable.a.__str__():
				#On Parse le contenue de l'attribut "onclick" pour récupérer toutes les infos
				res = re.findall('show_webplayer\(\'(\w+)\',\s*\'(\w+)\',\s*(\w+),\s*(\w+),\s*(\w+),\s*(\w+),\s*\'(\w+)\'\)', linktable.a["onclick"])
				if res:
					streamer,stream_id,eid,lid,ci,si,jj = res[0]
					
					#Si le stream n'est pas dans la table, on ignore
					# if streamer.lower().strip() not in Link.streamer_table:
						# continue
				else:
					streamer="web"
					stream_id=""
			else:
				streamer="web"
				stream_id=""
			
			#Récupération de l'url du lien
			url=linktable.a["href"]
			
			#Détection de la santé du stream
			res = re.findall('(\d+)<span',linktable.__str__())
			if res:
				health=res[0].strip()
			else:
				health="??"
			
			#Detection de la langue du stream					
			try:
				lang=linktable.img["title"].lower().strip()
			except:
				lang="inconnue"
			
			#Détection du bitrate
			res=linktable.findAll("td", {"class": "bitrate"})
			if res:
				bitrate=res[0].text.strip()
			else:
				bitrate=""
				
			link=Link(streamer, stream_id, lang, health, bitrate, url, self)
			self.links.append(link)
			
		return(self.links)
	
	def getDictForJson(self):
		d=self.__dict__
		d.pop("html", None)
		d.pop("headers", None)
		d.pop("session", None)
		d.pop("params", None)
		links=[l.getDictForJson() for l in self.links]
		d["links"]=links
		d["datetime"]=str(self.datetime)
		return(d)