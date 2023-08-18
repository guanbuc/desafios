# -*- encoding: utf-8 -*-
import datetime as dt

def main():
    #Integer = input('Inserir seu valor:')
    #trf2(int(Integer))
    trf(1633570016)

def trf(parDt):
    print(dt.datetime.strftime(dt.datetime.fromtimestamp(parDt), '%Y-%m-%d'))

def trf1(pString):
    if pString.upper()[0] == 'B':
        print('começa com B')

        if pString.upper()[-1] == 'A':
            print('termina com A')

        else:
            print(f'começa com {pString.upper()[0]}\ntermina com {pString.upper()[-1]}')

    else:
        print(f'começa com {pString.upper()[0]}\ntermina com {pString.upper()[-1]}')

def trf2(pValor):
    lst = [11, 18, 25, 32, 39]
    x = 0
    if pValor <= 0:
        print(f'retornará: {0}')

    elif pValor <= len(lst):
        print(f'retornará: {lst[pValor-1]}')

    else:
        while x <= (pValor - (len([11, 18, 25, 32, 39])))-1:

            x+=1

            lst.append((lst[-1]+7))

        print(f'retornará: {lst[-1]}')

if __name__ == '__main__':
    main()