from multiprocessing import Process, Queue, Pool
from subprocess import call
import sys
import re, codecs, Queue, os
import time
import glob
from script_template import logger

stamp = time.strftime("%Y%m%d")

ScrapeQueue = Queue.Queue()

def fork(toDo):
        l = logger(toDo.replace('.py','').replace('./Master\', ''), 'Y')
        name = "%s"%(toDo).replace(".py","")
        direct = os.getcwd()
        os.chdir(direct)
        l.debug("Loading files from dir")
        l.debug("Feed to aggregate: %s"%(toDo))
        start = time.time()
        try:
                l.debug(call(["python", name + ".py"]))
                l.debug("Completed %s"%(toDo))
        except Exception as e:
                l.critical('Error on %s!' %(toDo))
                l.critical(str(e))
        #count = open('%s_%s_000.csv'%(name,stamp), 'r').read().count("\n")
        #l.debug("Number of records: %s" %count)
        l.debug("Completed in: %s" %str(time.time()-start))

if __name__ == '__main__':
        p = Pool(2)
        ScrapeQueue = []
        ScrapeQueue.append(glob.glob('./Master/*.py'))
        l.debug(ScrapeQueue)
        p.map(fork, ScrapeQueue[0])
        l.debug('All Donez')
