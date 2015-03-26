from selenium import webdriver
from bs4 import BeautifulSoup
import re, codecs, time
from script_template import create_file, logger

f = create_file('pes_b_UTdaf', 'w', ["Name","License Type","License Number","Customer Number","Mailing Address", "Location Address", "Application Date", "Renewal Printed", "First Certification", "Renewal Date", "License Expires", "When Re-Certified", "License Printed", "Certification Expires", "Late Fee Printed", "Uniform Registry Number", "Applicator Name", "Applicator License", "Expired"])
l = logger('pes_b_UTdaf')
driver = webdriver.PhantomJS()

def main():
        driver.get('http://ag.utah.gov/licenses-registrations.html')
        driver.find_element_by_xpath('//*[@id="main"]/article/ul[2]/li[1]/a').click() # open instance of sql access
        driver.find_element_by_xpath('/html/body/form/table/tbody/tr[54]/td[1]/input').click()

        for i in range(1,2000):
                try:
                        driver.get('http://webapp.ag.utah.gov/LicenseLookup/pageRedirection.jsp?lic_Number=%s&lic_Type=4000&runPage=licDetails.jsp&LicenseType=4000&sortBy=tCustomerAddress.LastName' %i)
                        c = driver.page_source
                        soup = BeautifulSoup(c)
                        type = str(soup.findAll("b")[1]).split(":",1)[1].replace("</b>","").strip()
                        numb = str(soup.findAll("b")[2]).split(":",1)[1].replace("</b>","").strip()
                        name = str(soup.findAll("b")[3]).split(":",1)[1].replace("</b>","").strip()
                        cust = str(soup.findAll("font", {"size":"3"})[2]).split(":",1)[1].replace("</font>","").strip()
                        locationadd = str(soup.findAll("font",{"size":"2"})[1]).split(">",2)[1].replace("</font","").strip()
                        if locationadd == "":
                                locationadd = " "
                        mailadd = str(soup.findAll("font",{"size":"2"})[2]).split(">",2)[1].replace("</font","").strip()
                        if mailadd == "":
                                mailadd = " "
                        info = []
                        # first round of appending
                        for data in [name, type, numb, cust, mailadd.split(',')[0].strip(), mailadd.split(',')[1].strip()]:
                                info.append(data)
                        td = soup.findAll("td",{"align":"left"})
                        date1a = str(td[4])
                        date2a = str(td[5])
                        date3a = str(td[6])
                        date4a = str(td[7])
                        date5a = str(td[8])
                        date6a = str(td[9])
                        date7a = str(td[10])
                        date8a = str(td[11])
                        date9a = str(td[12])
                        date10a = str(td[13])
                        date1 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date1a)
                        if date1 == "":
                                date1 = " "
                        date2 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date2a)
                        if date2 == "":
                                date2 = " "
                        date3 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date3a)
                        if date3 == "":
                                date3 = " "
                        date4 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date4a)
                        date5 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date5a)
                        date6 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date6a)
                        date7 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date7a)
                        date8 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date8a)
                        date9 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date9a)
                        date10 = re.findall("(\d{1,2}[/-]\d{1,2}[/-]\d{1,4})",date10a)
                        for data in [date1, date2, date3, date4, date5, date6, date7, date8, date9, date10]:
                                if len(data) == 0:
                                        info.append('')
                                if len(data) == 1:
                                        info.append(data[0])
                        l.info(info)
                        f.write('|'.join(info) + '\n')
                except:
                        pass

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()