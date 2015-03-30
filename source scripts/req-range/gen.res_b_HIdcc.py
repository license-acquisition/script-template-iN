import requests, codecs, time
from bs4 import BeautifulSoup
#<<<<<<< HEAD:Trigger/Source Scripts/HI/gen.res_b_HIdcc.py

#=======
#>>>>>>> ea8ddcced279b00725b0af98257566a05f755d5f:Trigger/Source Scripts/HI/HIdcc.py
from script_template import create_file, logger

f = create_file('gen.res_b_HIdcc', 'w', ['21', '38', '37', '13', 'Legal License Name', 'Trade/Professional Name', 'Entity', '19', 'Class Prefix', 'Special Privilege', 'Restriction', 'Education Code', 'Business Code', 'Conditions & Limitations', 'Business Address'])
l = logger('gen.res_b_HIdcc')
s = requests.Session()

def main():
    licenseTypes = ['PJ', 'EJ', 'EM', 'CT', 'PCFR']
    s.get('https://pvl.ehawaii.gov/pvlsearch/')
    for lic in licenseTypes:
            i = 25000 # original i = 1
            while i <= 35000:
                    info = []
                    page = s.get("https://pvl.ehawaii.gov/pvlsearch/info/%s-%s-0"%(lic, str(i)))
                    l.info('searching %s-%s' %(lic, str(i)))
                    time.sleep(1)
                    try:
                            soup = BeautifulSoup(page.content)
                            for span in soup.findAll("span"):
                                    span.extract()
                            for td in soup.findAll("td"):
                                    info.append(td.text.replace("&amp;", "&"))
                            i += 1
                            if len(info)>7:
                                    f.write("|".join(info) + "\n")
                                    l.info(info)
                            else:
                                    pass
                    except Exception, e:
                            l.error(str(e))
                            i += 1
                            l.error(i)

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()