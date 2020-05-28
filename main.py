from urllib.request import urlopen, urlretrieve, Request
from time import sleep
import sys
import os



subreddit = input("Subreddit: ")

if not os.path.isdir(subreddit):
	os.makedirs(subreddit)

url = "https://www.reddit.com/r/"+subreddit+"/"

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

while True:
	try:
		page = urlopen(url)
		break
	except Exception as e:
		sys.exit(e)
bv = page.read()
html = bv.decode()

html = html[:html.rfind("<script>")]

f1 = open("html.txt","w")
f1.write(html)

a = html.find('https://preview.redd.it/')
b = 0
while 0 == html[a:].find('https://preview.redd.it/award_images'):
	a += html[a+10:].find('https://preview.redd.it/') + 10

done = set()
tdone = set()

i = 0
while a != 9:

	b = html[a:].find("jpg")
	img = html[a:a+b+3].replace('preview','i')

	c = html[:a].rfind("</h3>")
	d = html[:c].rfind(">")+1
	title = html[d:c]

	if img not in done and title not in tdone and len(img) == len("https://i.redd.it/wzwlj4b8xd151.jpg"):
		print(title+".jpg")
		try:
			urlretrieve(img, subreddit+"/"+title+".jpg")
		except Exception as e:
			break
		done.add(img)
		tdone.add(title)
	elif img == "":
		break
	i += 1
	a += html[a+10:].find('https://preview.redd.it/') + 10
	while 0 == html[a:].find('https://preview.redd.it/award_images'):
		a += html[a+10:].find('https://preview.redd.it/') + 10
		