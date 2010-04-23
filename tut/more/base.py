#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo

import sys
sys.path.insert(0, '')

import gen

import os, signal

import config

class Tela(gtk.DrawingArea):

    __gsignals__ = { "expose-event": "override" }

    def do_expose_event(self, event):
        cr = self.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.rectangle(0, 0, width, height)
        cr.fill()

    def size_request(self):
        (640, 480)

def main(tela, hmm):
    global x
    x = hmm

    def quit(x):
        gtk.main_quit()

    janela = gtk.Window()
    janela.set_title("Escalonador")
    janela.connect("destroy", quit)

    vbox = gtk.VBox(False, 5)
    vbox.set_border_width(0)
    vbox.show()
    janela.add(vbox)

    tela.show()
    tela.size_request()

    align = gtk.Alignment(1, 0.5, 0, 0)
    align.set_padding(0, 3, 3, 3)

    botao = gtk.Button("Config")
    botao.connect_object("clicked", config.criar_config, janela)
    botao.show()

    align.add(botao)
    align.show()

    vbox.pack_start(tela, True, True, 0)
    vbox.pack_start(align, False, False, 0)

    vbox.set_size_request(640, 480)


    #vbox.add(tela)

    janela.present()
    #janela.show()
    gtk.main()

if __name__ == "__main__":
    main(Tela(), lambda x: x)

#    vbox.pack_start(button, True, True, 0)
#    vbox.pack_start(button2, True, True, 0)
    #vbox.pack_start(button, False, False, 0)
    #vbox = gtk.VBox(False, 0)
    #window.add(vbox)
    #vbox.show()
#    button2 = gtk.Button("Quit2")
#    w.add(button)
#    button.show()
