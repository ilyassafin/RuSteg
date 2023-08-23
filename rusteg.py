import sys
from os import listdir
from getpass import getpass

import cryptocode
from stegano import lsb

def Reveal(Dir, OutputFile):
    Pswd = getpass('\nВведите ключ-пароль: ')
    while len(Pswd) < 4:
        Pswd = getpass('Был введён слишком короткий ключ-пароль (менее 4 символов). Повторите ввод: ')
    PartsOfMessage = []
    Files = listdir(Dir)
    Flag = False
    for File in Files:
        if File.endswith('.png'):
            EncryptedMessage = cryptocode.decrypt(lsb.reveal(f'{Dir}/{File}'), Pswd)
            if EncryptedMessage and EncryptedMessage.startswith('RuSteg'):
                Part = EncryptedMessage.replace('RuSteg', '').split('_____')
                PartsOfMessage.append((int(Part[0]), Part[1]))
                Flag = True
    if Flag:
        PartsOfMessage.sort()
        Msg = ''
        for Part in PartsOfMessage:
            Msg += Part[1]
        Msg = cryptocode.decrypt(Msg, Pswd)
        if OutputFile == '_____NONE_____':
            print(f'Спрятанное сообщение: {Msg}\n')
        else:
            OutputFile.write(Msg)
            print(f'Сообщение было записано в файл {OutputFile.name}\n')
    else:
        print('Ошибка: в выбранной директории не найдено скрытых сообщений!\n')

def Hide(Dir, Msg):
    if Msg == '_____NONE_____':
        Msg = input('\nВведите сообщение: ')
    else:
        print()
    Pswd = getpass('Введите ключ-пароль: ')
    while len(Pswd) < 4:
        Pswd = getpass('Был введён слишком короткий ключ-пароль (менее 4 символов). Повторите ввод: ')
    else:
        EncryptedMessage = cryptocode.encrypt(Msg, Pswd)
        Files = listdir(Dir)
        UsefulFiles = []
        for File in Files:
            if File.endswith('.png'):
                UsefulFiles.append(f'{Dir}/{File}')
        if len(UsefulFiles) == 0:
            print('Ошибка: в выбранной директории нет png-файлов!\n')
        PartialLength = len(EncryptedMessage) // len(UsefulFiles) + 1
        if PartialLength == 0:
            pass
            print('Ошибка: в выбранной директории слишком много png-файлов для корректной работы алгоритма!\n')
        else:
            Counter = 0
            for i in range(0, len(EncryptedMessage), PartialLength):
                FinalMessage = cryptocode.encrypt(f'RuSteg{Counter}_____{EncryptedMessage[i:i+PartialLength]}', Pswd)
                if UsefulFiles[Counter].endswith('.png'):
                    lsb.hide(UsefulFiles[Counter], FinalMessage).save(UsefulFiles[Counter])
                Counter += 1
            print('Сообщение успешно спрятано!\n')

if __name__ == '__main__':
    Argv = sys.argv
    if len(Argv) == 1:
        print('\nRuSteg')
        print('    Инструмент для стеганографии. Подробнее здесь: https://github.com/ilyassafin/RuSteg')
        print('    Версия: 1.0')
        print('    Автор: Сафин Ильяс (https://github.com/ilyassafin/)\n')
    elif len(Argv) == 2:
        print('Ошибка: введено недостаточное количество параметров!')
    elif len(Argv) == 3:
        if Argv[1] == '-h':
            Hide(Argv[2], '_____NONE_____')
        elif Argv[1] == '-r':
            Reveal(Argv[2], '_____NONE_____')
    elif len(Argv) == 5:
        if Argv[3] == '-f':
            if Argv[1] == '-h':
                with open(Argv[4], 'r') as InputFile:
                    Hide(Argv[2], InputFile.read())
            elif Argv[1] == '-r':
                with open(Argv[4], 'w') as OutputFile:
                    Reveal(Argv[2], OutputFile)