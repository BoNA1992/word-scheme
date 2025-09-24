import numpy as np
import cv2
from glob import glob
import matplotlib.pyplot as plt
import re 
import os
from utils.russian_alphabet import RussianAlphabet
from utils.image_loader import ImageLoader

loader = ImageLoader('./images')
images = loader.load_images()

# Доступ к изображениям
blue_red = images['blue_red']
green_red = images['green_red']
blue = images['blue']
red = images['red']
green = images['green']


def create_folder(folder_path):
    """
    Создает папку по указанному пути относительно текущей директории
    и возвращает полный абсолютный путь к созданной папке.
    
    Args:
        folder_path (str): Путь к папке (например, "./result")
    
    Returns:
        str: Абсолютный путь к созданной папке
    """
    # Получаем абсолютный путь
    absolute_path = os.path.abspath(folder_path)
    
    # Создаем папку, если она не существует
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)
        # print(f"Папка '{absolute_path}' успешно создана")
    # else:
        # print(f"Папка '{absolute_path}' уже существует")
    
    return absolute_path


def is_all_cyrillic(word: str):
    """
    Проверяет, состоит ли строка полностью из кириллических символов.
    
    Args:
        text (str): Строка для проверки
    
    Returns:
        bool: True если строка состоит только из кириллических символов, иначе False
     """
    if not word:  # Проверка на пустую строку
        return False
    
    # Проверяем, что все символы соответствуют кириллическому диапазону
    return bool(re.fullmatch(r'[а-яА-ЯёЁ]+', word))


def get_word_scheme(word: str):
    """
    Проходимся по слову и присваеваем метку букве:
    0 - Ъ или Ь знак
    1 - согласная буква - Б, В, Г, Д, З, К, Л, М, Н, П, Р, С, Т, Ф, Х
    2 - согласные всегда мягкие - Й, Ч, Щ
    3 - согласные всегда твердые - Ж, Ц, Ш
    4 - гласные - А, О, У, Ы, Э
    5 - гласные - Е, Ё, И, Ю, Я
    """
    result = []
    for i, letter in enumerate(word):
        if letter in RussianAlphabet.HARD_AND_SOFT_SIGN:
            result.append(0)
        elif letter in RussianAlphabet.CONSONANT_LETTERS:
            result.append(1)
        elif letter in RussianAlphabet.CONSONANT_LETTERS_SOFT:
            result.append(2)
        elif letter in RussianAlphabet.CONSONANT_LETTERS_HARD:
            result.append(3)        
        elif letter in RussianAlphabet.VOWEL_LETTERS:
            result.append(4)        
        elif letter in RussianAlphabet.VOWEL_LETTERS_SOFT:
            result.append(5)  
    result = get_image_scheme(scheme=result) 
    return result


def get_image_scheme(scheme: list[int]):
    """Проходимся по слову и присваеваем метку букве:
    # 0 - Ъ или Ь знак
    # 1 - согласная буква - Б, В, Г, Д, З, К, Л, М, Н, П, Р, С, Т, Ф, Х
    # 2 - согласные всегда мягкие - Й, Ч, Щ
    # 3 - согласные всегда твердые - Ж, Ц, Ш
    # 4 - гласные - А, О, У, Ы, Э
    # 5 - гласные - Е, Ё, И, Ю, Я
    """
    img = []
    skip_next = False
    for i, x in enumerate(scheme):
        if skip_next or x == 0:
            skip_next = False
            continue
        # print('i', i)
        try:
            if x == 1:
                if scheme[i+1] == 4:
                    img.append(blue_red)
                    skip_next = True
                elif scheme[i+1] == 5:
                    img.append(green_red)
                    skip_next = True
                elif scheme[i+1] in [0, 1, 2, 3]:
                    img.append(blue)
            elif x == 2:
                if scheme[i+1] in [4, 5]:
                    img.append(green_red)
                    skip_next = True
                elif scheme[i+1] in [0, 1, 2, 3]:
                    img.append(green)
            elif x == 3:
                if scheme[i+1] in [4, 5]:
                    img.append(blue_red)
                    skip_next = True
                elif scheme[i+1] in [0, 1, 2, 3]:
                    img.append(blue)
            elif x == 4:
                img.append(red)
            elif x == 5:
                if i == 0 or scheme[i-1] in [0, 4, 5]:
                    img.append(green_red)
                else:
                    img.append(red)
        except:
            if x == 0:
                continue
            if x == 1:
                img.append(blue)
            elif x == 2:
                img.append(green)
            elif x == 3:
                img.append(blue)
            elif x == 4:
                img.append(red)
            # elif x == 5:
            #     img.append(red)
    # соединить изображения по горизонтали
    result = cv2.hconcat(img)
    white_img = result * 0 + 255
    result = cv2.vconcat([white_img, result, white_img])
    # преобразовать BGR-изображение в RGB
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return result

def vis_image_scheme(word, image):
    save_path = f"{create_folder("./result")}/{word}.png"
    plt.title(word.upper(), fontsize=50, pad=10)
    plt.axis('off')
    plt.imshow(image)
    plt.savefig(save_path)

    # Отображаем график для Jupyter Notebook
    plt.show()
    return save_path


def load_dictionary(dictionary_path, encoding='windows-1251'):
    """
    Загружает словарь из файла в множество для многократного использования
    
    Args:
        dictionary_path (str): Путь к файлу словаря
        encoding (str): Кодировка файла
    
    Returns:
        set: Множество слов из словаря или пустое множество при ошибке
    """
    try:
        with open(dictionary_path, 'r', encoding=encoding) as file:
            words = set()
            for line in file:
                word = line.strip().lower()
                if word:  # Пропускаем пустые строки
                    words.add(word)
            return words
    except FileNotFoundError:
        print(f"Ошибка: Файл словаря '{dictionary_path}' не найден")
        return set()
    except Exception as e:
        print(f"Ошибка при загрузке словаря: {e}")
        return set()


def process_word(word):
    """Обрабатывает слово: создает схему и визуализирует ее"""
    img = get_word_scheme(word.upper())
    result = vis_image_scheme(word=word, image=img)
    return result


def validate_and_process_word(word, dictionary):
    """Проверяет слово и обрабатывает его если оно корректно"""
    # Проверка на выход
    if word in 'QqЙй':
        return "exit"
    
    # Проверка на корректность ввода
    if not word.isalpha() or not is_all_cyrillic(word):
        print(f'Слово должно состоять только из русских букв (без пробелов и знаков препинания), попробуй еще раз')
        return "invalid"
    
    # Проверка наличия в словаре
    if word.lower() in dictionary:
        process_word(word)
        return "processed"
    else:
        # print(f"Слово '{word}' не найдено в словаре.")
        return "not_in_dict"