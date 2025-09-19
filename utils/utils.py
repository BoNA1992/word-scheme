import numpy as np
import cv2
from glob import glob
import matplotlib.pyplot as plt
import re 


consonant_letters = {'Б': 1041, 'В': 1042, 'Г': 1043, 'Д': 1044, 
               'Ж': 1046, 'З': 1047, 'Й': 1049, 'К': 1050, 
               'Л': 1051, 'М': 1052, 'Н': 1053, 'П': 1055, 
               'Р': 1056, 'С': 1057, 'Т': 1058,'Ф': 1060, 
               'Х': 1061, 'Ц': 1062, 'Ч': 1063, 'Ш': 1064, 
               'Щ': 1065
}

vowel_letters = {'А': 1040, 'О': 1054, 'У': 1059, 'Ы': 1067, 'Э': 1069}

vowel_letters_soft = {'Е': 1045, 'И': 1048, 'Ю': 1070, 'Я': 1071, 'Ё': 1025}

hard_and_soft_sign = {'Ъ': 1066, 'Ь': 1068}

blue_red = cv2.imread(glob('./images/blue_red.png')[0])
green_red = cv2.imread(glob('./images/green_red.png')[0])
blue = cv2.imread(glob('./images/blue.png')[0])
red = cv2.imread(glob('./images/red.png')[0])
green = cv2.imread(glob('./images/green.png')[0])

blue_red = cv2.resize(blue_red, (250, 100))
green_red = cv2.resize(green_red, (250, 100))
blue = cv2.resize(blue, (100, 100))
red = cv2.resize(red, (100, 100))
green = cv2.resize(green, (100, 100))


def has_cyrillic(word):
    return bool(re.search('[а-яА-Я]', word))


def get_word_scheme(word: str):
    lst = []
    for i, letter in enumerate(word):
        try:
            if letter in hard_and_soft_sign.keys():
                continue
            elif letter in consonant_letters.keys() and word[i+1] in vowel_letters.keys():
                if ord(letter) == 1063:
                    lst.append(2)
                elif ord(letter) in [1064, 1065] and ord(word[i+1]) == 1059:
                    lst.append(2)
                else:
                    lst.append(0)
            elif letter in consonant_letters.keys() and word[i+1] in vowel_letters_soft.keys():
                if ord(letter) in [1046, 1062, 1064] and ord(word[i+1]) in [1045, 1048]:
                    lst.append(0)
                else: 
                    lst.append(2)
            elif letter in consonant_letters.keys() and word[i+1] in consonant_letters.keys():
                lst.append(0)
            elif letter not in consonant_letters.keys():
                lst.append(1)
            elif letter in consonant_letters.keys() and word[i+1] in hard_and_soft_sign.keys():
                lst.append(0)
        except:
            if letter in consonant_letters.keys() and ord(letter) not in [1063, 1065]:
                lst.append(0)
            elif letter in vowel_letters.keys() or letter in vowel_letters_soft.keys():
                lst.append(1)
    result = get_image_scheme(scheme=lst)
    return result

def get_image_scheme(scheme: list[int]):
    img = []
    for i, x in enumerate(scheme):
        try:
            if x == 0 and scheme[i+1] == 1:
                img.append(blue_red)
            elif x == 2 and scheme[i+1] == 1:
                img.append(green_red)
            elif x == 1 and (scheme[i-1] == 0 or scheme[i-1] == 2):
                if i-1 == -1:
                    img.append(red)
                else:
                    continue
            elif x == 0:
                img.append(blue)
            elif x == 2:
                img.append(green)
            elif x == 1 and i == len(scheme) - 1:
                img.append(red)
            elif x == 1:
                img.append(red)
        except:
            if x == 1:
                img.append(red)
            elif x == 0:
                img.append(blue)
            elif x == 2:
                img.append(green)
    # соединить изображения по горизонтали
    result = cv2.hconcat(img)
    white_img = result * 0 + 255
    result = cv2.vconcat([white_img, result, white_img])
    # преобразовать BGR-изображение в RGB
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    return result

def vis_image_scheme(word, image):
    plt.title(word.upper(), fontsize=50, pad=10)
    plt.xlabel(str(image.shape[1]))
    plt.ylabel(str(image.shape[0]))
    # plt.annotate(text='', xy=(250, 100),  xycoords='data',
    #         xytext=(250, 50), textcoords='data',
    #         arrowprops=dict(facecolor='black', 
    #                         arrowstyle="-", 
    #                         connectionstyle="angle",
    #         )
    # )
    # plt.annotate(text='', xy=(250, 190),  xycoords='data',
    #         xytext=(250, 250), textcoords='data',
    #         arrowprops=dict(facecolor='black', 
    #                         arrowstyle="-", 
    #                         connectionstyle="angle",
    #         )
    # )
    # plt.annotate('min', xy=(250, 100),  xycoords='data',
    #         xytext=(250, 50), textcoords='data',
    #         arrowprops=dict(facecolor='black'))
    plt.imshow(image)

# Отображаем график
    # print(word)
    plt.show()
