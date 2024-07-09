def soma(a, b):
    return a + b

def sub(a, b):
    return a - b

somar = soma
print(somar(3, 4))


def operacao_aritmetica(fn, op1, op2):
    return fn(op1, op2)


resultado = operacao_aritmetica(soma, 13, 48)
print(resultado)

resultado = operacao_aritmetica(sub, 13, 48)
print(resultado)


def soma_parcial(a):
    def concluir_soma(b):
        return a + b
    return concluir_soma


resultado_final = soma_parcial(10)(12)
print(resultado_final)
