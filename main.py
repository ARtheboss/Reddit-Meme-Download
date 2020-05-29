from urllib.request import urlopen, urlretrieve, Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os


subreddit = input("Subreddit: ")

if not os.path.isdir("downloads/"+subreddit):
	os.makedirs("downloads/"+subreddit)

url = "https://www.reddit.com/r/"+subreddit+"/"

pages = int(input("Number of pages (~5-8 pics/pg):"))*10

opt = Options()
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')  # Last I checked this was necessary.

driver_path = False
for dirpath,_,filenames in os.walk(os.getcwd()):
    for f in filenames:
    	if f == "chromedriver":
        	driver_path = os.path.abspath(os.path.join(dirpath, f))
        	break
if not driver_path:
	driver_path = input("Chrome Driver Path: ")
	driver_path = driver_path[:-1]
browser = webdriver.Chrome(driver_path, options = opt)

browser.get(url)
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

while pages:
    elem.send_keys(Keys.PAGE_DOWN)
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.2)
    pages-=1

html = elem.get_attribute("innerHTML")

html = html[:html.rfind("<script>")]

a = html.find('https://preview.redd.it/')
b = 0
while 0 == html[a:].find('https://preview.redd.it/award_images'):
	a += html[a+10:].find('https://preview.redd.it/') + 10

done = set()
tdone = set() 

start = time.process_time()

i = 0
while a != 9:

	b = html[a:].find("jpg")
	img = html[a:a+b+3].replace('preview','i')

	c = html[:a].rfind("</h3>")
	d = html[:c].rfind(">")+1
	title = html[d:c]

	if img not in done and title not in tdone and len(img) == len("https://i.redd.it/wzwlj4b8xd151.jpg"):
		try:
			urlretrieve(img, "downloads/"+subreddit+"/"+title+".jpg")
		except Exception as e:
			pass
		print(title+".jpg")
		done.add(img)
		tdone.add(title)
		i += 1
	elif img == "":
		break
	a += html[a+10:].find('https://preview.redd.it/') + 10
	while 0 == html[a:].find('https://preview.redd.it/award_images'):
		a += html[a+10:].find('https://preview.redd.it/') + 10
	if time.process_time() - start > 5:
		break
print("# Downloaded: "+str(i))
browser.quit()
		