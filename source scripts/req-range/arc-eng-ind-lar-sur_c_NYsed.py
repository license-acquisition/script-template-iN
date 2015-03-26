import codecs, re, requests, csv, time, sys, string
from bs4 import BeautifulSoup
from script_template import create_file, logger

f= create_file('arc-eng-ind-lar-sur_c_NYsed', 'w', ['32', '102', '6', '0', '1', '4', '36', '44', '60', 'PSC #/Company ID#', 'Initial Filing Date', 'close date/current through', '37', '21', '13', 'Officers/Directors/Shareholders'])
l = logger('arc-eng-ind-lar-sur_c_NYsed')

def main():
        i = 1
        license_list = ['03', '16', '14', '04', '15'] # corresponds to arc, eng, ind, lar, sur
        for license_type in license_list:
                while i < 100000:
                        try:
                                url = "http://www.nysed.gov/coms/op001/opscr9?profcd=%s&pscno=%06d" %(license_type, i)
                                i += 1
                                ''' If this works, then do it!
                                soup = BeautifulSoup(requests(url).content)
                                div = soup.find('div', {'id': 'content_column'})
                                data = div.text.split('\n')
                                info = []
                                for dt in data:
                                        if ':' in dt:
                                                info.append(dt.split(':')[1].strip())
                                        else:
                                                pass
                                data = [x.strip() for x in data if x != '']
                                '''

                                page = requests.get(url)
                                try:
                                        new = re.search("Street Address(.*?)Business", page.content.replace("\n", "")).group().replace("<BR>", "_")
                                        soup = BeautifulSoup(re.sub("Street Address.*?Business", new, page.content.replace("\n", "")))
                                except:
                                        soup = BeautifulSoup(page.content)
                                pageText = soup.find("div", {"id" : "content_column"}).text.replace('\n', " ")
                                pageText = re.sub("\s\s*", " ", pageText)
                                if "no matching record for profession was found" in pageText:
                                        l.debug("No Results for %s"%i)
                                else:
                                        info = []
                                        info.append("Engineering Firm")
                                        info.append("Certificate of Authorization")
                                        try:
                                                try:
                                                        info.append(re.search("Name :(.*?) Street", pageText).group(1))
                                                        info.append(re.search("Street Address :(.*?)Business", pageText).group(1))
                                                        info.append(re.search("Business Entity :(.*?) Company ID#", pageText).group(1))
                                                        info.append(re.search("Company ID# :(.*?) Initial", pageText).group(1))
                                                        info.append(re.search("Initial Filing Date :(.*?) Status", pageText).group(1))
                                                        info.append(re.search("Status :(.*?) Certificate", pageText).group(1))
                                                        info.append(re.search("Certificate of (.*?) Members/Managers", pageText).group(1))
                                                        info.append(re.search("Members/Managers : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))
                                                except:
                                                        info.append(re.search("Status :(.*?) Members/Managers", pageText).group(1))
                                                        info.append(re.search("Members/Managers : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))      
                                        except:
                                                try:
                                                        try:
                                                                info.append(re.search("Business Entity :(.*?) PSC #", pageText).group(1))
                                                                info.append(re.search("PSC # :(.*?) Initial", pageText).group(1))
                                                                info.append(re.search("Initial Filing Date :(.*?) Current", pageText).group(1))
                                                                info.append(re.search("Current through :(.*?) Certificate", pageText).group(1))
                                                                info.append(re.search("Certificate of (.*?) Officers", pageText).group(1))
                                                                info.append(re.search("Officers, Directors, Shareholders : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))
                                                        except:
                                                                info.append(re.search("Current through :(.*?) Officers", pageText).group(1))
                                                                info.append(re.search("Officers, Directors, Shareholders : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))     
                                                except:
                                                        try:
                                                                info.append(re.search("Initial Filing Date :(.*?) Close", pageText).group(1))
                                                                info.append(re.search("Close Date:(.*?) Members/Managers", pageText).group(1))
                                                                info.append(re.search("Members/Managers(.*?) Use", pageText).group(1))
                                                        except:
                                                                info.append(re.search("Close Date:(.*?) Officers", pageText).group(1))
                                                                info.append(re.search("Officers, Directors, Shareholders : Click on license number link to the left of professional's name for detailed information.(.*?) Use", pageText).group(1))
                                        info[3] = info[3].strip("_ ")
                                        info[3] = "\",\"".join(info[3].split("_", 1))   
                                        info[3] = "\",\"".join(info[3].rsplit(" ", 1))
                                        info[3] = "\",\"".join(info[3].rsplit(", ", 1))

                                        info[8] = "\",\"".join(info[8].rsplit("EXPIRES ", 1))
                                        info[8] = "\",\"".join(info[8].rsplit("CERT# ", 1))
                                        info = "\",\"".join(info).split("\",\"")
                                        if "_" in info[4]:
                                                info[4] = "\",\"".join(info[4].split("_", 1))
                                        else:
                                                info.insert(4, " ")
                                        info = "\",\"".join(info).split("\",\"")
                                        if "NO" in info[12] or "*" in info[12]:
                                                info.insert(13, " ")
                                                info.insert(13, " ")
                                        f.write(filter(lambda x: x in string.printable, "\"" + "\"|\"".join(info) + "\"\n"))
                                        l.info(info)
                        except Exception as e:
                                l.error(str(e))

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e: l.critical(str(e))
        finally: f.close()