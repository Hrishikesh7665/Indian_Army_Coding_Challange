import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
import urllib.request
import os


def wikiResult(query):
	query = query.replace('wikipedia','')
	query = query.replace('search','')
	if len(query.split())==0: query = "wikipedia"
	try:
		return wikipedia.summary(query)
	except Exception as e:
		return "Desired Result Not Found"

path = os.getenv("APPDATA")+"\\H_SearchEngine"

def downloadImage(query, n):
	x=0
	#for i in range(0,query.__len__()):
		#url=[f"https://www.bing.com/images/search?q={query}&go=Search&qs=ds&form=QBIR&first=1&scenario=ImageBasicHover&cw=1901&ch=961"]
	#url=[f"https://www.google.com/search?tbm=isch&q="+query]	# Google
	#url=[f"https://www.bing.com/images/search?q="+query]	#-Bing
	url=[f"https://www.google.com/search?q=search_term"+query+"&sxsrf=ALeKk01Uc1jZmkMslF91v0t6d3JZD9wRWw:1603913331249&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj02u_igtjsAhXCqZ4KHeviDgkQ_AUoAXoECDUQAw&biw=1918&bih=977"]
	for j in range(0,url.__len__()):
		html= requests.get(url[j])
		src=html.content
		soup=BeautifulSoup(src,"lxml")
		links = soup.find_all('img')
		for link in links:
			if x == n:
				break
			imageLink=link.get("src")
			try:
				r = requests.get(imageLink)
				open(f'{path}\\img{x}.jpg', 'wb').write(r.content)
				x+=1
			except Exception:
				pass


