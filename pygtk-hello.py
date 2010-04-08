#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk

def main():
    w = gtk.Window(gtk.WINDOW_TOPLEVEL)
    w.set_name ("Test Input")
    w.connect("destroy", lambda x: gtk.main_quit())

    #vbox = gtk.VBox(False, 0)
    #window.add(vbox)

    button = gtk.Button("Quit")
    w.add(button)
    button.show()

    w.show()
    gtk.main()

main()

#    vbox.pack_start(button, True, True, 0)
#    vbox.pack_start(button2, True, True, 0)
    #vbox.pack_start(button, False, False, 0)
    #vbox = gtk.VBox(False, 0)
    #window.add(vbox)
    #vbox.show()
#    button2 = gtk.Button("Quit2")
#    w.add(button)
#    button.show()
