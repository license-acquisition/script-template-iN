import requests, re
from bs4 import BeautifulSoup
import time
import codecs
f = codecs.open("gen.res_c_PAhic_20150223_000.txt","a","utf-8")
l = codecs.open('PAhic_log2.csv','a','utf-8')
#f.write("licensee_type_cd,company_flag,entity_name,dba,license_number,first_issue_date,expiration_date,phone,fax,address1,address2,city,state,zip,website,description\n".replace(',', '|'))
s = requests.session()
headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0"}
from thready import threaded
import logging
import subprocess
logging.basicConfig()

start = time.time()
soup = BeautifulSoup(s.get("http://hicsearch.attorneygeneral.gov/").content)
low = raw_input("Enter start number: ") # 1
high = raw_input("Enter end number: ") # 116000
threads = raw_input("Number of threads: ") # 3 or 4
def PA_hic(numb):
	try:
		soup = BeautifulSoup(s.get("http://hicsearch.attorneygeneral.gov/").content)
		data = {
		"__EVENTTARGET":"btnSearch",
		"__EVENTARGUMENT":"Click",
		"__VIEWSTATE":soup.find("input", id="__VIEWSTATE")['value'],
		"__EVENTVALIDATION":soup.find("input", id="__EVENTVALIDATION")['value'],
		"txtHICNumber":"%d"%numb,
		"hdnSearch":"specific",
		"gvBusiness$CallbackState":"/wEWBB4ERGF0YQUsQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBSEFBY0EeBVN0YXRlBZQBQnhFSEFBSUFCd0FDQVFjQkFnQUhBUUlBQndFQ0FBY0JBZ0FIQWdJQUJ3SUNBQWNDQWdBSEFnSUFCd0lDQUFjQ0FnQUhBZ0lBQndJQ0FBY0NBZ0FIQWdJQUJ3SUNBQWNBQndBSEFBY0FCUUFBQUlBSkFnQUpBZ0FDQUFNSEJBSUFCd0FDQVFjQUJ3QUNBUWNBQndBPQ==",
		"PopUpControlWS":"0:0:-1:-10000:-10000:0:885px:600px:1",
		"pcHelpWS":"0:0:-1:-10000:-10000:0:-10000:-10000:1;0:0:-1:-10000:-10000:0:-10000:-10000:1",
		"DXScript":"1_32,1_61,2_22,2_29,2_15,1_39,1_52,3_7,2_21,1_36,1_54,1_51,2_16,1_44"}
		soup = BeautifulSoup(s.post("http://hicsearch.attorneygeneral.gov/",data=data,headers=headers).content)	
		info = []
		info.append("Home Improvement Contractor")
		info.append('1')
		info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[0].findAll("td")[1].text.strip())
		if "Other Names" in soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[1].findAll("td")[0].text:
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[1].findAll("td")[1].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[2].findAll("td")[1].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[2].findAll("td")[3].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[2].findAll("td")[5].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[3].findAll("td")[1].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[3].findAll("td")[3].text.strip())
			if "Address 2" in soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[5].findAll("td")[0].text.strip():
				info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[4].findAll("td")[1].text.strip())
				info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[5].findAll("td")[1].text.strip())
			else:
				info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[4].findAll("td")[1].text.strip())
				info.append("")
		else:
			info.append("")
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[1].findAll("td")[1].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[1].findAll("td")[3].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[1].findAll("td")[5].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[2].findAll("td")[1].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[2].findAll("td")[3].text.strip())
			if "Address 2" in soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[4].findAll("td")[0].text.strip():
				info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[3].findAll("td")[1].text.strip())
				info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[4].findAll("td")[1].text.strip())
			else:
				info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[3].findAll("td")[1].text.strip())
				info.append("")
		if "Website" in soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-3].findAll("td")[0].text:
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-4].findAll("td")[1].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-4].findAll("td")[3].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-4].findAll("td")[5].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-3].findAll("td")[1].text.strip())
		else:
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-3].findAll("td")[1].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-3].findAll("td")[3].text.strip())
			info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-3].findAll("td")[5].text.strip())
			info.append("")
		info.append(soup.findAll("table",{"class":"templateTable"})[0].findAll("tr")[-2].findAll("td")[1].text.strip())
		desc = info.pop().replace('\n','').replace('\r','')
		info.append(desc)
		print info
		f.write("|".join(info) + "\n")
	except Exception, e:
		print re.sub("s+"," ",soup.text)
		log = []
		log.append(str(numb) + "\n")
		print numb
		l.write("|".join(log) + "\n")
		pass


def ThreadedScrape():
	numb = [int(i) for i in range(int(low), int(high))]
	threaded(numb, PA_hic, num_threads=int(threads))

if __name__ == '__main__':
	ThreadedScrape()
	#f.write('Minutes elapsed: %s \n' %((time.time() - start)/60))
	#f.write('It actually finished.')
	f.close()
