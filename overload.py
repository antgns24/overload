#coding=utf-8
#python2
###############################
#         AUTHOR : RIZKI M      #
###############################

import requests
import os
import time
from bs4 import BeautifulSoup as parser

logo= """       Author : Rizki M
  ____               __             __  
 / __ \_  _____ ____/ /__  ___ ____/ /  
/ /_/ / |/ / -_) __/ / _ \/ _ `/ _  /   
\____/|___/\__/_/ /_/\___/\_,_/\_,_/    
                                        """

head={"user-agent":"Mozilla/5.0 (Series40; NokiaX2-02/10.90; Profile/MIDP-2.1 Configuration/CLDC-1.1) Gecko/20100401 S40OviBrowser/1.0.2.26.11"}
host_url='https://mbasic.facebook.com'
ses=requests.Session()

def __cookie():
	cok=open("coki.log", "r").read()
	return {"cookie":cok}

def login():
	os.system('clear')
	print(logo)
	cok=raw_input('[+] cookie > ')
	try:
		n=ses.get(host_url, cookies={"cookies":cok}, headers=head)
		p=parser(n.text, "html.parser")
		if 'mbasic_logout_button' in str(p):
			with open('coki.log', 'w') as f:
				f.write(cok)
				f.close()
				print '[√] login berhasil'
				time.sleep(2)
				menu()
		else:
			print '[×] cookie salah'
			time.sleep(2)
			login()
	except(requests.exceptions.ConnectionError):
		exit('[!] Koneksi Bermasalah')
		
def language():
	r = ses.get(host_url+'/language.php', cookies=__cookie(),headers=head)
	bs = parser(r.text, 'html.parser')
	payload={
		'fb_dtsg':bs.find('input', {'name':'fb_dtsg'})['value'],
		'jazoest':bs.find('input', {'name':'jazoest'})['value'],
		'submit':'Bahasa Indonesia' }
	return ses.post(host_url+'/intl/save_locale/?loc=id_ID&amp;ls_ref=m_basic_locale_selector', data=payload, cookies=__cookie(), headers=head)

def menu():
	os.system('clear')
	try:
		p=ses.get(host_url+'/profile.php?', cookies=__cookie(), headers=head)
		h=parser(p.text, "html.parser")
		n=h.find('title')
		if 'mbasic_logout_button' in str(h):
			print(logo)
			print '[•] welcome > '+str(n.string)
			print '\n[1]. Aktifkan overload'
			print '[2]. Hapus overload'
			print '[0]. Keluar\n'
			while True:
				m=raw_input('[+] Pilih > ')
				if m=="1":
					aktif()
				elif m=="2":
					nonaktif()
				elif m=="0":
					exit()
				else:
					continue
		else:
			print '[!] cookie mati'
			os.system('rm -rf coki.log')
			time.sleep(2)
			login()
	except(requests.exceptions.ConnectionError):
		exit('[!] Koneksi Bermasalah')
	except(ValueError):
		print '[!] cookie mati'
		os.system('rm -rf coki.log')
		time.sleep(2)
		login()
	except IOError:
		login()
		
def aktif():
	language()
	next='/editprofile.php?type=contact&edit=website&refid=17'
	try:
		print('[•] silahkan tunggu beberapa menit ... ')
		fo=open("font.txt", "r").read()
		for c in range(10):
			u=ses.get(host_url+next, cookies=__cookie(), headers=head)
			x=parser(u.text, "html.parser")
			data={
				"fb_dtsg":x.find("input", {"name":"fb_dtsg"})["value"],
				"jazoest": x.find("input", {"name":"jazoest"})["value"],
				"type":"contact",
				"edit":"website",
				"add_website":"1",
				"new_info":"https://overloadrizki.com/"+fo,
				"save":"Tambahkan"
				}
			y=ses.post(host_url+'/a/editprofile.php', data=data, cookies=__cookie(), headers=head)
		exit('[√] sukses mengaktifkan')
	except requests.exceptions.ConnectionError:
		exit('[!] Koneksi Bermasalah')
	except IOError :
		exit("[!] file 'font.txt' tidak ada")
	
def nonaktif():
	language()
	try:
		c=ses.get(host_url+'/editprofile.php?type=contact&edit=website&refid=17', cookies=__cookie(), headers=head)
		h=parser(c.text, "html.parser")
		if 'Hapus' in str(h):
			print '[•] sedang menghapus... '
			for f in h.find_all('a', string='Hapus', href=True):
				k=f['href']
				y=ses.get(host_url+str(k), cookies=__cookie())
			exit('[√] sukses menghapus')
		else:
			exit('[!] overload sudah dihapus')
	except requests.exceptions.ConnectionError:
		exit('[!] Koneksi Bermasalah')
	
if __name__ == '__main__':
	menu()
