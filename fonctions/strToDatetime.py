# coding: utf-8

import time
from datetime import datetime

def strToDatetime(sDate):
	jour, mois, tmp, heure=sDate.split()
	annee=time.strftime("%Y")
	listmois=[u"janvier", u"février", u"mars", u"avril", u"mai", u"juin", u"juillet", u"aout", u"septembre", u"octobre", u"novembre", u"décembre"]
	mois=listmois.index(mois.lower())+1
	heure, minute=heure.strip().split(":")
	
	datetime_object = datetime.strptime("{} {} {}  {}:{}".format(jour, mois, annee, heure, minute), "%d %m %Y %H:%M")
	return(datetime_object)