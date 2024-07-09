# for i in range(10):
    # print(i)

# for i in range(1,11):
    # print(i)

# for i in range(1, 100, 7):
    # print(i)

# nums = [2,4,6,8]
# for n in nums:
    # print(n, end=",")

# texto = "Python é massa"

# for letra in texto:
    # print(letra, end=' ')
    
# for n in {1, 2, 3, 4, 4, 5}:
    # print(n, end=' ')

produto = {
    'nome': 'Caneta',
    'preco': 8.80,
    'desc': 0.5
}

# for atrib in produto:
    # print(atrib, '==>', produto[atrib])

for atrib, value  in produto.items():
    print(atrib, '=>', value)

for valor in produto.values():
    print(valor, end=' ')

for atrib  in produto.keys():
    print(atrib, end=' ')