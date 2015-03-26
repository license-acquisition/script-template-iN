import codecs
'''
g = codecs.open('headers.txt', 'r').readlines()

headers = {}
for line in g:
	info = line.replace('\n', '').split('\t')
	headers[info[1]] = info[0]
'''
headers = {
	'dba': '10', 'ce_course_number': '54', 'city_flag': '5', 'expiration_date2': '14', 'expiration_date3': '15', 'expiration_date6': '18', 'expiration_date4': '16', 'expiration_date5': '17',
	'surety': '101', 'company_email': '96', 'bond_number': '49', 'company_zip': '99', 'company_city': '95', 'web_site': '43', 'company_flag': '6', 'employer': '65', 'degrees': '61', 'workers_comp': '89',
	'bond_of_qualifying_individual': '50', 'fax': '66', 'address1': '0', 'address2': '1', 'address3': '2', 'address4': '3', 'last_renew_date': '20', 'registration_class': '79', 'license_type3': '23',
	'license_type2': '22', 'license_type5': '25', 'license_type4': '24', 'license_type6': '26', 'bond_amount': '45', 'company_state': '98', 'disciplinary_status': '62', 'fieldaVALUE': '68',
	'qualifying_individual': '35', 'first_issue_date': '19', 'certification1': '57', 'certification2': '58', 'certification3': '59', 'work_comp_expiration': '85', 'state': '36', 'email': '11',
	'limitations': '76', 'company_phone': '97', 'company_address4': '94', 'insurance_company': '72', 'license3': '28', 'license2': '27', 'licensee_type_cd': '32', 'license5': '30', 'license4': '29',
	'status5': '41', 'status4': '40', 'status6': '42', 'status3': '39', 'status2': '38', 'expiration_date': '13', 'employees': '64', 'ce_status': '56', 'bond_expiration': '47', 'work_comp_insurance_company':
	'86', 'entity_name': '12', 'principal_owner': '34', 'fieldaTYPE': '67', 'county': '8', 'work_comp_LI_account_ID': '87', 'insurance_number': '75', 'registration_flag': '100', 'city': '4', 'primary_specialty':
	'78', 'zip': '44', 'license6': '31', 'fieldbTYPE': '69', 'number_type': '102', 'insurance_issue': '74', 'monetary_limit': '77', 'ce_hours': '55', 'phone': '33', 'insurance_amount': '71',
	'workers_compensation_amount': '90', 'ce_course': '52', 'work_comp_effective_date': '83', 'disciplinary_string': '63', 'ce_course_date': '53', 'company_type': '60', 'work_comp_policy_number': '88',
	'work_comp_estimated_workers_reported': '84', 'bond_issue': '48', 'company_name': '7', 'bond_company': '46', 'status': '37', 'bond_type': '51', 'company_address1': '91', 'company_address2': '92',
	'company_address3': '93', 'secondary_specialty': '80', 'insurance_expiration': '73', 'fieldbVALUE': '70', 'ubi': '81', 'work_comp_cancelation': '82', 'license_number': '21', 'county_flag': '9'}

# insert array here
lookup = ["dba,company_name,company_address1,phone,licensee_type_cd,license_number,first_issue_date,expiration_date,status,license_type2,license2,issue_date2,expiration_date2,status2,license_type3,license3,issue_date3,expiration_date3,status3,license_type4,license4,issue_date4,expiration_date4,status4,license_type5,license5,issue_date5,expiration_date5,status5,company_flag,number_type"]
lookup = lookup[0].split(',')
output = []
for i in lookup:
	try:
		output.append(headers[i.strip()])
	except:
		output.append(i.strip())

print output