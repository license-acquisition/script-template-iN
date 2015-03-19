from multiprocessing import Process, Queue, Pool
from subprocess import call, Popen
import sys
import re, codecs, Queue, os
import time
import glob
from script_template import logger

stamp = time.strftime("%Y%m%d")

ScrapeQueue = Queue.Queue()
m = logger('Master', 'Y')
def fork(toDo):
        log_name = toDo.replace('.py','').replace('./Master\\', '').replace('./tester\\','')
        l = logger(log_name, 'Y')
        #sys.stdout = l.critical
        name = "%s"%(toDo.split('\\')[1].replace(".py",""))
        direct = os.getcwd()
        os.chdir(direct)
        l.info("Loading files from dir")
        l.info("Calling feed: %s"%(name))
        start = time.time()
        try:
                script = Popen(["python", toDo])
                while script.poll() is None:
                        time.sleep(5)
                if 'CRITICAL' not in open('./script_logs/%s.log' %name.split('_')[0], 'r').readlines()[-1]:
                        l.info("Completed: %s"%(name))
                        l.info("Minutes elapsed: %s" %str((time.time()-start)/60))
                else:
                        raise Exception
        except Exception as e:
                l.critical('Error on %s!' %(name))
        
        
if __name__ == '__main__':
        p = Pool(2)
        ScrapeQueue = []
        ScrapeQueue.append(glob.glob('./Master/*.py'))
        m.info(' # '*25)
        m.info(ScrapeQueue[0])
        try:
                p.map(fork, ScrapeQueue[0])
        except Exception as e:
                m.critical('Master script failed.')
                m.critical(str(e))
        finally:
                m.info('Closed properly')
