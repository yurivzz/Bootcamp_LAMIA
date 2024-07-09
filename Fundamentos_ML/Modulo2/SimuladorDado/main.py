import random
from collections import Counter
from functools import reduce

class Dado:
    def __init__(self, lados=6):
        self.lados = lados

    def rolar(self):
        return random.randint(1, self.lados)

    def rolar_varias_vezes(self, vezes):
        return [self.rolar() for _ in range(vezes)]

class SimuladorDeDados:
    def __init__(self, dado):
        self.dado = dado
        self.resultados = []

    def simular(self, vezes):
        self.resultados = self.dado.rolar_varias_vezes(vezes)
        return self.resultados

    def calcular_estatisticas(self):
        soma = lambda a, b: a + b
        total = reduce(soma, self.resultados)
        media = total/len(self.resultados)


        frequencia = dict(sorted(Counter(self.resultados).items()))
        return {
            "media": media,
            "frequencia": frequencia
        }


dado = Dado(lados=7)
simulador = SimuladorDeDados(dado)

resultados = simulador.simular(200)

# Calculando estatísticas
estatisticas = simulador.calcular_estatisticas()

print(f"Média: {estatisticas['media']}")
print(f"Frequência: {estatisticas['frequencia']}")
print(f'Resultados: {simulador.resultados}')
