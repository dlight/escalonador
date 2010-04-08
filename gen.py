class Processo:
    def __init__(self, nome, acoes):
        self.nome = nome
        self.acoes = acoes
    def nova_acao(self, tipo, tempo):
        self.acoes.append((tipo, tempo))

def escalonador_fifo(prontos):
    while prontos != []:
        #print "Debug: %s" % prontos
        proximo = prontos.pop(0)
        tipo, tempo = proximo.acoes.pop(0)
        yield [proximo.nome, tipo, tempo]
        if proximo.acoes == []:
            yield [proximo.nome, 'fim']
        else:
            prontos.append(proximo)

def passo(acao):
    nome = acao.pop(0)
    tipo = acao.pop(0)
    if tipo == 'fim':
        #print 'amm'
        print "Processo finalizado: %s" % nome
        #print 'err'
    else:
        tempo = acao.pop(0)
        print "Processo %s fica %s por %s segundos" % (nome, tipo, tempo)

def executar(escalonador, processos):
    for acao in escalonador(processos):
        passo(acao)


a = Processo('a', [('ahm', 1), ('wait', 10)])
b = Processo('b', [('ahm', 20), ('wait', 1)])

def e(): executar(escalonador_fifo, [a, b])
