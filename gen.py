from heapq import *

class Processo:
    # ps: acoes de executar e dormir estao sempre alternadas
    # a primeira acao e' sempre uma execucao

    def __init__(self, nome, acoes):
        self.nome = nome
        self.acoes = acoes
    def ver_acao(self):
        self.acoes[0]
    def proxima_acao(self):
        return self.acoes.pop(0)

class Fila_de_espera:
    fila = []

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


def escalonador_fifo(prontos):
    espera = Fila_de_espera()
    while prontos or espera.fila:
        if not prontos:
            tempo_ocioso = espera.tempo_a_acordar()
            pronto = espera.acordar()
            prontos.append(pronto)            
            espera.tick(tempo_ocioso)
            continue

        proximo = prontos.pop(0)
        tempo_executando = proximo.proxima_acao()

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

def passo(acao):
    tipo, nome = acao[:2]
    if tipo == 'terminou':
        print "%s terminou." % nome
    elif tipo == 'acordou':
        print "%s acordou." % nome
    elif tipo == 'dormiu':
        print "%s dormiu." % nome
    elif tipo == 'exec':
        tempo = acao[2]
        print "%s executa por %ss." %(nome, tempo)
    else:
        raise Exception("Acao desconhecida?")

def executar(escalonador, processos):
    for acao in escalonador(processos):
        passo(acao)


a = Processo('a', [1, 10, 3])
b = Processo('b', [20, 1, 5, 2, 3, 5, 6])

def e(): executar(escalonador_fifo, [a, b])
