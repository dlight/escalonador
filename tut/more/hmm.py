import gtk

def criar_config():
    window = gtk.Window()
    vbox = gtk.VBox(False, 5)
    vbox.set_border_width(5)
    window.add(vbox)
    window.connect("destroy", lambda x: x.destroy())
    window.set_title("Criar Processos")

    read = []

    def vals(x): print([f() for f in read])

    def add_opt(s):
        b = gtk.HBox(False, 5)

        o = gtk.Entry()
        l = gtk.Label(str=s)
        b.add(l)
        b.add(o)
        vbox.add(b)
        read.append(o.get_text)

    add_opt('Trem 1')
    add_opt('Trem 2')
    add_opt('Trem 3')
    add_opt('Trem 4')
    add_opt('Trem 5')

    hbox = gtk.HBox(False, 5)
    alig = gtk.Alignment(1, 0, 0, 0)
    alig.add(hbox)
    vbox.add(alig)

    def add_bt(s, f):
        #a.set_padding(0, 3, 3, 3)

        b = gtk.Button(label=s)
        b.connect_object("clicked", f, window)
        hbox.add(b)


    add_bt('Ok', vals)
    add_bt('Cancelar', lambda x: x.destroy())

    window.show_all()

if __name__ == "__main__":
    criar_config()
    criar_config()
    gtk.main()


