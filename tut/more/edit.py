import gtk
import pygtk

window = gtk.Window()
window.connect("destroy", lambda w: gtk.main_quit())
vbox = gtk.VBox()
hbox = gtk.HBox()
label = gtk.Label('Loading')
entry = gtk.Entry()
button = gtk.Button(stock='gtk-ok')
vbox.pack_start(label)
vbox.add(hbox)
hbox.pack_start(entry)
hbox.pack_end(button)
#entry.connect('activated',self.key_set,entry.get_text())
#button.connect('clicked',self.key_set)
window.add(vbox)
#label.set_label(self.load_keys())
window.show_all()
gtk.main()
