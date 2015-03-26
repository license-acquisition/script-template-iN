import requests, re, codecs, time
from bs4 import BeautifulSoup
from subprocess import call
from script_template import create_file, logger

f = create_file("pes_c_MIdar","w",[8,"categories",6,4,36,33,32])
l = logger("MIdar")

def main():
	page = requests.get("http://www.michigan.gov/mdard/0,4610,7-125-1569_16988_35288-11993--,00.html")
	soup = BeautifulSoup(page.content)
	for link in soup.find_all("a"):
		if "2015 Pesticide Application Business License List by County" in link.text:
			codecs.open('Michigan_Pest_Control.pdf', 'wb').write(requests.get("http://www.michigan.gov/documents/mdard/2015rptWebAlphaByCounty_2-19-15_481814_7.pdf").content)
			break
	#f = codecs.open('Michigan_Pest_Control.pdf', 'wb')	
	#f.write(requests.get(contractor_link).content)

	call(["pdftotext", "-layout", "Michigan_Pest_Control.pdf"])


	for line in open("Michigan_Pest_Control.txt", "r"):
		if "PABL as of" in line:
			date = re.search("PABL as of (.*?) ", line).group(1)
			break
	bad = """1A      Field Crops               4       Seed Treatment                         7D      Vertebrate
		  1B      Vegetable Crops           5       Aquatic                                7E      Interiorscape
		  1C      Fruit Crops               5A      Swimming Pools                         7F      Mosquito
		  1D      Livestock                 5B      Microbial Pest Mgt                     7G      Domestic Animals
		  2       Forestry                  5C      Sewer Line Root Control                8       Public Health (gov)
		  2A      Wood Preservation         6       Right-of-Way                           9       Regulatory (gov)
		  3A      Turfgrass                 7A      General Pest Management                10      Demonstration/Research
		  3B      Ornamental                7B      Wood Destroying Organisms              FUM     Fumigation
	                                                                                   AE      Aerial""".split("\n")

	for line in open("Michigan_Pest_Control.txt", "r"):
		line = re.split("\s\s+", line)
		if len(line)>5 and not any(s in line for s in bad) and line[0].strip() != "":
			line[-1] = line[-1].strip()	
			line.append("Pesticide Application Business")
			l.info("\"" + "\"|\"".join(line).strip() + "\"\n")
			f.write("\"" + "\"|\"".join(line).strip() + "\"\n")


if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		f.close()
