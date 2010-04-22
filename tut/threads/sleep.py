import threading

class FractionSetter(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		"""while sentence will continue until the stopthread event is set"""
		while not self.stopthread.isSet():
			print "I'm a fancy thread, yay!"
	
	def stop(self):
		self.stopthread.set()
		
fs = FractionSetter()
fs.start()

#Waiting 2 seconds until the thread stop
import time
time.sleep(2)

#Stopping the thread
fs.stop()
