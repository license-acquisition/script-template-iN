import codecs, re, requests, csv, time
from bs4 import BeautifulSoup
from datetime import date
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('arc-eng_c_NEbea_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
f.write("entity_name,license_number,licensee_type_cd,qualifying_individual,qualifying_individual2,primary_specialty,status,city,county,state,country,first_issue_date,expiration_date,company_flag,number_type\n")

for i in range(0, 5000):
        try:
                url = "http://www.ea.nebraska.gov/search/search.php?page=details&lic=CA%04d" %i
                
                page = requests.get(url)
                soup = BeautifulSoup(page.content)

                data = []
                data.append(soup.find_all("p", {"class" : "center"})[0].find("span", {"class" : "bold"}).text)
                for span in soup.find_all("span", {"class" : "bold"}):
                        span.decompose()
                for p in soup.find_all("p", {"class" : "label"}):
                        data.append(p.text)

#fix 1st parsing issue             
                if len(data)==12:

                        data.insert(4," ")

                data.append("1")
                data.append("license number")


                        

                f.write('\"' + "\",\"".join(data) + "\"\n")
                print('\"' + "\",\"".join(data) + "\"\n")
        
        except Exception as e:
                print str(e)

f.close()
