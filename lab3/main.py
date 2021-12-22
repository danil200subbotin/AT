from interpretator import Interpreter
from interpretator_staff.standard_converts import Var
import pygame



menu_main = ['1. Тестирование функциями',
             '2. Погонять робота',
             '3. запасной пункт',
             '0. Завершенение работы']
menu_functions = ['1. Пузырьковая сортировка',
                  '2. Нерекурсивный Фибоначи (with while)',
                  '3. Рекурсивный Фибоначи (with recursion)',
                  '0. Exit']
functions_set = ['',
                 'tests/array_test',
                 'tests/fibonacci.txt',
                 'tests/fibonacci_recursion.txt']
menu_robot = ['1. Небольшая карта',
              '2. Большая карта',
              '0. Exit']
maps = ['',
           'maps/test_map.txt',
           'Maps/test_map2']

if __name__ == '__main__':

    # while run:
    #     # pygame.draw.rect(win, (0, 0, 255), (x + 200, y + 200, w, h))
    #     # pygame.display.update()
    #     # pygame.time.delay(10000)
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #
    #     pygame.draw.rect(win, (0, 0, 255), (x, y, w, h))
    #     pygame.display.update()
    #     pygame.time.delay(100)
    #     pygame.draw.rect(win, (0, 0, 255), (x + 100, y + 100, w, h))
    #     pygame.display.update()
    # pygame.quit()

    run = True

    while run:
        print('Чем мучать?')
        for msg in menu_main:
            print(msg)
        choice = int(input())
        match choice:
            case 0:
                run = False
                print("ок.")
            case 1:
                print('Функции:')
                work1 = True
                while work1:
                    for msg in menu_functions:
                        print(msg)
                    choice = int(input())
                    if choice == 0:
                        work1 = False
                    elif choice in range(len(functions_set)):
                        interpr = Interpreter()
                        f = open(functions_set[choice])
                        text = f.read()
                        f.close()
                        interpr.interpreter(text)

                        print("Результат")
                        for sym_table in interpr.notion_table:
                            for keys, values in sym_table.items():
                                if isinstance(values, Var):
                                    if values.type == 'STRING':
                                        print(values.type, keys, '= \'', values.value, '\'')
                                    else:
                                        print(values.type, keys, '=', values.value)
                                elif isinstance(values[1], dict):
                                    print(values[0], keys, '=\n', values[1])
                                elif isinstance(values, list):
                                    print(values[0][0], ' o1f ', values[0][1], keys, '=\n', "[", end="")
                                    for index, i in enumerate(values[1]):
                                        print("  {", index, "}", i, ";", end="")
                                    print("]")

                        print('Records:')
                        for rec in interpr.records:
                            print(f'"{rec}" : {interpr.records[rec].child}')
                        print('Procedures:')
                        print(interpr.procedures)
            case 2:
                pygame.init()
                win = pygame.display.set_mode([1000, 1000])
                pygame.display.set_caption("Super-Puper Language")
                print('Где искать выход?')
                work1 = True
                while work1:
                    for msg in menu_robot:
                        print(msg)
                    choice = int(input())
                    if choice == 0:
                        work1 = False
                    elif choice in range(len(menu_robot)):
                        interpr = Interpreter(window=win)
                        interpr.read_map_document(maps[choice])
                        f = open('tests/rh_algritm.txt')
                        text = f.read()
                        f.close()
                        interpr.interpreter(text)
                        for sym_table in interpr.notion_table:
                            for keys, values in sym_table.items():
                                if isinstance(values, Var):
                                    if values.type == 'STRING':
                                        print(values.type, keys, '= \'', values.value, '\'')
                                    else:
                                        print(values.type, keys, '=', values.value)
                                elif isinstance(values[1], dict):
                                    print(values[0], keys, '=\n', values[1])
                                elif isinstance(values, list):
                                    print(values[0][0], ' of ', values[0][1], keys, '=\n', values[1])
                        print('Records:')
                        for rec in interpr.records:
                            print(f'"{rec}" : {interpr.records[rec]}')
                        print('Procedures:')
                        print(interpr.procedures)
                pygame.quit()
            case _:
                print('Incorrect input, try again')