import threading
import base, gen
import gtk, gobject, cairo
import time

import config

gtk.gdk.threads_init()

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
        self.set_r(gen.q, 0.5)

    def draw_seg(self, cr, line):
        cr.set_line_width(0.003)
        cr.set_source_rgb(line.r, line.g, line.b)
        cr.move_to(line.comeco, line.altura)
        cr.line_to(line.comeco + line.tamanho, line.altura)
        cr.stroke()

    def set_r(self, l, o):
            self.r = gen.f(l, o)
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

def timeout():
    plot.queue_draw()
    return True

gobject.timeout_add(16, timeout)

base.main(plot, plot.set_r)
