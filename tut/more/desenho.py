import threading
import base, gen
import gtk, gobject, cairo
import time

import config

gtk.gdk.threads_init()

class Thr(threading.Thread):
    stopthread = threading.Event()

    def __init__(self, plot):
        threading.Thread.__init__(self)
        self.plot = plot

    def run(self):
        print "Teste.."
        while not self.stopthread.isSet():
            dt = 0.01 # segundos
            #print "AAAa, ", self.data.r()

            gtk.gdk.threads_enter()

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

cores = [(0.8, 0.0, 0.8),
   (0.0, 0.0, 0.8),
   (0.0, 0.8, 0.0),
   (0.8, 0.0, 0.0),
   (0.8, 0.8, 0.0),
   (0.0, 0.8, 0.8)]

class Plot(base.Tela):
    def __init__(self):
        base.Tela.__init__(self)
        self.set_r(gen.q)

    def draw_seg(self, cr, line):
        cr.set_line_width(0.003)
        cr.set_source_rgb(line.r, line.g, line.b)
        cr.move_to(line.comeco, line.altura)
        cr.line_to(line.comeco + line.tamanho, line.altura)
        cr.stroke()

    def set_r(self, l):
            self.r = gen.f(l)
            self.ta = time.time()
            self.tacc = self.ta
            self.lines = []

    def draw(self, cr, width, height):
        #print "Hmmm, ", self.data.r()

        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        cr.translate(0, 0)
        cr.scale(width / 1.0, height / 1.0)

        cor = (0.0, 0.0, 0.8)

        if self.r.acoes:
            p = self.r.acoes[0]
            tempo, nome = p

            #if len(self.r.acoes) == 1:
            #    print tempo, '!!'
            #    tempo -= 1.0

            ordem = self.r.ordem[nome]

            global cores
            cor = cores[int(ordem)]

            q = (ordem + 1) / (self.r.num + 1)

            t0 = (self.tacc - self.ta) / self.r.total
            dt = (time.time() - self.tacc) / self.r.total

            #print nome, dt

            line = Line(q, t0, dt, cor)
            if time.time() < tempo + self.tacc:
                #print self.t(), tempo, self.tacc
                self.draw_seg(cr, line)
            else:
                self.r.acoes.pop(0)
                self.lines.append(line)
                self.tacc += tempo

        for line in self.lines:
            self.draw_seg(cr, line)

plot = Plot()

fs = Thr(plot)

fs.start()

def main_quit(obj):
	"""main_quit function, it stops the thread and the gtk's main loop"""

	global fs
	fs.stop()
	gtk.main_quit()

base.main(plot, plot.set_r)
