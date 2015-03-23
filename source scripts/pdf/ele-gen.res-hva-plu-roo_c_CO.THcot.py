############################
# Output: feed_name.txt
# Method: PDF
############################

# Import modules #########################################

import codecs, re, requests, time
from subprocess import call # allows for doing terminal commands

       
# Write file and headers #################################

f = codecs.open('ele-gen.res-hva-plu-roo_c_CO.THcot_%s_000.csv' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

headers = ['entity_name', 'address1', 'city', 'state','zip','license_number','licensee_type_cd','phone', 'company_flag','city_flag']

f.write('|'.join(headers) + '\n') # all write code should include a new-line ('\n') character at end


# Set up logging ########################################
def log(status):
    
    feed = 'ele-gen.res-hva-plu-roo_c_CO.THcot_%s_000.txt' %(time.strftime('%Y%m%d'))  # date in output

    l = codecs.open('log.csv', 'a')
    
    l.write(','.join([feed, str(time.strftime('%Y/%m/%d')), str(time.time()), status]) + '\n')


# Save pdf and call pdftotext on it #####################
# Make sure it's 'wb' (write binary) ####################

open('authority.pdf', 'wb').write(requests.get('http://www.cityofthornton.net/Departments/CityDevelopment/Development/Documents/BUILDING%20INSPECTION/Reports/Licensed_Contractors_2015_CityofThornton/City_of_Thornton_Licensed_Contractors_as_of_3-9-2015.pdf').content)

# -layout preserves layout, -table lets it know the pdf is in table format
call(['pdftotext', '-layout', '-table', 'authority.pdf'])


#########################################################
# PDFs are super messy. Read them line by line and look for
# a common line that ends the info array
##########################################################

def main():
    # iterate through lines #####################################
    for line in codecs.open("authority.txt", "r").readlines():
        
        nline = re.sub("   *", "_%_", line)
            
        nline = re.sub("\n", "", nline)
            
        nline = nline.split("_%_")
        info = []
        count = 0
        
        for element in nline[:-1]:
            if count == 2:
                city = element[:-11]
                state = element[-9:-7]
                zip_code = element[-6:-1]
                info.append(city)
                info.append(state)
                info.append(zip_code)
            else:
                info.append(element) 
            count += 1
            
        info.append('1')
        info.append('1')
        if len(info) > 4:
            if info[1]=="Address":
                pass
            else:
                f.write('|'.join(info)+'\n')

if __name__ == '__main__':

    log('START')

    try:
        
        main()

        log('COMPLETE')

    except: log('ERROR')
    
    finally: f.close()
