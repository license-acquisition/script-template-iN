#######################
# json to normalized
#
#######################

import codecs, json, re


with open('html2json.txt', 'r') as f:
    json_data = json.load(f)

output = []
for i in range(len(json_data)):
    info = {}
    count = 1.0
    for data in json_data[str(i)]:
        # transform if phone number
        if re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', data):
             phone = re.search('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', data).group()
             phone = phone.replace('(','').replace(')','')
             if len(phone) > 8:
                 if count > 7.0:
                     info[count] = {'header': 'fax', 'data': phone}
                 else:
                     info[count] = {'header': 'phone', 'data': phone}
        elif len(data) == 2:
            info[count] = {'header': 'state', 'data': data}
        elif 'OKFIRM' in data:
            info[count] = {'header': 'license_number', 'data': data}
        else:
            info[count] = {'header': 'NA', 'data': data}
        count +=1
    output.append(info)
        
f = codecs.open('json2norm.txt', 'w')
json.dump(output, f)
f.close()
