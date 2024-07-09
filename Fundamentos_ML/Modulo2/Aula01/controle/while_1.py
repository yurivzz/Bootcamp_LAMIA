total = 10
qtde = 0
nota = 0

while nota != -1:
    nota =  float(input('Informe o número ou -1 para sair: '))
    if nota != -1:
        total+= nota
        qtde += 1

print(f'A média da turma é {total/qtde}')