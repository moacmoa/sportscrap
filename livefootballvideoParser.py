#!/usr/bin/env python
# coding=UTF-8

from bs4 import BeautifulSoup
from fonctions.fctHtml import getHtml
# from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import os
import datetime
import re
from lxml import etree


path=os.path.dirname(os.path.realpath(__file__))
url="http://livefootballvideo.com/streaming"
html=getHtml(url)
soup=BeautifulSoup(html, "lxml")
urls=[url]+[e["href"] for e in soup.findAll("a", {"class": "page larger"})]

matchs=[]
all_matchs=[]

for url in urls:
	html=getHtml(url)
	soup=BeautifulSoup(html, "lxml")
	divlist=soup.find("div", {"class": "listmatch"})
	for match in divlist.findAll("li"):
		champ=match.find("div", {"class": "league column"}).text.strip()
		div_dom=match.find("div", {"class": "team column"})
		dom=div_dom.text.strip()
		div_ext=match.find("div", {"class": "team away column"})
		ext=div_ext.text.strip()
		div_btn=match.find("div", {"class": "live_btn column"})
		lien=div_btn.find("a")["href"].strip()
		# div_logoch=match.find("div", {"class": "leaguelogo column"})
		div_date=match.find("div", {"class": "date_time column"})
		timestamp=div_date.find("span", {"class": "starttime time"})["rel"].strip()
		if "online" in div_btn.text.lower():
			dateColor="green"
		else:
			dateColor="red"
		try:
			print("{} - {} [{}]\t{}".format(dom.strip(), ext.strip(), champ.strip(), lien.strip()))
		except:
			continue
		html=getHtml(lien)
		soup=BeautifulSoup(html, "lxml")
		lst_links=[]
		for table in soup.findAll("table", {"class": "streamtable"}):
			for tr in table.findAll("tr"):
				tds=tr.findAll("td")
				if len(tds)<5:
					continue
				logo=tds[0]				# print(logo.img)
				bitrate=tds[3].text.replace("\n", " ").strip()
				channel=tds[1].text.strip()
				lang=tds[2].text.strip()
				a=tds[4].find("a")
				if not a:
					continue
				link=a["href"]
				if "acestream://" in link:
					mode="acestream"
					abv="Ace"
					id=link.split("//")[-1]
				elif "sop://" in link:
					mode="sopcast"
					abv="Sop"
					id=link.split("/")[-1]
				# elif logo.img["alt"]=="acestream":
					# print(link)
					# html2=getHtml(link)
					# if not html2:
						# continue
					# tmp=re.search(r"acestream:\/\/([a-fA-F0-9]{40})", html2)
					# if not tmp:
						# continue
					# link=tmp.group(0)
					# mode="acestream"
					# abv="Ace"
					# id=tmp.group(1)
				else:
					continue
				print("\t{} ({})".format(link, bitrate))
				date=datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d/%m %Hh%M')
				title="[COLOR orange][{}][/COLOR] {} - {} ([I]{}[/I]) [COLOR blue][{}][/COLOR] [COLOR {}][{}][/COLOR]".format(abv, dom, ext, champ, bitrate, dateColor, date)
				dic={
					"link":			link,
					"bitrate":		bitrate,
					"mode":			mode,
					"id":			id,
					"channel":		channel,
					"title":		title,
					"lang":			lang,
				}
				if dic in lst_links:
					continue
				lst_links.append(dic)
				all_matchs.append(dic)
		dic={
			"domicile":		dom,
			"exterieur":	ext,
			"champ":		champ,
			"liens":		lst_links,
			"match_url":	lien,
			"timestamp":	timestamp,
		}
		matchs.append(dic)

root = etree.Element('root')
for m in matchs:
	item=etree.SubElement(root, 'item')
	for key, val in m.iteritems():
		tmp=etree.SubElement(item, key)
		if key=="liens":
			for dic in val:
				tmp2=etree.SubElement(tmp, "item")
				for key2, val2 in dic.iteritems():
					tmp3=etree.SubElement(tmp2, key2)
					tmp3.text=val2
			continue
		tmp.text=val
		
xml = etree.tostring(root, pretty_print=True)
with open(path+'/webUI/matchs.xml', 'w') as the_file:
	the_file.write(xml)

m3u="#EXTM3U\n"
for m in all_matchs:
	m3u+="#EXTINF:-1,{}\n".format(m["title"])
	m3u+=m["link"]+"\n"
	
with open(path+'/webUI/kodi.m3u', 'w') as the_file:
	the_file.write(m3u)
