import random
import logic

def validator_strok(stroka):
    chasti = stroka.strip().split()
    if len(chasti) != 5:
        raise ValueError("В строке должно быть ровно 5 чисел.")
        
    karty = []
    for ch in chasti:
        if not ch.isdigit():
            raise ValueError(f"Элемент '{ch}' не является целым числом.")
        num = int(ch)
        if not (0 <= num <= 9):
            raise ValueError(f"Карта {num} выходит за допустимые границы [0..9].")
        karty.append(num)
    return karty

def vvod_vruchnuyu():
    while True:
        try:
            print("\nВведите 5 карт ПЕРВОГО игрока (числа 0-9 через пробел):")
            k1 = validator_strok(input("> "))
            print("Введите 5 карт ВТОРОГО игрока (числа 0-9 через пробел):")
            k2 = validator_strok(input("> "))
            
            if len(set(k1 + k2)) != 10:
                print("Ошибка: По условию все 10 карт должны быть уникальными (без дубликатов).")
                continue
            return k1, k2
        except ValueError as e:
            print(f"Ошибка ввода: {e} Попробуйте снова.")

def zagruzka_iz_faila():
    print("\nВведите имя файла (например, karty.txt):")
    path = input("> ").strip()
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            
        if len(lines) < 2:
            print("Ошибка формата: В файле должно быть не менее двух непустых строк.")
            return None
            
        k1 = validator_strok(lines[0])
        k2 = validator_strok(lines[1])
        
        if len(set(k1 + k2)) != 10:
            print("Ошибка: Карты в файле содержат дубликаты. Ожидается 10 уникальных карт.")
            return None
            
        print(f"[+] Карты успешно загружены из файла '{path}'")
        return k1, k2
    except FileNotFoundError:
        print(f"Ошибка: Файл '{path}' не найден в директории скрипта.")
    except PermissionError:
        print("Ошибка: Недостаточно прав для чтения указанного файла.")
    except ValueError as e:
        print(f"Ошибка парсинга данных из файла: {e}")
    return None

def random_generaciya():
    vse_karty = list(range(10))
    for i in range(len(vse_karty)):
        j = random.randint(0, 9)
        vse_karty[i], vse_karty[j] = vse_karty[j], vse_karty[i]
    return vse_karty[:5], vse_karty[5:]

def sohranit_rezultat(karty1, karty2, rez, hodov):
    print("\nСохранить протокол игры в файл? (1 — Да, любой другой символ — Нет):")
    vibor = input("> ").strip()
    if vibor != "1":
        return
        
    print("Введите имя файла для сохранения (например, result.txt):")
    path = input("> ").strip()
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("=" * 40 + "\n")
            f.write("        ПРОТОКОЛ ИГРЫ В ПЬЯНИЦУ\n")
            f.write("=" * 40 + "\n")
            f.write(f"Исходная колода Игрока 1: {karty1}\n")
            f.write(f"Исходная колода Игрока 2: {karty2}\n\n")
            if rez == "botva":
                f.write("Результат симуляции: botva\n")
            else:
                f.write(f"Результат симуляции: {rez} {hodov}\n")
        print(f"[+] Файл результатов успешно сохранен в '{path}'")
    except IOError as e:
        print(f"Критическая ошибка записи на диск: {e}")

def main():
    while True:
        print("\n" + "="*45)
        print("         ГЛАВНОЕ МЕНЮ: ИГРА В ПЬЯНИЦУ")
        print("="*45)
        print("1. Ввести начальные карты вручную с клавиатуры")
        print("2. Загрузить конфигурацию колод из файла")
        print("3. Сгенерировать случайный набор карт")
        print("4. Завершить работу программы")
        print("-" * 45)
        
        vibor = input("Выберите пункт меню (1-4): ").strip()
        karty1, karty2 = None, None
        
        if vibor == "1":
            karty1, karty2 = vvod_vruchnuyu()
        elif vibor == "2":
            res = zagruzka_iz_faila()
            if res:
                karty1, karty2 = res
        elif vibor == "3":
            karty1, karty2 = random_generaciya()
            print(f"[+] Игрок 1: {' '.join(map(str, karty1))}")
            print(f"[+] Игрок 2: {' '.join(map(str, karty2))}")
        elif vibor == "4":
            print("\nПрограмма успешно завершена. Спасибо за использование!")
            break
        else:
            print("Неверный ввод! Пожалуйста, выберите число от 1 до 4.")
            continue
            
        if karty1 is not None and karty2 is not None:
            rez, hodov = logic.zapustit_igru(karty1, karty2)
            
            print("\n" + "*"*35)
            if rez == "botva":
                print("ФИНАЛЬНЫЙ ВЫВОД: botva")
            else:
                print(f"ФИНАЛЬНЫЙ ВЫВОД: {rez} {hodov}")
            print("*"*35)
            
            sohranit_rezultat(karty1, karty2, rez, hodov)

if __name__ == "__main__":
    main()
