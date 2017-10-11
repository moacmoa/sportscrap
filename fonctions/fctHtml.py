# coding=UTF-8

""" Fonctions permettant de r�cup�rer le code HTML d'une url (m�thode normae ou POST) """

from urllib2 import urlopen, Request
from urllib import urlencode, urlretrieve
import os, sys

def getHtml(url):
	""" Fonction renvoyant le code HTML d'une URL"""
	try:
		print("coucou")
		user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.168 Chrome/18.0.1025.168 Safari/535.19'
		rq=Request(url, headers={'User-Agent': user_agent})
		usock=urlopen(rq)
		print(url, usock.getcode())
		html = usock.read()
		usock.close()
		return(html)
	except:
		return(None)
	
def postHtml(url, params):
	"""Fonction permettant de passer des param�tres 'POST'
	- url correspond a la page
	- params est un dictionnaire dont le cl� est le nom du param�tre"""
	
	p = urlencode(params).encode('utf-8')
	f = urlopen(url, p)
	html=f.read()
	f.close()
	return(html)
	
def download(url, filename, path=""):
	"""Fonction permettant de t�l�charger un fichier"""
	import string
	if path and path[-1]!="/":
		path+="/"
	path=path.decode("utf-8")
	filename=filename.replace("\"", "'")
	filename=filename.replace("/", "-")
	forbid_chars=["\"", "/", "\\", "*", "?", "<", ">", "|", ":"]
	filename="".join(c for c in filename if c not in forbid_chars)
	# valid_chars = u"àâçèéêîôùûäëïöü-_.()[]'°& %s%s" % (string.ascii_letters, string.digits)
	# filename="".join(c for c in filename if c in valid_chars)
	urlretrieve(url, path+filename)
	return(path+filename)
