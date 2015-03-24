script_template: the module that all of the scripts use
source scripts: contains to-be or converted source scripts
	-> folders inside are broken up by template type
Templates: contains examples for each type of template
test: test environment for EC2
	-> Master.py runs all files inside either 'tester' or 'Master' folder depending on which one designated in script
canonical_headers: contains canonical headers
