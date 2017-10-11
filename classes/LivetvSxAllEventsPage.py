# coding: utf-8

from classes.LivetvSxWebPage import LivetvSxWebPage
from classes.LivetvSxSportPage import LivetvSxSportPage
from bs4 import BeautifulSoup
# from datetime import datetime, timedelta
# from fonctions.strToDatetime import strToDatetime

class LivetvSxAllEventsPage(LivetvSxWebPage):
	def getSports(self, deltahours=None):
		#Récupération du code HTML de la page
		if not self.html:
			self.get()
		
		#Souping
		# print("[INFO] Souping")
		soup=BeautifulSoup(self.html, "lxml")
	
		# Recherche de la balise span qui contient le nom du sport
		# span=soup.findAll("span", { "class": "sltitle" })[0]
		# self.sport=span.text.strip()
		
		# On cherche dans la table suivante les balise <a> qui conernent un live
		# table=span.findNext("table")
		aTags=soup.findAll("a", { "class": "main" })
		
		#On parcour les balises de live
		self.sports=[]
		for aTag in aTags:
			sport=aTag.text.replace("\n", " ").strip()
			if sport:
				self.sports.append(LivetvSxSportPage(self.domain+aTag["href"]))
		
		return(self.sports)
		
		
	def getDictForJson(self):
		d=self.__dict__
		d.pop("html", None)
		d.pop("headers", None)
		d.pop("session", None)
		d.pop("params", None)
		sports=[s.getDictForJson() for s in self.sports]
		d["sports"]=sports
		return(d)