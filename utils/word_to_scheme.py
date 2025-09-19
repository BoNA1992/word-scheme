from utils import has_cyrillic, get_word_scheme, vis_image_scheme

while True:
    word = input("Введи слово на русском языке (для выхода введи Q или Й) ")
    if word in 'QqЙй':
        break
    if word.isalpha() == False or has_cyrillic(word) == False:
        print(f'Слово должно состоять только из русских букв, попробуй еще раз')
    else:
        img = get_word_scheme(word.upper())
        result = vis_image_scheme(word=word, image=img)
