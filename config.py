import gtk, re, base, gen

def criar_config(q):
    window = gtk.Window()
    vbox = gtk.VBox(False, 5)
    vbox.set_border_width(5)
    window.add(vbox)
    window.connect("destroy", lambda x: x.destroy())
    window.set_title("Config")

    s = 'Para cada processo, digite o tempo de cada\n' + \
            'acao (executar e esperar), alternadamente.\n' + \
            'Se o quantum nao for especificado, o\n' + \
            'algoritmo usado sera FIFO; caso contrario,\n' + \
            'Round Robin.'

    l = gtk.Label(str=s)
    l.set_line_wrap(True)
    vbox.add(l)

    read = []
    do_overhead = [lambda x: x]
    do_quantum = [lambda x: x]
    overhead = 0.0
    quantum = 0.0

    def vals(x):
        c = ['O Processo A', 'O Processo B', 'O Processo C',
            'O Processo D', 'O Processo E', 'O Processo F'].__iter__()
        def eachf(q):
            return gen.Processo(c.next(), [float(i.group(0)) for i in
                    re.finditer('[0-9.]+', q())])

        a = filter(lambda x: x.acoes, [eachf(f) for f in read])
        try:
            o = float(do_overhead[0]())
        except:
            o = 0.0

        try:
            q = float(do_quantum[0]())
        except:
            q = 0.0

        base.x(a, o, q)

    def add_opt(s, proc):
        b = gtk.HBox(False, 5)

        o = gtk.Entry()
        l = gtk.Label(str=s)
        b.add(l)
        b.add(o)
        vbox.add(b)
        if proc == 'q':
            do_quantum[0] = o.get_text
        if not proc:
            read.append(o.get_text)
        else:
            do_overhead[0] = o.get_text

    add_opt('Processo 1', 0)
    add_opt('Processo 2', 0)
    add_opt('Processo 3', 0)
    add_opt('Processo 4', 0)
    add_opt('Processo 5', 0)

    add_opt('Overhead', True)

    add_opt('Quantum', 'q')

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
    criar_config('a', lambda x: x)
    gtk.main()


