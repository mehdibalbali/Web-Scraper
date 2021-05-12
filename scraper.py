'''
projet IDL L3 informatique université Paris8

Ce Scraper fait extraire les données textuelles a partir des liens fournis dans un ficher text
'''
import re 
import sys
import requests
import ssl
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def usage():
    print("python3 scraper.py  <file name>.txt")

'''
fonction pour extraire les liens du ficher
'''
def extract(links):
    count = 1 
    for link in links:
        filee = "lien_" + str(count)+"_scrapped" + ".txt"
        scraps(str(link),filee)
        count = count + 1
    
          
'''
 fonction pour supprimer les balises html du ficher text 
'''
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def scraps(link, outf):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    print(" Scraping pour ",link)
    
    
    # pour resoudre l'erreur du SSL 
    ctx_no_secure = ssl.create_default_context()
    ctx_no_secure.set_ciphers('HIGH:!DH:!aNULL')
    ctx_no_secure.check_hostname = False
    ctx_no_secure.verify_mode = ssl.CERT_NONE


    req = Request(link, headers=headers)
    page_html = urlopen(req,context=ctx_no_secure).read()
    page_sup = BeautifulSoup(page_html, "html.parser")
    container = page_sup.find_all("body")

    out = open(outf, 'w')

    for div in container:
        balise = div.find_all("p")
        out.write(cleanhtml(str(balise)) + '\n')
   
    out.close()


def main():
    if len(sys.argv)==2:
        links = open(sys.argv[1],'r')
        extract(links)
    else:
         usage()

if  __name__ == '__main__':
    main()
