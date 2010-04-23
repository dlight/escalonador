# !/usr/bin/env python
import gtk
import pygtk
import gconf
class Gui:
    def __init__(self):
        self.keylocation = '/apps/avant-window-navigator/applets/MediaControl/Album_Art'
        self.client = gconf.client_get_default()
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
        button.connect('clicked',self.key_set)
        window.add(vbox)
        label.set_label(self.load_keys())
        window.show_all()
        self.label = label
        self.entry = entry
    def gconfkey(self):
        
        self.entry = entry    
    def load_keys(self):
        """
        Loads all the gconf variables 
        """
	var = ""
        var = self.client.get_string(self.keylocation)
        var = 'Current key value: ' + var
        return var
    def key_set(self,widget):
        """
        This Method takes the keyname and sets a value
        """
        var = self.entry.get_text()
        try:
            self.client.set_string        (self.keylocation,var)
        except:
            print 'Fail' 
        self.label.set_label(self.load_keys())
if __name__ == '__main__':
    main = Gui()
    gtk.main()
