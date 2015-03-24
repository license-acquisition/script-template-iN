import codecs

g = codecs.open('headers.txt', 'r').readlines()
g = g.split('\n')

info = []
for line in g:
	