#######################
# json to normalized
#
#######################

import codecs, json, re

with open('html2json.txt', 'r') as f:
    info = json.load(f)

json_data = {}
for i in range(len(info)):
    for data in info[str(i)]:
        # transform if phone number
        if re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', data):
             phone = re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', data).group()
             phone = phone.replace('(','').replace(')','')
             json_data[phone] = {'header': 'phone', 'row': i}

for i in json_data.keys():
	print i
	print 'Header type: ' + json_data[i]['header']
	print 'Row number: ' + str(json_data[i]['row'])
