import random

class Bingo:
    def __init__(self):
        self.balotas = {
            'B': [i for i in range(1, 16)],
            'I': [i for i in range(16, 31)],
            'N': [i for i in range(31, 46)],
            'G': [i for i in range(46, 61)],
            'O': [i for i in range(61, 76)],
        }
        self.llamadas = {
            'B': [],
            'I': [],
            'N': [],
            'G': [],
            'O': [],
        }

    def get_balota(self):
        letra = ''
        while self.balotas.get(letra) == [] or self.balotas.get(letra) is None:
            letra = random.choice(list(self.balotas.keys()))
        numero = random.choice(self.balotas[letra])
        self.balotas[letra].remove(numero)
        self.llamadas[letra].append(numero)
        self.llamadas[letra].sort()
        return f'{letra}{numero}'

    def empty(self):
        empty = True
        for letra in self.balotas:
            if self.balotas[letra] != []:
                empty = False
                break
        return empty

if __name__ == '__main__':
    counter = 0
    bingo = Bingo()
    while True:
        if bingo.empty():
            print('¡El tablero ha sido llenado! Se termina el juego.')
            break
        i = input('Presiona enter para llamar una nueva balota:')
        print(bingo.get_balota())
        counter += 1
        if counter == 15:
            counter = 0
            print('Balotas restantes:')
            for letra in bingo.balotas:
                print(f'{letra}: {bingo.balotas[letra]}')
            print('Balotas llamadas:')
            for letra in bingo.llamadas:
                print(f'{letra}: {bingo.llamadas[letra]}')
