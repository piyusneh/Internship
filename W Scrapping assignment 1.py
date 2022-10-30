#!/usr/bin/env python
# coding: utf-8

# # Write a python program to display all the header tags from wikipedia.org.

# In[3]:


#importing required libraries
from bs4 import BeautifulSoup
import requests


# In[4]:


page=requests.get("https://en.wikipedia.org/wiki/Wikipedia")


# In[5]:


page.content


# In[6]:


soup=BeautifulSoup(page.content,'html.parser')


# In[7]:


Heading=[]


# In[8]:


heading=soup.find_all("span",class_="mw-headline")
heading


# In[9]:


for i in heading:
    Heading.append(i.get_text())
Heading   


# In[10]:


import pandas as pd
Heading_wiki=pd.DataFrame({})
Heading_wiki["Heading"]=Heading


# In[11]:


Heading_wiki.to_csv("Wikipedia Main page.csv",index=False)


# # Write a python program to display IMDB’s Top rated 100 movies’ data (i.e. name, rating, year of release)
# 

# In[13]:


from bs4 import BeautifulSoup
import requests
import re


# Downloading imdb top 250 movie's data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]

ratings = [b.attrs.get('data-value')
		for b in soup.select('td.posterColumn span[name=ir]')]

votes = [b.attrs.get('data-value')
		for b in soup.select('td.ratingColumn strong')]

list = []

# create a empty list for storing
# movie information
list = []

# Iterating over movies to extract
# each movie's details
for index in range(0, 101):
	
	# Separating movie into: 'place',
	# 'title', 'year'
	movie_string = movies[index].get_text()
	movie = (' '.join(movie_string.split()).replace('.', ''))
	movie_title = movie[len(str(index))+1:-7]
	year = re.search('\((.*?)\)', movie_string).group(1)
	place = movie[:len(str(index))-(len(movie))]
	data = {"movie_title": movie_title,
			"year": year,
			"place": place,
			"star_cast": crew[index],
			"rating": ratings[index],
			"vote": votes[index],
			"link": links[index]}
	list.append(data)
print('\033[1m'+'IMDB’s Top rated 100 movies of all time'+'\033[0m')
# printing movie details with its rating.
for movie in list:
	print(movie['place'], '-', movie['movie_title'], '('+movie['year'] +
		') -', 'Starring:', movie['star_cast'], movie['rating'])


# # Write a python program to display IMDB’s Top rated 100 Indian movies’ data (i.e. name, rating, year of release ) and make data frame
# 

# In[14]:


from bs4 import BeautifulSoup
import requests
import re


# Downloading imdb top 250 movie's data
url = 'https://www.imdb.com/india/top-rated-indian-movies/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]

ratings = [b.attrs.get('data-value')
		for b in soup.select('td.posterColumn span[name=ir]')]

votes = [b.attrs.get('data-value')
		for b in soup.select('td.ratingColumn strong')]

list = []

# create a empty list for storing
# movie information
list = []

# Iterating over movies to extract
# each movie's details
for index in range(0, 101):
	
	# Separating movie into: 'place',
	# 'title', 'year'
	movie_string = movies[index].get_text()
	movie = (' '.join(movie_string.split()).replace('.', ''))
	movie_title = movie[len(str(index))+1:-7]
	year = re.search('\((.*?)\)', movie_string).group(1)
	place = movie[:len(str(index))-(len(movie))]
	data = {"movie_title": movie_title,
			"year": year,
			"place": place,
			"star_cast": crew[index],
			"rating": ratings[index],
			"vote": votes[index],
			"link": links[index]}
	list.append(data)

print('\033[1m'+'IMDB’s Top rated 100 Indian movies'+'\033[0m')
# printing movie details with its rating.
for movie in list:
	print(movie['place'], '-', movie['movie_title'], '('+movie['year'] +
		') -', 'Starring:', movie['star_cast'], movie['rating'])


# # Write s python program to display list of respected former presidents of India(i.e. Name , Term of office)
# 

# In[18]:


import requests
r = requests.get('https://www.nytimes.com/interactive/2017/06/23/opinion/trumps-lies.html')

from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all('span', attrs={'class':'short-desc'})

records = []
for result in results:
    date = result.find('strong').text[0:-1] + ', 2017'
    lie = result.contents[1][1:-2]
    explanation = result.find('a').text[1:-1]
    url = result.find('a')['href']
    records.append((date, lie, explanation, url))

import pandas as pd
df = pd.DataFrame(records, columns=['date', 'lie', 'explanation', 'url'])
df['date'] = pd.to_datetime(df['date'])
df.to_csv('trump_lies.csv', index=False, encoding='utf-8')


# # Write a python program to scrape cricket rankings from icc-cricket.com. You have to scrape:
# a) Top 10 ODI teams in men’s cricket along with the records for matches, points and rating.
# b) Top 10 ODI Batsmen along with the records of their team and rating.
# c) Top 10 ODI bowlers along with the records of their team and rating.# 

# # i) Top 10 ODI teams in men’s cricket along with the records for matches, points and rating.# 

# In[20]:


from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests

url = 'https://www.icc-cricket.com/rankings/mens/team-rankings/odi'

response = requests.get(url)
print(response.status_code, '--->',url)
print('\n')
soup= BeautifulSoup(response.content, 'lxml')


Team=[]
Matches=[]
Points=[]
Rating=[]
Country = soup.find_all('span',class_="u-hide-phablet")
for i in Country:
    Team.append(i.get_text().replace("\n",""))
    Team=Team[0:10]

match=soup.find_all('td',class_='rankings-block__banner--matches')
matchs=soup.find_all('td',class_='table-body__cell u-center-text')
mtc = match + matchs

for i in mtc:
    Matches.append(i.text)
    Matches=Matches[0:10]
    
pt=soup.find_all('td',class_="rankings-block__banner--points")

pts= soup.find_all('td',class_ ="table-body__cell u-center-text")
Point= pt + pts
for i in Point:
    Points.append(i.get_text().replace("\n",""))
    Points=Points[0:10]
rating = soup.find_all('td',class_="table-body__cell u-text-right rating")
for i in rating:
    Rating.append(i.get_text().replace("\n",""))
    Rating=Rating[0:10]
    
ODI=pd.DataFrame({})
ODI['Country']=Team
ODI['Matches']=Matches
ODI['Rating']=Rating
ODI['Points']=Points
print('\033[1m'+'ICC MENS ODI RANKING'+'\033[0m') # Print Title in bold case
ODI


# ii) Top 10 ODI Batsmen in men along with the records of their team and rating.# ii) Top 10 ODI Batsmen in men along with the records of their team and rating.

# In[21]:


# ICC Bating Ranking

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

response = requests.get(url)
print(response.status_code, '--->',url)
print('\n\n')
soup= BeautifulSoup(response.content, 'lxml')
Position =[]
Player =[]
Country =[]
Rating =[]

# Extracting Data of Top Player from Banner
block_1= soup.find('tr', attrs={'class':'rankings-block__banner'}) # contains Top Player ranking detail

Position.append(block_1.find('td',class_='rankings-block__position').text)# Ranking Position
Player.append(block_1.find('div', class_="rankings-block__banner--name-large").text) # Extract Player Name
Country.append(block_1.find('span', class_='rankings-block__banner--nation').text)# Extract Country Name
Rating.append(block_1.find('div', class_="rankings-block__banner--rating").text) # Extract Rating

# Extracting other Player Ranking
table_rows =soup.find_all('tr', attrs={'class':'table-body'})

for row in table_rows[:10]:
    Position.append(row.find('td', class_='table-body__cell table-body__cell--position u-text-right').text.replace('\n',''))
    Player.append(row.find('a').text)
    Country.append(row.find('span', class_='table-body__logo-text').text)
    Rating.append(row.find('td', class_='table-body__cell rating').text)
    
# Storing data in Dataframe
ODI_Batmans=pd.DataFrame({'Ranking':Position,'Player_Name':Player, 'Team':Country, 'Rating':Rating})

print('\033[1m'+'ICC ODI MENS BATTING RANKING'+'\033[0m') # Print Title in bold case
ODI_Batmans


# ### iii) Top 10 ODI bowlers along with the records of their team and rating# 

# In[22]:


# ICC ODI Mens Bowling Ranking

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

response = requests.get(url)
print(response.status_code, '--->',url)
print('\n\n')
soup= BeautifulSoup(response.content, 'lxml')
Position =[]
Player =[]
Country =[]
Rating =[]

# Extracting Data of Top Player from Banner
block_1= soup.find('tr', attrs={'class':'rankings-block__banner'}) # contains Top Player ranking detail

Position.append(block_1.find('td',class_='rankings-block__position').text)# Ranking Position
Player.append(block_1.find('div', class_="rankings-block__banner--name-large").text) # Extract Player Name
Country.append(block_1.find('span', class_='rankings-block__banner--nation').text)# Extract Country Name
Rating.append(block_1.find('div', class_="rankings-block__banner--rating").text) # Extract Rating

# Extracting other Player Ranking
table_rows =soup.find_all('tr', attrs={'class':'table-body'})

for row in table_rows[:10]:
    Position.append(row.find('td', class_='table-body__cell table-body__cell--position u-text-right').text.replace('\n',''))
    Player.append(row.find('a').text)
    Country.append(row.find('span', class_='table-body__logo-text').text)
    Rating.append(row.find('td', class_='table-body__cell rating').text)
    
# Storing data in Dataframe
ODI_Bowling=pd.DataFrame({'Ranking':Position,'Player_Name':Player, 'Team':Country, 'Rating':Rating})

print('\033[1m'+'ICC ODI MENS BOWLING RANKING'+'\033[0m') # Print Title in bold case
ODI_Bowling


# Write a python program to scrape cricket rankings from ‘www.icc-cricket.com’. You have toscrape:
# i) Top 10 ODI teams in women’s cricket along with the records for matches, points and rating.
# 
# ii) Top 10 women’s ODI players along with the records of their team and rating.
# 
# iii) Top 10 women’s ODI all-rounder along with the records of their team and rating.
# 
# i) Top 10 ODI teams in women’s cricket along with the records for matches, points and rating.# 

# # i) Top 10 ODI teams in women’s cricket along with the records for matches, points and rating# 

# In[23]:


from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests

url = 'https://www.icc-cricket.com/rankings/womens/team-rankings/odi'

response = requests.get(url)
print(response.status_code, '--->',url)
print('\n')
SOUP= BeautifulSoup(response.content, 'lxml')

# Creating empty list
Team=[]
Matches=[]
Points=[]
Rating=[]

# Extracting Team Name
Country = SOUP.find_all('span',class_="u-hide-phablet")
for i in Country:
    Team.append(i.get_text().replace("\n",""))
    Team=Team[0:10]
    
# Extracting No of Matches    
match=SOUP.find_all('td',class_='rankings-block__banner--matches')
matchs=SOUP.find_all('td',class_='table-body__cell u-center-text')
mtc = match + matchs
for i in  mtc:
    Matches.append(i.text)
    Matches=Matches[0:10]
    
# Extracting Points gain    
pt=SOUP.find_all('td',class_="rankings-block__banner--points")
pts= SOUP.find_all('td',class_ ="table-body__cell u-center-text")
Point= pt + pts
for i in Point:
    Points.append(i.get_text().replace("\n",""))
    Points=Points[0:10]
    
# Extracting Rating
rat=SOUP.find_all('td',class_="rankings-block__banner--rating")

rating = SOUP.find_all('td',class_="table-body__cell u-text-right rating")
RATING=rat + rating
for i in RATING:
    Rating.append(i.get_text().replace("\n",""))
    Rating=Rating[0:10]
Rating

# Creating dataframe to store data
ODI=pd.DataFrame({})
ODI['Country']=Team
ODI['Matches']=Matches
ODI['Rating']=Rating
ODI['Points']=Points

print('\033[1m'+'ICC ODI WOMENS RANKING'+'\033[0m') # Print Title in bold case
ODI


# # ii) Top 10 women’s ODI players along with the records of their team and rating.

# In[24]:


# ICC WOMENS Bating Ranking

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'https://www.icc-cricket.com/rankings/womens/player-rankings/odi/batting'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

response = requests.get(url)
print(response.status_code, '--->',url)
print('\n\n')
soup= BeautifulSoup(response.text, 'lxml')
Position =[]
Player =[]
Country =[]
Rating =[]

# Extracting Data of Top Player from Banner
block_1= soup.find('tr', attrs={'class':'rankings-block__banner'}) # contains Top Player ranking detail

Position.append(block_1.find('td',class_='rankings-block__position').text)# Ranking Position
Player.append(block_1.find('div', class_="rankings-block__banner--name-large").text) # Extract Player Name
Country.append(block_1.find('span', class_='rankings-block__banner--nation').text)# Extract Country Name
Rating.append(block_1.find('div', class_="rankings-block__banner--rating").text) # Extract Rating

# Extracting other Player Ranking
table_rows =soup.find_all('tr', attrs={'class':'table-body'})

for row in table_rows[:10]:
    Position.append(row.find('td', class_='table-body__cell table-body__cell--position u-text-right').text.replace('\n',''))
    Player.append(row.find('a').text)
    Country.append(row.find('span', class_='table-body__logo-text').text)
    Rating.append(row.find('td', class_='table-body__cell rating').text)
    
# Storing data in Dataframe
ODI_Batmans=pd.DataFrame({'Ranking':Position,'Player_Name':Player, 'Team':Country, 'Rating':Rating})

print('\033[1m'+'ICC ODI WOMENS BATTING RANKING'+'\033[0m') # Print Title in bold case
ODI_Batmans


# # iii) Top 10 women’s ODI all-rounder along with the records of their team and rating.

# In[25]:


# ICC ODI Womens Bowling Ranking

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'https://www.icc-cricket.com/rankings/womens/player-rankings/odi/bowling'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

response = requests.get(url)
print(response.status_code, '--->',url)
print('\n\n')
soup= BeautifulSoup(response.text, 'html.parser')
Position =[]
Player =[]
Country =[]
Rating =[]

# Extracting Data of Top Player from Banner
block_1= soup.find('tr', attrs={'class':'rankings-block__banner'}) # contains Top Player ranking detail

Position.append(block_1.find('td',class_='rankings-block__position').text)# Ranking Position
Player.append(block_1.find('div', class_="rankings-block__banner--name-large").text) # Extract Player Name
Country.append(block_1.find('span', class_='rankings-block__banner--nation').text)# Extract Country Name
Rating.append(block_1.find('div', class_="rankings-block__banner--rating").text) # Extract Rating

# Extracting other Player Ranking
table_rows =soup.find_all('tr', attrs={'class':'table-body'})

for row in table_rows[:10]:
    Position.append(row.find('td', class_='table-body__cell table-body__cell--position u-text-right').text.replace('\n',''))
    Player.append(row.find('a').text)
    Country.append(row.find('span', class_='table-body__logo-text').text)
    Rating.append(row.find('td', class_='table-body__cell rating').text)
    
# Storing data in Dataframe
ODI_Bowling=pd.DataFrame({'Ranking':Position,'Player_Name':Player, 'Team':Country, 'Rating':Rating})

print('\033[1m'+'ICC ODI WOMENS BOWLING RANKING'+'\033[0m') # Print Title in bold case
ODI_Bowling


# # Write a python program to scrape mentioned news details from https://www.cnbc.com/world/?region=world :
# i) Headline
# ii) Time
# iii) News Link

# In[26]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as soup
import requests


# In[2]:


from datetime import date
today = date.today()

d = today.strftime("%m-%d-%y")
print("date =", d)


# In[3]:


cnn_url="https://edition.cnn.com/world/live-news/coronavirus-pandemic-{}-intl/index.html".format(d)
cnn_url


# In[4]:


html = requests.get(cnn_url)


# In[5]:


bsobj = soup(html.content,'lxml')
bsobj


# In[6]:


for link in bsobj.findAll("h2"):
    
    print("Headline : {}".format(link.text))


# In[7]:


for news in bsobj.findAll('article',{'class':'sc-jqCOkK sc-kfGgVZ hQCVkd'}):
    print(news.text.strip())


# In[8]:


nbc_url='https://www.nbcnews.com/health/coronavirus'


# In[9]:


r = requests.get('https://www.nbcnews.com/health/coronavirus')


# In[10]:


b = soup(r.content,'lxml')


# In[11]:


for news in b.findAll('h2'):
    print(news.text)


# In[12]:


links = []
for news in b.findAll('h2',{'class':'teaseCard__headline'}):
    links.append(news.a['href'])
    
links


# In[13]:


for link in links:
    page = requests.get(link)
    bsobj = soup(page.content)
    for news in bsobj.findAll('div',{'class':'article-body__section article-body__last-section'}):
        print(news.text.strip())


# Write a python program to scrape the details of most downloaded articles from AI in last 90 days.# 

# In[29]:


import requests
from bs4  import BeautifulSoup
res = requests.get('https://hackevents.co/hackathons')
bs = BeautifulSoup(res.text, 'lxml')
hacks_data = bs.find_all('div',{'class':'hackathon '})
for i,f in enumerate(hacks_data,1):
    hacks_month = f.find('div',{'class':'date'}).find('div',{'class':'date-month'}).text.strip()
    hacks_date = f.find('div',{'class':'date'}).find('div',{'class':'date-day-number'}).text.strip()
    hacks_days = f.find('div',{'class':'date'}).find('div',{'class':'date-week-days'}).text.strip()
    hacks_final_date = "{} {}, {} ".format(hacks_date, hacks_month, hacks_days )
    hacks_name = f.find('div',{'class':'info'}).find('h2').text.strip()
    hacks_city = f.find('div',{'class':'info'}).find('p').find('span',{'class':'city'}).text.strip()
    hacks_country = f.find('div',{'class':'info'}).find('p').find('span',{'class':'country'}).text.strip()
    print("{:<5}{:<15}: {:<90}: {}, {}\n ".format(str(i)+')',hacks_final_date, hacks_name.title(), hacks_city, hacks_country))


# In[31]:


from bs4 import BeautifulSoup 
base_url = 'https://www.journals.elsevier.com/artificial-intelligence/most-downloaded-articles'
# Add 1 because Python range.
url_list = ["{}{}".format(base_url, str(page)) for page in range(1, 408)]
s=[]
for url in url_list:
    print (url)
    s.append(url)


# # Write a python program to scrape mentioned details from dineout.co.in :

# In[33]:


get_ipython().system('pip install bs4')
get_ipython().system('pip install requests')


# In[34]:


from bs4 import BeautifulSoup
import requests


# In[37]:


page = requests.get('https://www.dineout.co.in/delhi-restaurants/buffet-special')


# In[38]:


page


# In[39]:


soup = BeautifulSoup(page.content)
soup


# In[40]:


first_title = soup.find('a',class_="restnt-name ellipsis")
first_title


# In[41]:


first_title.text


# In[42]:


loc = soup.find('div',class_="restnt-loc ellipsis")
loc.text


# In[43]:


sta = soup.find('span',class_="double-line-ellipsis")
sta.text


# In[46]:


titles = []
for i in soup.find_all('a',class_="restnt-name ellipsis"):
    titles.append(i.text)
    
titles    


# In[47]:


location = []
for i in soup.find_all('div',class_="restnt-loc ellipsis"):
    location.append(i.text)
    
location


# In[48]:


images = []
for i in soup.find_all('img',class_="no-img"):
    images.append(i.get('data-src'))
    
images


# In[51]:


print(len(titles),len(location),len(images))


# # Write a python program to scrape the details of top publications from Google Scholar from# Write a python program to scrape the details of top publications from Google Scholar from

# In[ ]:


from ..search import Search
from .settings import GOOGLE_URLS

from bs4 import BeautifulSoup
from urllib.parse import unquote
import re

class GScholar(Search):
	'''
	GScholar is a class to get result from Google Scholar Search.
	Search --> Inherited.
	'''

	URL = GOOGLE_URLS['GOOGLE_SCHOLAR']
	LABELS = ['year', 'title', 'description', 'authors', 'link', 
			  'pdf_link', 'journal_domain', 'domain', 'many_version']

	def __init__(self, search_word, start_page=1, max_page=1):
		super().__init__(search_word, start_page, max_page)
		self.start_page_num = (start_page-1) * 10
		self.max_page_num = (max_page-1) * 10
		self.pages = self.get_result(GScholar.URL, self.start_page_num, self.max_page_num)

		self.years = []
		self.titles = []
		self.descs = []
		self.authors = []
		self.links = []
		self.pdf_links = []
		self.journal_domains = []
		self.domains = []
		self.many_versions = []


	def get_main(self, tag, attr, findAll=False):
		'''
		Return: result -> list, the value is BS4 object. This function 
				is used by all another function inside this class.
		Parameter:
		tag -> string, html tag to gather.
		attr -> string, attribute from a tag. 
		[findAll] !optional -> boolean, the result will be 2D list instead of 1D, 
							   because BS4 will search all tag and attr 
							   that meet the criteria, not the first match.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_main('h3', {'class': 'gs_rt'})) # you get title
		'''

		res = []
		for page_num in self.pages:
			page = self.pages[page_num]
			soup = BeautifulSoup(page, 'html.parser')
			texts_parse = soup.findAll('div', {'class': 'gs_r gs_or gs_scl'})

			for t in texts_parse:
				get_attr = t.findAll(tag, attr) if findAll else t.find(tag, attr)

				if get_attr:
					res.append(get_attr)
				else:
					res.append(None)

		return res


	def get_year(self):
		'''
		Return: year -> list, year of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_year())
		'''

		if self.years:
			return self.years

		dates_tmp = self.get_main('div', {'class': 'gs_a'})
		for d in dates_tmp:
			d = d.text
			pattern = r"\d{4}"
			found_year = re.search(pattern, str(d))
			if found_year:
				self.years.append(found_year.group(0))
			else:
				self.years.append(None)

		return self.years


	def get_title(self):
		'''
		Return: title -> list, title of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_title())
		'''

		if self.titles:
			return self.titles

		res = [res.text for res in self.get_main('h3', {'class': 'gs_rt'})]
		self.titles.extend(res)
		return self.titles


	def get_desc(self):
		'''
		Return: description -> list, description of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_desc())
		'''

		if self.descs:
			return self.descs

		res = [res.text for res in self.get_main('div', {'class': 'gs_rs'})]
		self.descs.extend(res)
		return self.descs


	def get_author(self):
		'''
		Return: author -> list, author of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_author())
		'''

		if self.authors:
			return self.authors

		split_sym = '-'
		dates_tmp = self.get_main('div', {'class': 'gs_a'})
		for d in dates_tmp:
			d = d.text
			if split_sym in d:
				id_split_sym = d.index(split_sym)
				self.authors.append(d[:id_split_sym-1])
			else:
				self.authors.append(None)

		return self.authors


	def get_link(self):
		'''
		Return: link -> list, link of result.
		Example:
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_link())
		'''

		if self.links:
			return self.links

		res = [unquote(res.find('a')['href']) for res in self.get_main('h3', {'class': 'gs_rt'})]
		self.links.extend(res)

		return self.links


	def get_pdflink(self):
		'''
		Return: pdflink -> list, if the result have pdf, then the 
						   element must not be None.
		Example: 
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_pdflink())
		'''

		if self.pdf_links:
			return self.pdf_links

		self.pdf_links = [unquote(res.find('a')['href'])
						 if res 
						 else None 
						 for res in self.get_main('div', {'class': 'gs_or_ggsm'})]

		return self.pdf_links


	def get_journal_domain(self):
		'''
		Return: journal_domain -> list, domain or subdomain that used 
								  for online publication.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_journal_domain())
		'''

		if self.journal_domains:
			return self.journal_domains

		split_sym = '-'
		journal_dom_tmp = self.get_main('div', {'class': 'gs_a'})
		for j in journal_dom_tmp:
			j = j.text
			pattern = r"([a-z0-9][a-z0-9\-]{0,61}[a-z0-9]\.)+[a-z0-9][a-z0-9\-]*[a-z0-9]"
			found_domain = re.search(pattern, str(j))
			if found_domain:
				self.journal_domains.append(found_domain.group(0))
			else:
				self.journal_domains.append(None)

		return self.journal_domains


	def get_domain(self):
		'''
		Return: domain -> list, domain or subdomain that extracted from link.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_domain())
		'''

		if self.domains:
			return self.domains

		subdomains = self.get_journal_domain()
		for s in subdomains:
			found_domain = re.search(r"(\w{2,}\.\w{2,3}\.\w{2,3}|\w{2,}\.\w{2,3})$", str(s))
			if found_domain:
				self.domains.append(found_domain.group(1))
			else:
				self.domains.append(None)

		return self.domains


	def get_many_version(self):
		'''
		Return: many of version -> list, available version of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_many_version())
		'''

		if self.many_versions:
			return self.many_versions

		self.many_versions = [res[-1].text
							  if res 
							  else None 
							  for res in self.get_main('a', {'class': 'gs_nph'}, findAll=True)]

		return self.many_versions


	def get_all(self):
		'''
		Return: all attributes of result -> dict.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_all())
		'''

		years = self.get_year()
		titles = self.get_title()
		descs = self.get_desc()
		authors = self.get_author()
		links = self.get_link()
		pdf_links = self.get_pdflink()
		journal_domains = self.get_journal_domain()
		domains = self.get_domain()
		many_versions = self.get_many_version()

		return self.to_dict(GScholar.LABELS, years, titles, descs, authors, 
							links, pdf_links, journal_domains, domains, many_versions)


# In[ ]:




