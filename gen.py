from heapq import *

class Processo:
    # ps: acoes de executar e dormir estao sempre alternadas
    # a primeira acao e' sempre uma execucao

    def __init__(self, nome, acoes, tempo):
        self.nome = nome
        self.acoes = acoes
        self.tempo_de_chegada = tempo
    def ver_acao(self):
        self.acoes[0]
    def proxima_acao(self):
        return self.acoes.pop(0)
    def inserir_acao(self, acao):
        self.acoes.insert(0, acao)

class Fila_de_espera:
    fila = []

    def __init__(self, f):
        heapify(f)
        print f
        self.fila = heapify(f)

    def dormir(self, tempo, nome):
        heappush(self.fila, (tempo, nome))
    def acordar(self):
        tempo, acordado = heappop(self.fila)
        return acordado
    def tempo_a_acordar(self):
        tempo, nome = heappop(self.fila)
        self.dormir(tempo, nome)
        return tempo
    def alguem_vai_acordar(self, em_certo_tempo):
        return self.fila and self.tempo_a_acordar() < em_certo_tempo
    def despertador(self, em_certo_tempo):
        while self.alguem_vai_acordar(em_certo_tempo):
           yield self.acordar()
    def tick(self, tempo_a_subtrair):
        self.fila = [(tempo - tempo_a_subtrair, nome) for (tempo, nome) in self.fila]


def escalonador_fifo(espera, overhead, qqqqq):
    print '* Iniciando FIFO'
    prontos = []

    while prontos or espera.fila:
        if not prontos:
            tempo_ocioso = espera.tempo_a_acordar()
            pronto = espera.acordar()
            prontos.append(pronto)
            espera.tick(tempo_ocioso)
            continue

        proximo = prontos.pop(0)
        tempo_executando = proximo.proxima_acao()

        if overhead:
            yield ['exec', 'O Escalonador', overhead]
        yield ['exec', proximo.nome, tempo_executando]

        for pronto in espera.despertador(tempo_executando):
            prontos.append(pronto)
            yield ['acordou', pronto.nome]

        espera.tick(tempo_executando)

        if not proximo.acoes:
            yield ['terminou', proximo.nome]
        else:
            tempo_a_dormir = proximo.proxima_acao()
            espera.dormir(tempo_a_dormir, proximo)
            yield ['dormiu', proximo.nome]

def escalonador_rr(espera, overhead, quantum):
    print '* Iniciando Round Robin'

    prontos = []

    while prontos or espera.fila:
        #print 'prontos: ', prontos
        #print 'espera:  ', espera.fila

        if not prontos:
            tempo_ocioso = espera.tempo_a_acordar()
            yield ['nada', tempo_ocioso]
            pronto = espera.acordar()
            prontos.append(pronto)
            espera.tick(tempo_ocioso)
            continue

        proximo = prontos.pop(0)
        tempo_executando = proximo.proxima_acao()

        chutado = False

        if overhead:
            yield ['exec', 'O Escalonador', overhead]
            espera.tick(overhead)

        if tempo_executando <= quantum:
            yield ['exec', proximo.nome, tempo_executando]
        else:
            yield ['exec', proximo.nome, quantum]
            yield ['chutado', proximo.nome]
            chutado = True
            proximo.inserir_acao(tempo_executando - quantum)
            prontos.append(proximo)

        for pronto in espera.despertador(tempo_executando):
            prontos.append(pronto)
            yield ['acordou', pronto.nome]

        espera.tick(tempo_executando)

        if chutado:
            continue

        if not proximo.acoes:
            yield ['terminou', proximo.nome]
        else:
            tempo_a_dormir = proximo.proxima_acao()
            espera.dormir(tempo_a_dormir, proximo)
            yield ['dormiu', proximo.nome]

def passo(acoes, acao):
    tipo, nome = acao[:2]
    if tipo == 'terminou':
        print "%s terminou." % nome
    elif tipo == 'acordou':
        print "%s acordou." % nome
    elif tipo == 'dormiu':
        print "%s dormiu." % nome
    elif tipo == 'chutado':
        print "%s foi chutado." % nome
    elif tipo == 'nada':
        acoes.append((nome, 'Nada'))
        print "Nada acontece por %ss" % nome
    elif tipo == 'exec':
        tempo = acao[2]
        acoes.append((tempo, nome))
        print "%s executa por %ss." %(nome, tempo)
    else:
        raise Exception("Acao desconhecida?")

    return acoes

def ee(processos):
    return [(p.tempo_de_chegada, p) for p in processos]

def executar(escalonador, processos, overhead, quantum):
    acoes = []
    espera = Fila_de_espera(ee(processos))

    print '---------------------------------------'
    for acao in escalonador(espera, overhead, quantum):
        #print acao
        acoes = passo(acoes, acao)
    print '---------------------------------------'
    print
    return acoes

def total(l):
    return reduce(lambda x, y: x + y[0], l, 0)

def make_dict(l):
    i = 0.0
    d = {}
    for p in l:
        e = p[1]
        if not e in d:
            d[e] = i
            i += 1

    return d
#a = Processo('a', [1.0, 10.0, 3.0])
#b = Processo('b', [20.0, 1.0, 5.0, 2.0, 3.0, 5.0, 6.0])

a = Processo('O Processo A', [1, 2, 1], 10)
b = Processo('O Processo B', [1, 2, 1], 2)
c = Processo('O Processo C', [0.7, 1.0, 0.2], 0.4)
d = Processo('O Processo D', [0.7, 1.0, 0.2], 0.5)
g = Processo('O Processo E', [0.7, 1.0, 0.2], 0.6)

class Resultado:
    def __init__(self, acoes):
        #print acoes
        self.acoes = acoes
        self.total = total(acoes)
        self.ordem = make_dict(acoes)
        self.num = len(self.ordem)

def f(l, o, q):
    if q:
        esc = escalonador_rr
    else:
        esc = escalonador_fifo

    return Resultado(executar(esc, l, o ,q))

q = [a, b]

def e(): f(q, 0.5, 0.0)
