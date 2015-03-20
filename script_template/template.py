import codecs, time
from headers import get_headers
# drop module into Python > Lib > site-packages 

def create_file(feed_name, permission, headers_array):
    if permission == 'a':
        f = codecs.open('output/%s' %feed_name, permission, 'utf-8')
    else:
        f = codecs.open('output/%s_%s_000.csv'%(feed_name, time.strftime('%Y%m%d')), permission, 'utf-8')
    headers = get_headers(headers_array)
    f.write('|'.join(headers) + '\n')
    return f
    
