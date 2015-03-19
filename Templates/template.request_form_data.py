# Import modules #########################################

import requests
from bs4 import BeautifulSoup
from script_template import create_file
       
# Write file and headers #################################

f = create_file('pro-type_entity-type_authority','w',[header_num, header_num,...])
# all write code should include a new-line ('\n') character at end




#########################################################
# Some sites allow post requests which can be written into
# the url via form data.
# Example: www.site.com?key1=value1&key2=value2
##########################################################

def main():
    # Hit the initial page ###################################
    # It's usually the navigation, form-input page ###########

    url = 'initial url to hit'
    soup = BeautifulSoup(requests.get(url).content)
    # Get all elements which will be used in iteration url ###
    # loop through form data inputs ##########################
    for element in soup.find_all('element'):
        iteration_url = 'url with added form data'
        soup = BeautifulSoup(requests.get(iteration_url).content)
        for link in soup.find_all("a"):
                # look for commonalities in link urls
            if 'details/lic_number=' in link['href']:      
                # get the soup where the actual data is!!
                detailed_soup = BeautifulSoup(requests.get(link['href']).content)
                info = [] # list for appending license data
                '''
                parse the page source in any way you need to, then write to file
                '''
                print info
                f.write('|'.join(info) + '\n')

# Main logic #################################################

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print str(e) 
    finally: 
        f.close()
