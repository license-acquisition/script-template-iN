############################
# Output: gen.res.a_c_CO.FCcfc
# Method: PDF
############################

import codecs, re, requests, time
from subprocess import call # allows for doing terminal commands
from script_template import create_file, logger

f = create_file('gen.res.a_c_CO.FCcfc', 'w', ['12', '21', '34', '0', '33', '13', '11', '4', '36', '44', '32', '6', '5'])
l = logger('gen.res.a_c_CO.FCcfc')


def main():
    # iterate through lines #####################################
    open('gen.res.a_c_CO.FCcfc.pdf', 'wb').write(requests.get('http://citydocs.fcgov.com/?cmd=convert&vid=2&docid=2438982&dt=MONTHLY+REPORT').content)
    call(['pdftotext', '-layout', '-table', 'gen.res.a_c_CO.FCcfc.pdf'])

    lines = []
    for line in open("gen.res.a_c_CO.FCcfc.txt", "r"):
        if not any(s in line for s in ['Gen Contractor', 'Company Name', 'Number']):
            nline = re.sub("  ","_%_", line)
            nline = re.sub("\n","", nline)
            nline = nline.split("_%_")
            nline = [x.strip() for x in nline if len(x) != 0]
            for n in nline:
                lines.append(n)
    
    index = [x for x, char in enumerate(lines) if re.match(r'[0-9]{5}', char)]
    
    for i in range(len(index)-1):
        if i==0:
            info = lines[:index[i]+1]      
        else:
            info = lines[index[i-1]+1:index[i]+1]
        info = [x for x in info if 'Email Address' not in x]
        f.write('|'.join(info) + '\n')
        l.info(info)        
                

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
