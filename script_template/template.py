import codecs, time
from headers import get_headers

def create_file(feed_name, permission, headers_array):
    if permission == 'a':
        f = codecs.open(feed_name, permission, 'utf-8')
    else:
        f = codecs.open(feed_name+'_%s_000.csv'%(time.strftime('%Y%m%d')), permission, 'utf-8')
    headers = get_headers(headers_array)
    f.write('|'.join(headers) + '\n')
    return f
    
