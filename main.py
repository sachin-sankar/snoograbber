import praw
from requests import get
from user_agent import generate_user_agent
from shutil import copyfileobj
from redgifdl import download as downloadRedGifs
import os

reddit = praw.Reddit(
    client_id="hi68JmCO_lEXGFWWjMvpZQ",
    client_secret="CR_IXnjOA-qw02lcD0JGiSFo6i8rrg",
    password="Ayush2010",
    user_agent="gifgraber.chickengeek.app: by chickengeek",
    username="Akhilucky",
)

def downloadMedia(url : str,folder: str = ''):
	print(f'Downloading {url}')
	try:
		res = get(url, stream = True,headers={'User-Agent':generate_user_agent(device_type='desktop')})
	except Exception as e:
		print(e)
		quit()
	fileName = folder + '/' + url.split('/')[-1]
	if os.path.exists(fileName):
		print(f'File {fileName} aldready exists')
		return
	if res.status_code == 200:
	    try:
		    with open(fileName,'wb') as f:
	        	copyfileobj(res.raw, f)
	        	print('Downloaded image',fileName)
	        	return fileName
	    except FileExistsError:
	    	print(f'{fileName} aldready exists')
	else:
		print(res.status_code)

def downloadImgur(url):
	downloadMedia(url.replace('.gifv','.mp4'),folder='results')

def downloadRedgifs(url):
	if os.path.exists(f"results/{url.split('/')[-1]}.mp4"):
		print(f'File results/{url.split(\'/\')[-1]}.mp4} aldready exists')
		return
	print(f'Downloading {url}')
	downloadRedGifs.url_file(redgifs_url=url, filename=f"{url.split('/')[-1]}.mp4")
	os.rename(f"{url.split('/')[-1]}.mp4",f"results/{url.split('/')[-1]}.mp4")	

def getGfycat(url):
	return get(url).url

def getSubreddit(sub,sort,limit):
	sub = reddit.subreddit(sub)
	if sort == 'top':
		a =  sub.top(limit=limit)
	urls = [i.url for i in a]
	print(f'Downloading {len(urls)} posts')
	for url in  urls:
		if 'redgifs.com' in url:
			downloadRedgifs(url)
		elif 'imgur' in url:
			downloadImgur(url)
		elif 'gfycat' in url:
			if 'redgifs' in getGfycat(url):
				downloadRedgifs(url)
		else:
			print(f'{url} not supported')