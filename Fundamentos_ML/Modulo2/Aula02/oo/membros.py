class Contador():
    contador = 0

    def inst(self):
        return 'Estou bem!'

    @classmethod
    def inc(cls):
        cls.contador += 1
        return cls.contador
    
    @classmethod
    def dec(cls):
        cls.contador -= 1
        return cls.contador

    @staticmethod
    def mais_um(n):
        return n + 1
    
print(Contador.inc())
print(Contador.inc())
print(Contador.inc())
print(Contador.dec())
print(Contador.dec())
print(Contador.dec())
