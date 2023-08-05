#logging decorator

This project provides a logging decorator that allows you to put a wrapper on your functions to log their output. Inspired by cross cutting technologies I thought I'd do the same for Python.

```
from Baubles.Logger import Logger

logger = Logger()


@logger.warning
def handler(*args, **kwargs):
	return 'in handler (%s, %s)' % (args, kwargs)


class Test(object):
	@logger.debug
	def __init__(self):
		pass

	@logger.debug
	def __del__(self):
		pass

	@logger.info
	def run(self, a, k=None):
		return 'kk'

	@logger.handle
	def noFail(self, arg1, arg2, kwargs1=None):
		logger.info('did not fail')
		return True

	@logger.handle
	def willFail(self, arg1, arg2, kwargs1=None):
		raise Exception('failed and logged')
		return False

	@logger.handle(handler=handler)
	def doFail(self, arg1, arg2, kwargs1=None):
		raise Exception('failed and handled')
		return False
```
