class EscapeSequence:

    def __init__(self):
        self.flag = False

    def resetChange(self):
        print('\033[0m', end='')

    def setCharBold(self):
        print('\033[1m', end='')

    def setCharFine(self):
        print('\033[2m', end='')

    def setCharIteric(self):
        print('\033[3m', end='')

    def setCharUnderline(self):
        print('\033[4m', end='')

    def setCharDelete(self):
        print('\033[9m', end='')

    def setCharBlack(self):
        print('\033[30m', end='')

    def setCharRed(self):
        print('\033[31m', end='')

    def setCharGreen(self):
        print('\033[32m', end='')

    def setCharYellow(self):
        print('\033[33m', end='')

    def setCharBlue(self):
        print('\033[34m', end='')

    def setCharMagenta(self):
        print('\033[35m', end='')

    def setCharCyan(self):
        print('\033[36m', end='')

    def setCharWhite(self):
        print('\033[37m', end='')

    def setCharN(self, n: int):
        string = '\033[38;5;' + str(n) + 'm'
        print(string, end='')

    def resetChar(self):
        print('\033[39m', end='')

    def setBackBlack(self):
        print('\033[40m', end='')

    def setBackRed(self):
        print('\033[41m', end='')

    def setBackGreen(self):
        print('\033[42m', end='')

    def setBackYellow(self):
        print('\033[43m', end='')

    def setBackBlue(self):
        print('\033[44m', end='')

    def setBackMagenta(self):
        print('\033[45m', end='')

    def setBackCyan(self):
        print('\033[46m', end='')

    def setBackWhite(self):
        print('\033[47m', end='')

    def resetBack(self):
        print('\033[49m', end='')

    def showAllColor(self):
        for i in range(256):
            print('\033[48;5;', i, 'm', sep='', end='')
            print(' '*4, end='')
            print('\033[49m', end=' ')
            print('\033[38;5;', i, 'm', sep='', end='')
            print('hoge', i, end=' ')
            print('\033[39m', end='')
            print()


if __name__ == '__main__':
    es = EscapeSequence()
    es.showAllColor()
