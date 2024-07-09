a = 'valor'
a = 0 # false
a = -1 # true
a = -0.00001 # true
a = '' # false
a = ' ' # true
a = [] # false
a = {} # false

if a:
    print('Existe!!!')
else:
    print('Não existe ou zero ou vazio')