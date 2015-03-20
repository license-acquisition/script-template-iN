import time, codecs, logging

def logger(feed, master='N'):
    # set up loggers
    logger = logging.getLogger(str(feed))
    logger.setLevel(logging.DEBUG)

    # create handlers
    if master == 'N': # general use: individual script
        fh = logging.FileHandler('script_logs/%s.log' %feed)
        fh.setLevel(logging.DEBUG)
        fh2 = logging.FileHandler('main_%s.log' %time.strftime('%Y-%m-%d'))
        fh2.setLevel(logging.CRITICAL)
    else:
        fh = logging.FileHandler('main_%s.log' %time.strftime('%Y-%m-%d'))
        fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler() # logs to console all Critical errors
    ch.setLevel(logging.CRITICAL)    
    
    # format and add to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  '%Y/%m/%d %H:%M:%S')
    if master == 'N':
        for handler in [fh, fh2, ch]:
            handler.setFormatter(formatter)
            logger.addHandler(handler)
    else:
        for handler in [fh, ch]:
            handler.setFormatter(formatter)
            logger.addHandler(handler)
    
    return logger
