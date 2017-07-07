import requests
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re 

def download_file(url, destination_dir):
	file_name = url.split('/')[-1].strip()
	u = urllib2.urlopen(url)
	f = open(destination_dir + file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s%s Bytes: %s" % (destination_dir, file_name, file_size)

	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()

def main():
	destination_dir = "./test/"
	initial_link = "https://templates.office.com/en-us/Timelines"

	page = urllib2.urlopen(initial_link)
	soup = BeautifulSoup(page)
	main_links = []
	dl_links = []

	# grab all the main links from the initial website
	productDivs = soup.findAll('ul', attrs={'id' : 'catNav'})
	for div in productDivs:
	    the_link = div.findAll('a')
	    for link in the_link:
	    	main_links.append(re.findall('href="([^"]*)"', str(link))[0])


	# go through each main link make a list of links within
	for m_link in main_links:
		try:
			links = []
			page = urllib2.urlopen(m_link)
			soup = BeautifulSoup(page)
			all_links = soup.findAll("a")
			for link in all_links:
				if link.get("tabindex") == "-1":
					href = link.get("href")
					links.append(href)

			# get the download link from the next page
			for page_link in links:
				new_page = urllib2.urlopen(page_link)
				new_soup = BeautifulSoup(new_page)

				new_links = new_soup.findAll("a")
				for link in new_links:
					id_class = link.get("ms.ea_action")
					if id_class == "DownloadWin32":
						new_link=link.get("href")
						download_file(new_link, destination_dir)

		except Exception, e:
			print e


if __name__ == "__main__":
    main()
