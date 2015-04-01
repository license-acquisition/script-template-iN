############################
# Output: ele-gen.res-hva-plu-roo_c_CO.THcot
# Method: PDF
############################

# Import modules #########################################

import codecs, re, requests, time
from subprocess import call # allows for doing terminal commands
from script_template import create_file, logger

f = create_file('ele-gen.res-hva-plu-roo_c_CO.THcot', 'w', ['12', '0', '4', '36', '44', '21', '32', '33', '6', '5'])
l = logger('ele-gen.res-hva-plu-roo_c_CO.THcot')

def main():
    # write pdf to file and convert it ######################
    open('ele-gen.res-hva-plu-roo_c_CO.THcot.pdf', 'wb').write(requests.get('http://www.cityofthornton.net/Departments/CityDevelopment/Development/Documents/BUILDING%20INSPECTION/Reports/Licensed_Contractors_2015_CityofThornton/City_of_Thornton_Licensed_Contractors_as_of_3-9-2015.pdf').content)
    call(['pdftotext', '-layout', '-table', 'ele-gen.res-hva-plu-roo_c_CO.THcot.pdf'])

    # iterate through lines #####################################
    for line in codecs.open("ele-gen.res-hva-plu-roo_c_CO.THcot.txt", "r").readlines():
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
                l.info(info)
                f.write('|'.join(info)+'\n')

if __name__ == '__main__':
    try:
        main()
        l.info('COMPLETE')
    except Exception as e: l.critical(str(e))
    finally:
        f.close()
        call(['rm', 'ele-gen.res-hva-plu-roo_c_CO.THcot.pdf'])
        call(['rm', 'ele-gen.res-hva-plu-roo_c_CO.THcot.txt'])
