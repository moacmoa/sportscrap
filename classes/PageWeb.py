# coding=UTF-8
import requests

class PageWeb:
	"""Classe définissant une page Web"""

	def __init__(self, url, params=None, session=None):
		""" Constructeur. Initialisation des attributs de la classe """
		self.url=url
		self.params=params
		if not session:
			session=requests.session()
		self.session=session
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36'
		}
		self.html=""

	def get(self):
		if self.params:
			from urllib import urlencode
			p = urlencode(self.params).encode('utf-8')
			self.url=self.url+"?"+p
		
		self.html=self.session.get(self.url, headers=self.headers).text
		
		return(self.html)
		
	def post(self):
		self.html=self.session.post(self.url, self.params, headers=self.headers).text
		
		return(self.html)

	def __str__(self):
		st="<PageWeb:{}>".format(self.url)
		return(st)
