############################
# From tutorial: http://plumberjack.blogspot.com/2010/09/using-logging-with-multiprocessing.html
# 
# https://docs.python.org/2/library/queue.html
# RabbitMQ would be super cool to implement (stack or queue)
############################


import logging
import logging.handlers
import multiprocessing

class QueueHandler(logging.Handler):
	def __init__(self, queue):
		'''
		Initalize an instance using the passed queue argument
		'''
		logging.Handler.__init__(self)
		self.queue = queue

	def emit(self, record):
		'''
		Emits record, writing the LogRecord to the queue
		'''
		try:
			ei = record.exc_info
			if ei:
				dummy = self.format(record)
				record.exc_info = None
			self.queue.put_nowait(record)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)

def listener_configurer():
	root = logging.getLogger()
	fh = logging.handlers.RotatingFileHandler('/tmp/mptest.log', 'a', 300, 10)
	format = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
	fh.setFormatter(format)
	rott.addHandler(fh)

def listener_process(queue, configurer):
	configurer()
	while True:
		try:
			record = queue.get()
			if record is None:
				break
			logger = logging.getLogger(record.name)
			logger.handle(record)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			import sys, traceback
			print >> sys.stderr, 'Whoops! Problem:'
			traceback.print_exc(file=sys.stderr)

LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING,
          logging.ERROR, logging.CRITICAL]

LOGGERS = ['a.b.c', 'd.e.f']

MESSAGES = [
    'Random message #1',
    'Random message #2',
    'Random message #3',
]

def worker_configurer(queue):
	h = QueueHandler(queue)
	root = logging.getLogger()
	root.addHandler(h)
	root.setLevel(logging.DEBUG)

def worker_process(queue, configurer):
	configurer(queue)
    name = multiprocessing.current_process().name
    print('Worker started: %s' % name)
    for i in range(10):
        time.sleep(random())
        logger = logging.getLogger(choice(LOGGERS))
        level = choice(LEVELS)
        message = choice(MESSAGES)
        logger.log(level, message)
    print('Worker finished: %s' % name)

def main():
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(target=listener_process,
                                       args=(queue, listener_configurer))
    listener.start()
    workers = []
    for i in range(10):
        worker = multiprocessing.Process(target=worker_process,
                                       args=(queue, worker_configurer))
        workers.append(worker)
        worker.start()
    for w in workers:
        w.join()
    queue.put_nowait(None)
    listener.join()

if __name__ == '__main__':
    main()