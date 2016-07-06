# Python selenium 
# intermarchedrive
# Create By Bi-kay Team
# Created on: 07-06-2016
#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# -*- coding: utf-8 -*-
import os, sys
from binascii import b2a_base64
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import ErrorInResponseException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import re
import time
import subprocess
import math
import requests
import numpy
from datetime import date
fs = open("lib/all_shop.txt", "r+")
strs = fs.read()
splitstr = strs.split("\n")

data_store = '../datas/extract_intermarche_'
home = 'https://drive.intermarche.com/'
home_magasin = 'https://drive.intermarche.com/Home?p='
weekNumber = date.today().isocalendar()[1]
month = datetime.datetime.now().strftime ("%m")
mydate = datetime.datetime.now().strftime ("%d-%m-%Y")
post_code = ''
magasin_code = ''
magasin_name = ''
departement = ''
cate_type = []
cate_index = []
links = []
pro_code = ''
type_of_cate = ''
file = ''


# binary = FirefoxBinary(r"/Applications/TorBrowser.app/Contents/MacOS/firefox")
# profile = FirefoxProfile(r"/Applications/TorBrowser.app/TorBrowser/Data/Browser/profile.default")  
# driver = webdriver.Firefox(profile, binary)
driverchrome = '/Users/mesa/Desktop/sdd-extraction/python/intermarche/sources/lib/chromedriver'
driver = webdriver.Chrome(driverchrome)

def existsSelector(selectors):
	return WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, selectors)))

def pageNotFound(link, run):
	r = requests.head(link)
	if r.status_code != 200 or r.status_code == 404 or r.status_code == 403 or r.status_code == 304:
		print('Page response : ' + str(r.status_code))
		print('Page Not Found!!\nReloading Page...\n\n')
		run(link)

def findElement(selectors):
	return driver.find_element_by_css_selector(selectors)

def findElements(selectors):
	return driver.find_elements_by_css_selector(selectors)

def closePopup(panel, close):
	try:
		existsSelector(panel)
		findElement(close).click()
	except TimeoutException:
		print('No popup')

def firstOpen():
	global home
	driver.get(home)
	try:
		existsSelector('.js-lien_tous_les_magasins > a:last-child')
		separatePro()
	except TimeoutException:
		r = requests.head(home)
		if r.status_code != 200:
			print('Page Not Found!!\nReloading Page...')
			firstOpen()

def separatePro():
	global mydate, post_code, magasin_code, splitstr, home_magasin, departement, file
	if len(sys.argv) > 1:
		print('######## Separating Processes ########')
		if sys.argv[1] != '' and sys.argv[2]!='':
			indexstart = int(sys.argv[1])
			separate = int(sys.argv[2])
			if indexstart!='' and separate!='':
				id_start = (indexstart - 1) * math.floor( len(splitstr) / separate )
				if indexstart < separate:
					id_stop = math.floor( len(splitstr) / separate ) * indexstart
					splitstr = splitstr[id_start:id_stop]
				else:
					splitstr = splitstr[id_start:]
		file=open(data_store+""+str(indexstart)+"_"+mydate+".csv","a")
	else:
		file=open(data_store+""+mydate+".csv","a")
	fs.close()
	for line in splitstr:
		tmp_post = re.search('\;\d+', line, re.I)
		if tmp_post:
			post = (tmp_post.group()).strip()
			post_code = re.sub('\;', '', post)
			tmp_depart = re.search('^\d\d', post_code, re.I)
			if tmp_depart:
				departement = (tmp_depart.group()).strip()

		tmp_magasin = re.search('\d+\;', line, re.I)
		if tmp_magasin:
			magasin = (tmp_magasin.group()).strip()
			magasin_code = re.sub('\;', '', magasin)
			url = home_magasin + '' + magasin_code
			openMagasin(url)

def openMagasin(url):
	driver.get(url)
	closePopup('.js-popup_affiche img.ombre3', '.js-btn_fermer_popup_magasin')
	try:
		global magasin_name
		existsSelector('.js-magasins_infos > h2')
		name = findElement('.js-magasins_infos > h2')
		magasin_name = str(name.text)
		print('****** Changing Magasin ******\n>>>>>> Magasin Name ' + magasin_name + ' >>>>>>\n')
		clickCategory()
	except TimeoutException:
		pageNotFound(url, openMagasin)

def clickCategory():
	try:
		existsSelector('ul li .js-click_deployer.js-univers[universtag="fruits_et_legumes"]')
		findElement('ul li .js-click_deployer.js-univers[universtag="fruits_et_legumes"]').click()
		try:
			global cate_type, cate_index, links
			links = []
			cate_type = []
			cate_index = []
			cate = ''
			existsSelector('nav.active.ombre div div h3')
			all_name = findElements('nav.active.ombre div div h3')
			i = 1
			while len(all_name) >= i:
				cate = findElement('nav.active.ombre div div:nth-child('+str(i)+') h3').text
				cate_type.append(cate)
				i = i + 1

			cate_id = 1
			if cate_type:
				for lst in cate_type:
					if lst == 'FRUITS':
						fruit_ind = cate_id
						cate_index.append(fruit_ind)
					if lst == 'LÉGUMES':
						legume_ind = cate_id
						cate_index.append(legume_ind)
					cate_id = cate_id + 1

				start_ind = 1
				while len(cate_index) >= start_ind:
					getLink(str(start_ind))
					start_ind = start_ind + 1

				for url in links:
					eachLinks(url)

		except TimeoutException:
			print('no selector found!!!')
	except TimeoutException:
		print('Selector has changed...')

def getLink(index):
	tmp = []
	try:
		global links
		existsSelector('nav.active.ombre div div:nth-child('+index+') ul li a')
		tmp = findElements('nav.active.ombre div div:nth-child('+index+') ul li a')
		for link in tmp:
			links.append(link.get_attribute('href'))
	except TimeoutException:
		print('Please selectors!!!')

def eachLinks(url):
	driver.get(url)
	try:
		existsSelector('.js-vignette_rayon > .vignettes_produit')
		pro_length = findElements('ul.vignettes_produit li.vignette_produit_info.js-vignette_produit')
		count = 1
		while len(pro_length) >= count:
			clickPro(str(count))
			count = count + 1
	except TimeoutException:
		print('No Product found!!!')

def clickPro(index):
	try:
		global type_of_cate
		type_of_cate = ''
		if existsSelector('span.js-rayon_txt'):
			cate = (findElement('span.js-rayon_txt').text).strip()
			cate = re.search('Légumes', cate, re.I)
			if cate:
				type_of_cate = 2
			else:
				type_of_cate = 1
		tmp_url = driver.current_url
		tmp_code = re.search('(\d+)$', tmp_url, re.I)
		if tmp_code:
			pro_code = (tmp_code.group()).strip()
			print('Product Code : ' + pro_code)

		existsSelector('#content > div > section.ombre3.inline.liste_produits_mae > div.content_vignettes.js-vignette_rayon > ul > li:nth-child('+index+'):not(.non-dispo) > div.vignette_picto_promo.js-ouvrir_fiche > img')
		click = 'document.querySelector("#content > div > section.ombre3.inline.liste_produits_mae > div.content_vignettes.js-vignette_rayon > ul > li:nth-child('+index+'):not(.non-dispo) > div.vignette_picto_promo.js-ouvrir_fiche > img").click();'
		driver.execute_script(click)
		getDetails()
	except TimeoutException:
		print(index)
		print('Error Selector, please Check!!')

def getDetails():
	time.sleep(20)
	try:
		global pro_code, magasin_name, magasin_code, post_code, file, mydate, weekNumber, month, departement, type_of_cate
		type_of_cate = str(type_of_cate)
		magasin_code = str(magasin_code)
		post_code = str(post_code)
		pro_code = str(pro_code)
		departement = str(departement)
		mydate = str(mydate)
		weekNumber = str(weekNumber)
		month = str(month)
		title = ''
		prix_tmp = ''
		prix_kg = ''
		prix_piece = ''
		origine = ''
		category = ''
		calibre = ''
		variete = ''
		img = ''
		pdc = ''
		tdc = ''
		sub_title = ''
		description = ''
		existsSelector('.popup.js-popup_affiche')

		if existsSelector('.fiche_produit_description.vignette_produit_info.inline > div.vignette_info.pop.inline > p.js-fiche_libelle'):
			title = (findElement('.fiche_produit_description.vignette_produit_info.inline > div.vignette_info.pop.inline > p.js-fiche_libelle').text).strip()
			print('Title : ' + title)

			if existsSelector('.js-fiche_conditionnement'):
				sub_title = (findElement('.js-fiche_conditionnement').text).strip()
				tmp_tdc = tdcSeparation(sub_title)
				tdc = re.sub('\s+', ' ', tmp_tdc, re.I)
				tmp_pdc = pdcSeparation(sub_title)
				pdc = re.sub('\s+', ' ', tmp_pdc, re.I)

			if existsSelector('.popup.js-popup_affiche .js-fiche_picto_sur_image'):
				image = findElement('.popup.js-popup_affiche .js-fiche_picto_sur_image')
				img = image.get_attribute('src')

			if existsSelector('.prix_visible.js-fiche_prix'):
				tmp_prix = (findElement('.prix_visible.js-fiche_prix').text).strip()
				prix = re.sub('\€', '', tmp_prix, re.I)
				print('Prix du Vente : ' + prix)

			if existsSelector('p.js-fiche_prix_quantite'):
				prix_tmp = (findElement('p.js-fiche_prix_quantite').text).strip()
				kg_tmp = re.search('kg|g', prix_tmp, re.I)
				piece = re.search('pièce', prix_tmp, re.I)
				if kg_tmp:
					kg = re.search('[1-9].*\d+|\,', prix_tmp, re.I) # [1-9].*\d+|\, ;old = [1-9].|\,
					if kg:
						prix_kg = kg.group()
						prix_kg = re.sub('\,{1,2}', ',', prix_kg, re.I)
						prix_kg = re.sub('\,{1,2}', '.', prix_kg, re.I)
						print('Prix du kg : ' + prix_kg)
				if piece:
					piece_tmp = piece.group()
					prix_piece = re.sub('€.*?|\/|pièce', '', piece_tmp, re.I)
					prix_piece = re.sub('\,', '.', prix_piece, re.I)
					print('Prix de pièce : ' + prix_piece)

			# Information
			if existsSelector('ul li.tab-menu.js-onglet_information'):
				# findElement('ul li.tab-menu.js-onglet_information').click()
				script = "document.querySelector('ul li.tab-menu.js-onglet_information').click();"
				driver.execute_script(script)

			if existsSelector('.js-ligne_origine span.js-fiche_origine'):
				origine = (findElement('.js-ligne_origine span.js-fiche_origine').text).strip()
				print('Origine : ' + origine)

			if existsSelector('.js-ligne_categorie span.js-fiche_categorie'):
				category = (findElement('.js-ligne_categorie span.js-fiche_categorie').text).strip()
				print('Category : ' + category)

			if existsSelector('.js-ligne_calibre .js-fiche_calibre'):
				calibre = (findElement('.js-ligne_calibre .js-fiche_calibre').text).strip()
				print('Calibre : ' + calibre)

			if existsSelector('.js-ligne_variete .js-fiche_variete'):
				variete = (findElement('.js-ligne_variete .js-fiche_variete').text).strip()
				print('Variete : ' + variete)

			datas = mydate + ';intermarche;' + weekNumber + ';' + month + ';' + departement + ';'
			datas += magasin_name + '' + post_code + ';' + type_of_cate + ';' + title + ';' + variete + ';'
			datas += pdc + ';' + tdc + ';' + category + ';' + calibre + ';;;' + origine + ';;' + prix + ';'
			datas += prix_kg + ';' + prix_piece + ';' + description + ';' + img + '\n'
			kiwi = re.search('kiwi', title, re.I)
			if kiwi:
				print('Do not get kiwi product...\nGo to next products\n')
			else:
				file.write(datas)
				print('===========================================\n')
	except TimeoutException:
		print('Product does not show!!!')
	closePopup('.js-popup_affiche', '.js-btn_fermer_fiche_produit')
	time.sleep(5)

def pdcSeparation(arg):
	tmp = arg
	result = ''
	if re.search('\d\sfruits', tmp, re.I):
		pdc = re.search('\d\sfruits', tmp, re.I)
		result = (pdc.group()).strip()
		return result
	elif re.search('\d+\s+gr', tmp, re.I):
		pdc = re.search('\d+\s+gr', tmp, re.I)
		result = (pdc.group()).strip()
		return result
	elif re.search('[0-9,]+\s+g', tmp, re.I):
		pdc = re.search('[0-9,]+\s+g', tmp, re.I)
		result = (pdc.group()).strip()
		return result
	else:
		return result

def tdcSeparation(arg):
	tmp = arg
	result = ''
	if re.search('pièce', tmp, re.I):
		result = 'pièce'
		return result
	elif re.search('sachet', tmp, re.I):
		result = 'sachet'
		return result
	elif re.search('barquette', tmp, re.I):
		result = 'barquette'
		return result
	else:
		return result

firstOpen()
file.close()
driver.close()
