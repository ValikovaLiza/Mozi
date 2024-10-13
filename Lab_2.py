from collections import Counter
from sympy import mod_inverse
import math
import keyboard

rus_alphabet = 'а б в г д е ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я'.split()
alphabet_size = len(rus_alphabet)

letter_frequencies = {
    'о': 0.090, 'е': 0.072, 'а': 0.062,
    'и': 0.062, 'т': 0.053, 'н': 0.053, 'с': 0.045,
    'р': 0.040, 'в': 0.038, 'л': 0.035, 'к': 0.028,
    'м': 0.026, 'д': 0.025, 'п': 0.023, 'у': 0.021,
    'я': 0.018, 'ы': 0.016, 'з': 0.016, 'ъ': 0.014, 'ь': 0.014,
    'б': 0.014, 'г': 0.013, 'ч': 0.012, 'й': 0.010,
    'х': 0.009, 'ж': 0.007, 'ю': 0.006, 'ш': 0.006,
    'ц': 0.004, 'щ': 0.003, 'э': 0.003, 'ф': 0.002
}


letter_to_num = {letter: idx for idx, letter in enumerate(rus_alphabet)}
num_to_letter = {idx: letter for idx, letter in enumerate(rus_alphabet)}

m=32

def frequency_analysis(text):
    freq = Counter(text)
    total = len(text)
    return {char: count / total for char, count in freq.items()}

def most_frequent(freq_dict, top_n=10, offset=0):
    return sorted(freq_dict, key=freq_dict.get, reverse=True)[offset:offset + top_n]
def most_frequentL(letter_frequencies, top_n=2, offset=0):
    return sorted(letter_frequencies, key=letter_frequencies.get, reverse=True)[offset:offset + top_n]

def decrypt(m, cipher_text, a, b, letter_to_num, num_to_letter):
    a_inv = mod_inverse(a, m)
    decrypted_text = ""
    for char in cipher_text:
        C = letter_to_num[char] 
        P = (a_inv * (C - b)) % m  
        decrypted_text += num_to_letter[P] 
    return decrypted_text

def nod(a, m):
    return math.gcd(a, m)

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    a = a % m
    gcd, x, _ = gcd_extended(a, m)
    if gcd != 1:
        raise ValueError(f"Число {a} не обратимо по модулю {m}")
    return x % m

def solve_linear_congruence(a, b, m):
    gcd = math.gcd(a, m)
    if b % gcd != 0:
        return []  # Пустой список, если решений нет

    a //= gcd
    b //= gcd
    m //= gcd

    x0 = (mod_inverse(a, m) * b) % m

    solutions = []
    for i in range(gcd):  
        solutions.append((x0 + i * m) % (m * gcd))  

    return solutions

def solve2(m, x1, x2, y1, y2):
    diff_x = x1 - x2
    diff_y = y1 - y2
    d = math.gcd(diff_x, m)
    
    if diff_y % d != 0:
        return "Нет решений"  

    reduced_m = m // d
    try:
        inv = mod_inverse(diff_x // d, reduced_m)
    except ValueError:
        return f"Нет обратного элемента для {diff_x // d} по модулю {reduced_m}"

    a_particular = (inv * (diff_y // d)) % reduced_m
    
    all_a_solutions = [(a_particular + i * reduced_m) % m for i in range(d)]

    all_solutions = []
    for a in all_a_solutions:
        b = (y1 - a * x1) % m
        all_solutions.append((a, b))

    return all_solutions


def solve(m, x1, x2, y1, y2):
    d = nod(x1 - x2, m)
    if d % (y1 - y2) != 0:
        return "Нет решения"
    inv = mod_inverse(x1 - x2, m)

    a = ((y1 - y2) * inv) % m
    b = (y1 - a * x1) % m

    return a, b


results = []
print(f"Выберите действие: решение сравнения(1), решение системы сравнений(2), расшифровка(3), обратный элемент(4)")
inp=int(input())
if inp==1:
    print(f"Введите a,b и m")
    a,b,m = map(int, input().split())
    print(f"Решение для {a}x ≡ {b} (mod {m}): x = {solve_linear_congruence(a, b, m)}")
elif inp==2:
    print(f"Введите m, x1, x2, y1, y2")
    m, x1, x2, y1, y2 = map(int, input().split())
    solution = solve2(m, x1, x2, y1, y2)
    print(solution)
    # for a_sol, b_sol in solution:
    #     check1 = (x1 * a_sol + b_sol) % m
    #     check2 = (x2 * a_sol + b_sol) % m
    #     print(f"Проверка: {x1}*{a_sol} + {b_sol} ≡ {check1} (mod {m})")
    #     print(f"Проверка: {x2}*{a_sol} + {b_sol} ≡ {check2} (mod {m})")
elif inp==3:

    cipher_text = 'щгзшмпвжгщгзфвлыоцунпыщумжгфбгъгйвщйртжыпыщщгзъгъвйвпнздтпнунхбгтжфвпдъвйыпгъъдтийвувоыицмлбгщгзъгбмучытънхбгтжщныщцвинбнъцвипйвуво'
    cipher_freq = frequency_analysis(cipher_text)

    most_common_symbols = most_frequent(cipher_freq, top_n=10, offset=0)
    alf = most_frequent(letter_frequencies, top_n=10, offset=0)

    most_common_codes = [letter_to_num[symbol] for symbol in most_common_symbols]
    alf_num = [letter_to_num[symbol] for symbol in alf]

    stop_execution = False  

    for i in range(len(alf_num)):
        for j in range(len(alf_num)):
            if i != j:
                x1, y1 = alf_num[i], most_common_codes[0]
                x2, y2 = alf_num[j], most_common_codes[1]

                try:
                    result = solve(m, x1, x2, y1, y2)
                    if isinstance(result, tuple):
                        a, b = result
                        decrypted_text = decrypt(m, cipher_text, a, b, letter_to_num, num_to_letter)
                        results.append((a, b, decrypted_text[:100]))
                except ValueError:
                    continue

            if stop_execution:
                break

        for index in range(0, len(results), 2):
            for sub_index in range(2):
                if index + sub_index < len(results):
                    a, b, decrypted_text = results[index + sub_index]
                    print(f"Расшифрованный текст с ключом (a = {a}, b = {b}):\n{decrypted_text}\n")

            user_input = input("Нажмите Enter или пробел для продолжения, 'f' для сохранения в файл, или 'r' для прерывания: ").strip().lower()

            if user_input == 'r':
                print("Прерывание вывода...")
                stop_execution = True  
                break  

            if user_input == 'f':
                with open("text2.txt", "w", encoding="utf-8") as file:
                    for sub_index in range(2):
                        if index + sub_index < len(results):
                            a, b, decrypted_text = results[index + sub_index]
                            file.write(f"Ключ (a = {a}, b = {b}):\n{decrypted_text}\n\n")
                print("Результаты сохранены в файл text2.txt")

        if stop_execution:
            break
elif inp == 4:
    print(f"Введите число и модуль")
    a,m = map(int, input().split())
    try:
        inverse = mod_inverse(a, m)
        print(f"Обратный элемент к {a} по модулю {m}: {inverse}")
    except ValueError:
        print("Нет обратного элемента")
    