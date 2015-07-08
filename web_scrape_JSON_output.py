import urllib2, re, json
from bs4 import BeautifulSoup

#define url

#url taken out for confidentiality
#url=

#two things that need to be extracted, the link to each company's page, and the 
#links to other 9 pages

#for going to the next pages, since there are only total of 10 pages, simply
#go from page 1 to page 10 will do the job
#can use url+'?page=*' where * goes from 1 to 10


#extracting links
#function for extracting links to all companies' pages
def comp_link_extract(url, link_extract):
	soup=BeautifulSoup(urllib2.urlopen(url).read())
	names=soup.findAll('tbody')
	for name in names:
		links=name.findAll('a')
		for link in links:
			#store a string instead of a list by joining with ''
			link_extract.append(''.join(re.findall('href="(.+?)"', str(link))))		

#function for extracting company info and putting it into JSON format
def comp_detail(url, output):
	#creating place holders
	category_list=[]
	id_list=[]
	info_list=[]
	#scraping the content page
	soup=BeautifulSoup(urllib2.urlopen(url).read())
	#getting the categories and storing in a list
	names=soup.find_all('b', {'id':''})
	for name in names:
		category_list.append(name.text)
	

	#finding all id's for extracting the info
	for con in soup.find_all('td'):

		if con.get('id')!=None:
			id_list.append(con.get('id'))
	
	#extracting the info for each category
	for iD in id_list:
		info_list.append(soup.find('td', {'id':iD}).text)
		
	#matching the two lists and put into a dictionary
	complete_dict=dict(zip(category_list,info_list))

	#formatting into JSON
	Result=json.dump(complete_dict, output, indent=4, sort_keys=True)
	


soup=BeautifulSoup(urllib2.urlopen(url).read())
link_extract=[]		
#extracting company links without changing pages for page 1. Change page from 2 to 10 after that.
trigger=False
for page_num in range(1,11):
	if not trigger:
		trigger=True
		comp_link_extract(url,link_extract)
	else:
		#go to next page, then extract more links
		#set the url to be the next page's url
		#url again taken out
		#url=
		comp_link_extract(url, link_extract)


#extract info from each company and store in JSON format
with open('solution.json', 'wb') as output:
	for i in range(len(link_extract)):
		#getting url
		#replacing ' ' with '%20'
		#url taken out
		#url=some url+link_extract[i]
		url='%20'.join(url.split(' '))
		#feeding into comp_detail for extracting and converting
		comp_detail(url, output)

		




