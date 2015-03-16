import time, codecs, logging

'''
def logger(feed_name, status, error_string=''):
    l = codecs.open('log.csv', 'a')
    l.write(','.join([feed_name, str(time.strftime('%Y/%m/%d')), str(time.strftime('%H:%M:%S')), status, error_string]) + '\n')
    l.close()
'''

def logger(feed):
    # set up loggers
    logger = logging.getLogger(str(feed))
    logger.setLevel(logging.DEBUG)
    helper = logging.getLogger('HELPER')
    helper.setLevel(logging.DEBUG)

    # create handlers
    ch1 = logging.StreamHandler()
    ch1.setLevel(logging.CRITICAL)
    ch2 = logging.StreamHandler()
    ch2.setLevel(logging.DEBUG)
    fh1 = logging.FileHandler('main.log')
    fh1.setLevel(logging.DEBUG)
    fh2 = logging.FileHandler('%s.log' %feed)
    fh2.setLevel(logging.DEBUG)

    # format and add to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  '%m/%d/%Y %H:%M:%S')
    for handler in [ch, fh1, fh2]:
        handler.setFormatter(formatter)

    # add handlers to loggers
    logger.addHandler(ch1)
    logger.addHandler(fh1)
    helper.addHandler(ch2)
    helper.addHandler(fh2)

    return logger, helper
