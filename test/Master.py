from multiprocessing import Process, Queue, Pool
from subprocess import call
import sys
import re, codecs, Queue, os
import time
import glob
from script_template import logger

stamp = time.strftime("%Y%m%d")

ScrapeQueue = Queue.Queue()
m = logger('Master', 'Y')
def fork(toDo):
        l = logger(toDo.replace('.py','').replace('./Master\\', '').replace('./tester\\',''), 'Y')
        name = "%s"%(toDo.split('\\')[1].replace(".py",""))
        direct = os.getcwd()
        os.chdir(direct)
        l.info("Starting: %s"%(name))
        start = time.time()
        try:
                call(["python", toDo])
                l.info("Completed: %s"%(name))
        except Exception as e:
                l.critical('Error on %s!' %(name))
                l.critical(str(e))
        #count = open('%s_%s_000.csv'%(name,stamp), 'r').read().count("\n")
        #l.info("Number of records: %s" %count)
        l.info("Minutes elapsed: %s" %str((time.time()-start)/60))

if __name__ == '__main__':
        p = Pool(2)
        ScrapeQueue = []
        ScrapeQueue.append(glob.glob('./Master/*.py'))
        m.info(' # '*25)
        m.info(ScrapeQueue[0])
        p.map(fork, ScrapeQueue[0])
        m.info('All Donez')
