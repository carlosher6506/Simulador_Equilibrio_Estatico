import sys

def Convertion_KG(Kg):
    K = Kg
    result = K * 9.81
    return result

def Convertion_Newton(Ne):
    N = Ne
    result = N / 9.81
    return result



while True:
    print('----- Menu -----')
    print('1. Convertir KG a Newton')
    print('2. Convertir Newton a KG')
    print('3. Salir')

    op = int(input('Ingrese la opcion: '))
    if op == 1:
        Kg = float(input('Ingrese La Cntidad en KG: '))
        print(f'Valor en KG: {Kg}')
        result = Convertion_KG(Kg)
        print(f'Valor en Newton: {result}')
    elif op == 2:
        Ne = float(input('Ingrese La Cntidad en Newton: '))
        print(f'Valor en Newton: {Ne}')
        result = Convertion_Newton(Ne)
        print(f'Valor en KG: {result}')
    elif op == 3:
        print('Saliendo...')
        exit()