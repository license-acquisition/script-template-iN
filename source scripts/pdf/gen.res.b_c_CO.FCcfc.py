############################
# Output: feed_name.txt
# Method: PDF
############################

# Import modules #########################################

import codecs, re, requests, time
from subprocess import call # allows for doing terminal commands

       
# Write file and headers #################################

f = codecs.open('gen.res.b_c_CO.FCcfc_%s_000.csv' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

headers = ['entity_name', 'license_number', 'principal_owner','address1','phone','expiration_date', 'email','city','state','zip','license_type_cd','company_flag','city_flag']

f.write('|'.join(headers) + '\n') # all write code should include a new-line ('\n') character at end


# Set up logging ########################################
def log(status):
    
    feed = 'gen.res.b_c_CO.FCcfc_%s_000.txt' %(time.strftime('%Y%m%d'))  # date in output

    l = codecs.open('log.csv', 'a')
    
    l.write(','.join([feed, str(time.strftime('%Y/%m/%d')), str(time.time()), status]) + '\n')


# Save pdf and call pdftotext on it #####################
# Make sure it's 'wb' (write binary) ####################

open('authority.pdf', 'wb').write(requests.get('http://citydocs.fcgov.com/?cmd=convert&vid=2&docid=2438983&dt=MONTHLY+REPORT').content)

# -layout preserves layout, -table lets it know the pdf is in table format
call(['pdftotext', '-layout', '-table', 'authority.pdf'])


#########################################################
# PDFs are super messy. Read them line by line and look for
# a common line that ends the info array
##########################################################

def main():
    # iterate through lines #####################################

    
    temp_name = ""
    info = []
 

    for line in codecs.open("authority.txt", "r").readlines():
    
      nline = re.sub("   *","_%_", line)
            
      nline = re.sub("\n","", nline)
            
      nline = nline.split("_%_")
      
      nline = [x for x in nline if len(x) != 0]
  ########entity_name
      if 1 <= len(nline) <= 4: 
        temp_name = nline[0] +" " 
        #license_number = nline[1]
        digits = re.match("\d\d\d*",  temp_name) 
        if digits:
          temp_name = ""
        elif "Email Address:" in temp_name:
          temp_name = ""
        elif "Number" in temp_name:
          temp_name = ""
        elif "\x0c" in temp_name:
          temp_name = ""
        elif "@" in temp_name:
          temp_name = ""
        elif "Sub Contractor Roster" in temp_name:
          temp_name =""

      elif len(nline) >= 5:
        partial_name = nline[0]
        if "Email Address:" in partial_name:
          partial_name = ""
        elif "Company Name" in partial_name:
          partial_name = ""
        else:
          info = []
          entity_name = temp_name + partial_name
          temp_name =""
          info.append(entity_name)

      if len(nline) == 6: 
   
        license_number = nline[1]
 
        principal_owner = nline[2]
        address1 = nline[3]
        phone = nline[4]
        expiration_date = nline[5]
   
        info.append(license_number)
        info.append(principal_owner)
        info.append(address1)
        info.append(phone)
        info.append(expiration_date)
        
      elif len(nline) == 3:
        email_address = nline[0]
        city = nline[1][:-4]
        state = nline[1][-2:]
        zip_code == nline[2]
        info.append(email_address)
        info.append(city)
        info.append(state)
        info.append(zip_code)
        info.append("Sub Contractor")
        info.append("1")
        info.append("1")
        print '|'.join(info) + '\n'
        f.write('|'.join(info) + '\n')

      elif len(nline) == 4:
        email_address = nline[1]
        city=nline[2][:-4]
        state=nline[2][-2:]
        zip_code=nline[3]
        info.append(email_address)
        info.append(city)
        info.append(state)
        info.append(zip_code)
        info.append("Sub Contractor")
        info.append("1")
        info.append("1")
        print '|'.join(info) + '\n'
        f.write('|'.join(info) + '\n')

      elif len(nline) == 5:
        email_address = nline[1]
        city=nline[2]
        state=nline[3]
        zip_code=nline[4]
        info.append(email_address)
        info.append(city)
        info.append(state)
        info.append(zip_code)
        info.append("Sub Contractor")
        info.append("1")
        info.append("1")
        print '|'.join(info) + '\n'
        f.write('|'.join(info) + '\n')  
                
if __name__ == '__main__':

    log('START')

    try:
        
        main()

        log('COMPLETE')

    except: log('ERROR')
    
    finally: f.close()
