# -*- encoding: utf-8 -*-

import datetime as dt

def main():
    lista = []
    n = 0

    while n < 5:
        n += 1
        lista.append(input('Insira um novo número: '))

    print(f'\nInicio da execução: {dt.datetime.now()}\n')
    sequencial(lista)
    #binaria(lista)
    print(f'\nFim da execução: {dt.datetime.now()}\n')

def sequencial(par):
    n1 = 0
    n2 = input('Insira o número a se buscar: ')

    while n1 < len(par):
        if par[n1] == n2:
            print(n1)

        n1 += 1

def binaria(par):
    n2 = input('Insira o número a se buscar: ')

    def busca(n):
        n1 = n

        if n2 > par[n1]:
            n1 = int(round(((((n1 if n1 !=0 else len(par))) + n1)/2),0)) + 1
            busca(n1)

        elif n2 < par[n1]:
            n1 = int(round(((n1 + n1)/2),0)) - 1
            busca(n1)

        elif n2 == par[n1]:
            print(n1)




    busca(0)




if __name__ == '__main__':
    main()