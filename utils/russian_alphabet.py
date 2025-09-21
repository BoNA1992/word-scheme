
class RussianAlphabet:
    """Класс для работы с русским алфавитом и категориями букв."""
    
    @staticmethod
    def consonant_letters():
        return {'Б': 1041, 'В': 1042, 'Г': 1043, 'Д': 1044, 
                'З': 1047, 'К': 1050, 'Л': 1051, 'М': 1052, 
                'Н': 1053, 'П': 1055, 'Р': 1056, 'С': 1057, 
                'Т': 1058, 'Ф': 1060, 'Х': 1061}

    @staticmethod
    def consonant_letters_soft():
        return {'Й': 1049, 'Ч': 1063, 'Щ': 1065}

    @staticmethod
    def consonant_letters_hard():
        return {'Ж': 1046, 'Ц': 1062, 'Ш': 1064}

    @staticmethod
    def vowel_letters():
        return {'А': 1040, 'О': 1054, 'У': 1059, 'Ы': 1067, 'Э': 1069}

    @staticmethod
    def vowel_letters_soft():
        return {'Ё': 1025, 'Е': 1045, 'И': 1048, 'Ю': 1070, 'Я': 1071}

    @staticmethod
    def hard_and_soft_sign():
        return {'Ъ': 1066, 'Ь': 1068}

    # Использованием свойств класса, доступ к данным без вызова методов ()
    CONSONANT_LETTERS = consonant_letters.__func__()
    CONSONANT_LETTERS_SOFT = consonant_letters_soft.__func__()
    CONSONANT_LETTERS_HARD = consonant_letters_hard.__func__()
    VOWEL_LETTERS = vowel_letters.__func__()
    VOWEL_LETTERS_SOFT = vowel_letters_soft.__func__()
    HARD_AND_SOFT_SIGN = hard_and_soft_sign.__func__()