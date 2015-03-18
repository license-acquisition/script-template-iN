############################
# Output: feed_name.txt
# Method: PDF
############################

# Import modules #########################################

import codecs, re, requests, time
from subprocess import call # allows for doing terminal commands

       
# Write file and headers #################################

f = codecs.open('pro-type_entity-type_authority_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

headers = ['canonical_header1', 'canonical_header2', 'canonical_header3', '...']

f.write('|'.join(headers) + '\n') # all write code should include a new-line ('\n') character at end


# Set up logging ########################################
def log(status):
    
    feed = 'pro-type_entity-type_authority_%s_000.txt' %(time.strftime('%Y%m%d'))  # date in output

    l = codecs.open('log.csv', 'a')
    
    l.write(','.join([feed, str(time.strftime('%Y/%m/%d')), str(time.time()), status]) + '\n')


# Save pdf and call pdftotext on it #####################
# Make sure it's 'wb' (write binary) ####################

open('authority.pdf', 'wb').write(requests.get('webpage with pdf').content)

# -layout preserves layout, -table lets it know the pdf is in table format
call(['pdftotext', '-layout', '-table', 'authority.pdf'])


#########################################################
# PDFs are super messy. Read them line by line and look for
# a common line that ends the info array
##########################################################

def main():
    # iterate through lines #####################################
    for line in codecs.open("authority.txt", "r").readlines():
        if "Address" not in line:
            nline = re.sub("   *", "_%_", line)
                
            nline = re.sub("\n", "", nline)
                
            nline = nline.split("_%_")
                
            if len(nline) > 4:
                    
                f.write('|'.join(nline)+'\n')
		

if __name__ == '__main__':

    log('START')

    try:
        
        main()

        log('COMPLETE')

    except: log('ERROR')
    
    finally: f.close()
