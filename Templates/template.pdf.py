import requests, re
from subprocess import call # allows for doing terminal commands
from script_template import create_file, logger
       
# Write file and headers #################################
f = create_file('pro-type_entity-type_authority','w',[header_num, header_num,...])

# import logger
l = logger('authority')

#########################################################
# PDFs are super messy. Read them line by line and look for
# a common line that ends the info array
##########################################################

def main():
	open('authority.pdf', 'wb').write(requests.get('webpage with pdf').content)

	# -layout preserves layout, -table lets it know the pdf is in table format
	call(['pdftotext', '-layout', '-table', 'authority.pdf'])
    # iterate through lines #####################################
    for line in codecs.open("authority.txt", "r").readlines():
        if "Address" not in line:
            nline = re.sub("   *", "_%_", line)              
            nline = re.sub("\n", "", nline)    
            nline = nline.split("_%_")
            if len(nline) > 4:
                f.write('|'.join(nline)+'\n')

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
    	l.critical(str(e))
    finally:
    	f.close()
