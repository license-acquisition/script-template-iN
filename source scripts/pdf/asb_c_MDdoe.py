#*****************************************************************************************
# Web Scrape of Maryland Asbestos Contractor Companies
# PDF Download Link: http://mde.maryland.gov/programs/Air/Asbestos/AsbestosandIndustrialHygieneHome/Pages/programs/airprograms/asbestos/home/index.aspx

# 08/12/2014
# Anthony Nault
#*****************************************************************************************


import re, codecs, time, requests
from subprocess import call
from script_template import create_file, logger

f = create_file('asb_c_MDdoe', 'w', ['12', '0', '4', '36', '44', '33', 'Contact', '21', 'Small Jobs', '6', '102', '5', '9'])
l = logger('asb_c_MDdoe')

def main():
	open("asb_c_MDdoe.pdf", "wb").write(requests.get("http://mde.maryland.gov/programs/Air/Asbestos/AsbestosNewslettersandBrochures/Documents/Asbestos_Contractor_List_Jan_2015.pdf").content)
	call(["pdftotext", "-layout", "asb_c_MDdoe.pdf"])

	rows = [] # Store modified data.
	column1 = [] # Store all column1 data.
	column2 = [] # Store all column2 data.
	info = [] # Store parsed record from column1.

	# Put a delimiter between the two columns of data
	for line in open('asb_c_MDdoe.txt', 'r'):
		if "ATTN:" not in line:
			# Remove label data
			r = re.sub('[\w\.]*( [\w\.]*)?:', "  ", line.strip())
		else:
			r = line.strip()	
		r = re.sub('  ', '|', r)	
		# Skip over header at the top of each page.
		if "Last Revised" not in line and "MARYLAND DEPARTMENT" not in line and "1800 Washington" not in line and "http:// www.mde.state.md.us" not in line and "LICENSED CONTRACTORS" not in line and "contact this Administration" not in line and "effect the contractor's" not in line:
			rows.append(r)

	# Split the two columns on data.		
	for data in rows:
		row = filter(None, data.split('|'))
		if len(row) == 2 and (row[1] == "No" or row[1] == "Yes"):
			column1.append(row[0])
			column1.append(row[1])		
		elif len(row) == 2:
			column1.append(row[0])
			column2.append(row[1])
		elif len(row) == 4:
			column1.append(row[0])
			column1.append(row[1])
			column2.append(row[2])
			column2.append(row[3])
		elif len(row) == 1:
			column1.append(row[0])

	# Write record from each column to TXT		
	for item in column1:
		info.append(item)
		if info.index(item) == 6:
			info.append("1") # company_flag
			info.append("Approval No.") # number_type
			
			# Parse address
			address = info[2]
			if address[-1] == '-':
				address = address[:-1]
			address = address.split()
			zip = address[-1]
			zip = zip[0:5] # First 5 digets only.
			state = address[-2]
			if len(address) == 3:
				city = address[0]
			else:
				city = ' '.join(address[0:-2])
				
			info[2:3] = city, state, zip
			
			# Write to CSV
			l.info(info)
			f.write("|".join(info) + "\n") 
			l.info('-' * 50)
			info = [] 		
	for item in column2:
		info.append(item)
		if info.index(item) == 6:
			info.append("1") # company_flag
			info.append("Approval No.") # number_type
			
			# Parse address
			address = info[2]
			if address[-1] == '-':
				address = address[:-1]
			address = address.split()
			zip = address[-1]
			zip = zip[0:5] # First 5 digets only.
			state = address[-2]
			if len(address) == 3:
				city = address[0]
			else:
				city = ' '.join(address[0:-2])
				
			info[2:3] = city, state, zip
			
			# Write to CSV
			l.info(info)
			f.write("|".join(info) + "\n")
			l.info('-' * 50)
			info = []


if __name__ == '__main__':
        try:
                main()
                l.info('complete')
                call(['rm', 'asb_c_MDdoe.pdf'])
                call(['rm', 'asb_c_MDdoe.txt'])
        except Exception as e:
                l.critical(str(e))
        finally: 
                f.close()
	
	
