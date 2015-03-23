import codecs, re, requests, csv, time, sys, string
from bs4 import BeautifulSoup
from datetime import date
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('eng_c_NYsed_%s%s%s_000.csv' '''%(str(year), str(month).zfill(2), str(day).zfill(2))''', 'a', 'utf-8')
f.write("licensee_type_cd, number_type, company_flag, address1, address2, city, state, zip, entity_type, PSC #/Company ID#, Initial Filing Date, close date/current through, status, license_number, expiration_date, Officers/Directors/Shareholders\n")
largeGap = 5000
gap = 0
i=0
while True:
        try:
                i+=1
                gap+=1
                if gap > largeGap*2 and i > 110000:
                        break
                print i
                url = "http://www.nysed.gov/coms/op001/opscr9?profcd=16&pscno=%06d" %i
                page = requests.get(url)
                try:
                        new = re.search("Street Address(.*?)Business", page.content.replace("\n", "")).group().replace("<BR>", "_")
                        soup = BeautifulSoup(re.sub("Street Address.*?Business", new, page.content.replace("\n", "")))
                except:
                        soup = BeautifulSoup(page.content)
                pageText = soup.find("div", {"id" : "content_column"}).text.replace('\n', " ")
                pageText = re.sub("\s\s*", " ", pageText)
                if "no matching record for profession was found" in pageText:
                        print "No Results for %s"%i
                else:
                        #print pageText
                        data = []
                        data.append("Engineering Firm")
                        data.append("Certificate of Authorization")
                        try:
                                try:
                                        data.append(re.search("Name :(.*?) Street", pageText).group(1))
                                        data.append(re.search("Street Address :(.*?)Business", pageText).group(1))
                                        data.append(re.search("Business Entity :(.*?) Company ID#", pageText).group(1))
                                        data.append(re.search("Company ID# :(.*?) Initial", pageText).group(1))
                                        data.append(re.search("Initial Filing Date :(.*?) Status", pageText).group(1))
                                        data.append(re.search("Status :(.*?) Certificate", pageText).group(1))
                                        data.append(re.search("Certificate of (.*?) Members/Managers", pageText).group(1))
                                        data.append(re.search("Members/Managers : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))
                                except:
                                        data.append(re.search("Status :(.*?) Members/Managers", pageText).group(1))
                                        data.append(re.search("Members/Managers : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))      
                        except:
                                try:
                                        try:
                                                data.append(re.search("Business Entity :(.*?) PSC #", pageText).group(1))
                                                data.append(re.search("PSC # :(.*?) Initial", pageText).group(1))
                                                data.append(re.search("Initial Filing Date :(.*?) Current", pageText).group(1))
                                                data.append(re.search("Current through :(.*?) Certificate", pageText).group(1))
                                                data.append(re.search("Certificate of (.*?) Officers", pageText).group(1))
                                                data.append(re.search("Officers, Directors, Shareholders : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))
                                        except:
                                                data.append(re.search("Current through :(.*?) Officers", pageText).group(1))
                                                data.append(re.search("Officers, Directors, Shareholders : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))     
                                except:
                                        try:
                                                data.append(re.search("Initial Filing Date :(.*?) Close", pageText).group(1))
                                                data.append(re.search("Close Date:(.*?) Members/Managers", pageText).group(1))
                                                data.append(re.search("Members/Managers(.*?) Use", pageText).group(1))
                                        except:
                                                data.append(re.search("Close Date:(.*?) Officers", pageText).group(1))
                                                data.append(re.search("Officers, Directors, Shareholders : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))
                        data[3] = data[3].strip("_ ")
                        data[3] = "\",\"".join(data[3].split("_", 1))   
                        data[3] = "\",\"".join(data[3].rsplit(" ", 1))
                        data[3] = "\",\"".join(data[3].rsplit(", ", 1))

                        data[8] = "\",\"".join(data[8].rsplit("EXPIRES ", 1))
                        data[8] = "\",\"".join(data[8].rsplit("CERT# ", 1))
                        data = "\",\"".join(data).split("\",\"")
                        if "_" in data[4]:
                                data[4] = "\",\"".join(data[4].split("_", 1))
                        else:
                                data.insert(4, " ")
                        data = "\",\"".join(data).split("\",\"")
                        if "NO" in data[12] or "*" in data[12]:
                                data.insert(13, " ")
                                data.insert(13, " ")
                        f.write(filter(lambda x: x in string.printable, "\"" + "\"|\"".join(data) + "\"\n"))
                        print('\"' + "\"|\"".join(data) + "\"\n")
                if gap > largeGap:
                        largeGap = gap
                gap = 0
        except Exception as e:
                print str(e)
print time.time()-start
