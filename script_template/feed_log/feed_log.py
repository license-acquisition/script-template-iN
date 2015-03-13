import time, codecs

def log(feed_name, status, error_string=''):
    l = codecs.open('log.csv', 'a')
    l.write(','.join([feed_name, str(time.strftime('%Y/%m/%d')), str(time.strftime('%H:%M:%S')), status, error_string]) + '\n')
    l.close()
