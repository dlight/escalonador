import threading
import base
import gtk, gobject, cairo
import time

gtk.gdk.threads_init()

class Secret():
    q = 0
    def s(self, x):
        self.q = x
    def r(self):
        return self.q

class Thr(threading.Thread):
    stopthread = threading.Event()

    def __init__(self, shared, plot):
        threading.Thread.__init__(self)
        self.data = shared
        self.plot = plot
	
    def run(self):
        self.data.s(0)
        print "Teste.."
        while not self.stopthread.isSet():
            #print "AAAa, ", self.data.r()

            gtk.gdk.threads_enter()

            self.data.s(self.data.r() + 0.0006)
            self.plot.queue_draw()

            gtk.gdk.threads_leave()
            time.sleep(0.01)
	
    def stop(self):
        self.stopthread.set()

class Plot(base.Tela):
    def __init__(self, shared):
        base.Tela.__init__(self)
        self.data = shared

    def draw_seg(self, cr, begin, to, h, r, g, b):
        cr.set_line_width(0.003)
        cr.set_source_rgb(r, g, b)
        cr.move_to(0.01 + begin, h)
        cr.line_to(0.01 + to + begin, h)
        cr.stroke()

    def draw(self, cr, width, height):
        #print "Hmmm, ", self.data.r()

        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        cr.translate(0, 0)
        cr.scale(width / 1.0, height / 1.0)

        if (self.data.r() < 0.2):
            self.draw_seg(cr, 0, self.data.r(), 1 / 3.0, 0, 0, 0.8)
        else:
            self.draw_seg(cr, 0, 0.2, 1 / 3.0, 0, 0, 0.8)
            self.draw_seg(cr, 0.2, self.data.r() - 0.2, 1 / 5.0, 0.8, 0, 0)

s = Secret()

plot = Plot(s)

fs = Thr(s, plot)

fs.start()

def main_quit(obj):
	"""main_quit function, it stops the thread and the gtk's main loop"""
	#Importing the fs object from the global scope
	global fs
	#Stopping the thread and the gtk's main loop
	fs.stop()
	gtk.main_quit()

base.main(plot, main_quit)