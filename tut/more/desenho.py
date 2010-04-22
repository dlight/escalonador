import threading
import base, gen
import gtk, gobject, cairo
import time

gtk.gdk.threads_init()

class Secret:
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
            dt = 0.01 # segundos
            #print "AAAa, ", self.data.r()

            gtk.gdk.threads_enter()

            self.data.s(self.data.r() + dt)
            self.plot.queue_draw()

            gtk.gdk.threads_leave()
            time.sleep(dt)
	
    def stop(self):
        self.stopthread.set()

class Line:
    def __init__(self, h, begin, tam, cor):
        self.altura = h
        self.comeco = begin
        self.tamanho = tam
        self.r = cor[0]
        self.g = cor[1]
        self.b = cor[2]

cores = [(0.0, 0.0, 0.8),
   (0.0, 0.8, 0.0),
   (0.8, 0.0, 0.0),
   (0.8, 0.0, 0.8),
   (0.0, 0.8, 0.8)]

class Plot(base.Tela):
    def __init__(self, shared):
        base.Tela.__init__(self)
        self.data = shared
        self.tacc = 0.0
        self.lines = []

    def draw_seg(self, cr, line):
        cr.set_line_width(0.003)
        cr.set_source_rgb(line.r, line.g, line.b)
        cr.move_to(line.comeco, line.altura)
        cr.line_to(line.comeco + line.tamanho, line.altura)
        cr.stroke()

    def t(self):
        return self.data.r()

    def draw(self, cr, width, height):
        #print "Hmmm, ", self.data.r()

        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        cr.translate(0, 0)
        cr.scale(width / 1.0, height / 1.0)

        cor = (0.0, 0.0, 0.8)

        if base.r.acoes:
            p = base.r.acoes[0]
            tempo, nome = p

            ordem = base.r.ordem[nome]

            global cores
            cor = cores[int(ordem)]

            q = (ordem + 1) / (base.r.num + 1)

            t0 = self.tacc / base.r.total
            dt = (self.t() - self.tacc) / base.r.total

            print dt

            #print nome, dt

            line = Line(q, t0, dt, cor)
            if self.t() < tempo + self.tacc:
                self.draw_seg(cr, line)
            else:
                base.r.acoes.pop(0)
                self.lines.append(line)
                self.tacc += tempo

        for line in self.lines:
            self.draw_seg(cr, line)

        #if (self.data.r() < 0.2):
        #    self.draw_seg(cr, 0, self.data.r(), 1 / 3.0, 0, 0, 0.8)
        #else:
        #    self.draw_seg(cr, 0, 0.2, 1 / 3.0, 0, 0, 0.8)
        #    self.draw_seg(cr, 0.2, self.data.r() - 0.2, 1 / 5.0, 0.8, 0, 0)

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
