class Produto:
    def __init__(self, nome, preco = 1.99, desc=0):
        self.nome = nome
        self.__preco = preco
        self.desc = desc
    @property
    def preco(self):
        return self.__preco
    
    @preco.setter
    def preco(self, novo_preco):
        if novo_preco > 0:
            self.__preco = novo_preco

    @property
    def preco_final(self):
        return (1 - self.desc) * self.__preco

p1 = Produto('Caneta', 10, 0.1)
p2 = Produto('Caderno', 14, 0.5)

p1.preco = 70.89
p2.preco = 17.99

print(p1.nome, p1.preco, p1.desc, p1.preco_final)
print(p2.nome, p2.preco, p2.desc, p2.preco_final)
