import threading
import random, time
import gtk
#Initializing the gtk's thread engine
gtk.threads_init()


class FractionSetter(threading.Thread):
	"""This class sets the fraction of the progressbar"""
	
	#Thread event, stops the thread if it is set.
	stopthread = threading.Event()
	
	def run(self):
		"""Run method, this is the code that runs while thread is alive."""
		
		#Importing the progressbar widget from the global scope
		global progressbar 
		
		#While the stopthread event isn't setted, the thread keeps going on
		while not self.stopthread.isSet() :
			# Acquiring the gtk global mutex
			gtk.threads_enter()
			#Setting a random value for the fraction
			progressbar.set_fraction(random.random())
			# Releasing the gtk global mutex
			gtk.threads_leave()
			
			#Delaying 100ms until the next iteration
			time.sleep(0.1)
			
	def stop(self):
		"""Stop method, sets the event to terminate the thread's main loop"""
		self.stopthread.set()

def main_quit(obj):
	"""main_quit function, it stops the thread and the gtk's main loop"""
	#Importing the fs object from the global scope
	global fs
	#Stopping the thread and the gtk's main loop
	fs.stop()
	gtk.main_quit()

#Gui bootstrap: window and progressbar
window = gtk.Window()
progressbar = gtk.ProgressBar()
window.add(progressbar)
window.show_all()
#Connecting the 'destroy' event to the main_quit function
window.connect('destroy', main_quit)

#Creating and starting the thread
fs = FractionSetter()
fs.start()

gtk.main()

