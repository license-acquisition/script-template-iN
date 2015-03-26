import codecs, re, requests, csv, time, sys
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('lan_b_NCsed', 'w', ['headers'])
s = requests.session()

soup = BeautifulSoup(s.get("http://www.nclcrb.org/search-registrants.aspx").content)

def main():
	while True:
		viewState = soup.find("input", id="__VIEWSTATE")['value']
		eventValidation = soup.find("input", id="__EVENTVALIDATION")['value']
		info={"__EVENTTARGET":"ctl00$content$membersGrid", "__EVENTARGUMENT":"Page$Next", "__VIEWSTATE":viewState, "__EVENTVALIDATION":eventValidation, "ctl00$content$ddlFilter":"0"}
		soup = BeautifulSoup(s.post("http://www.nclcrb.org/search-registrants.aspx", info=info).content.replace("<br />", "_"))
		l.info(re.sub("\s\s*", " ", soup.text))
		for tr in soup.find("table", id="ctl00_content_membersGrid").find_all("tr"):
			info = []
			for span in tr.find_all("span"):
				info.append(span.text.replace("_", "\",\""))
			for a in tr.find_all("a"):
				info.append(a.text)
			f.write("\"" + "\",\"".join(info) + "\"\n")

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
                
