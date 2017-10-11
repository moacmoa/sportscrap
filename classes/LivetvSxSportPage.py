# coding: utf-8

from classes.PageWeb import PageWeb
from classes.LivetvSxMatchPage import LivetvSxMatchPage
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from fonctions.strToDatetime import strToDatetime

class LivetvSxSportPage(PageWeb):
	domain="http://livetv.sx"
	
	def getMatches(self, deltahours=None):
		#Récupération du code HTML de la page
		self.url=self.url.replace("/enx/", "/frx/")
		
		if not self.html:
			self.get()
		
		#Souping
		# print("[INFO] Souping")
		soup=BeautifulSoup(self.html, "lxml")
	
		# Recherche de la balise span qui contient le nom du sport
		span=soup.findAll("span", { "class": "sltitle" })[0]
		self.name=span.text.strip().encode("utf-8")
		
		# On cherche dans la table suivante les balise <a> qui conernent un live
		table=span.findNext("table")
		aTagsLive=table.findAll("a", { "class": "live" })
		
		#On parcour les balises de live
		self.matches=[]
		for aTagLive in aTagsLive:
			# Récupération de la description
			desc=aTagLive.findNext("span", { "class": "evdesc" })
			lines=desc.text.split("\n")
			lines=[l.strip() for l in lines if l.strip()]
			sDate=lines[0]
			dt=strToDatetime(sDate)
			if deltahours:
				if dt>datetime.now()+timedelta(hours=deltahours):
					continue
			
			matchUrl=LivetvSxSportPage.domain+aTagLive["href"]
			match=LivetvSxMatchPage(matchUrl)
			match.datetime=dt
			self.matches.append(match)
		
		return(self.matches)
		
		
	def getDictForJson(self):
		d=self.__dict__
		d.pop("html", None)
		d.pop("headers", None)
		d.pop("session", None)
		d.pop("params", None)
		matches=[m.getDictForJson() for m in self.matches]
		d["matches"]=matches
		return(d)