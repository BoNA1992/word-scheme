from utils.utils import get_word_scheme, vis_image_scheme, load_dictionary, validate_and_process_word
import random
import os

# Список забавных приглашений
funny_prompts = [
    "🎯 Введи слово на русском языке (для выхода введи Q или Й) ",
    "🔍 Какое слово разберем на запчасти? (Q/Й для выхода) ",
    "🔮 Вижу, у тебя есть слово для меня... Вводи! (Q/Й - прекратить ясновидение) ",
]

def process_and_save_word(word):
    """
    Обрабатывает слово и сохраняет результат с уведомлением
    """
    print(f"🔄 Обрабатываю слово '{word}'...")
    
    # Создаем схему слова
    img = get_word_scheme(word.upper())
    
    # Сохраняем и получаем путь к файлу
    result_path = vis_image_scheme(word=word, image=img)
    
    # Проверяем, что файл действительно сохранился
    if result_path and os.path.exists(result_path):
        file_size = os.path.getsize(result_path)
        save_messages = [
            f"💾 Слово '{word}' сохранено! Файл: {result_path}",
            f"✅ Готово! Схема слова '{word}' записана в {result_path}",
            f"🎉 Ура! Слово '{word}' разобрано и сохранено как {result_path}",
            f"📁 Схема слова '{word}' теперь живет в {result_path}",
            f"🔖 Запомни: схема слова '{word}' ждет тебя в {result_path}",
            f"🏷️ Слово '{word}' архивировано! Место хранения: {result_path}",
            f"📋 Миссия выполнена! Схема слова '{word}' в {result_path}",
            f"🎊 Файл со схемой слова '{word}' создан! Путь: {result_path}"
        ]
        
        print(f"✅ {random.choice(save_messages)}")
        
        # Дополнительное забавное сообщение
        fun_facts = [
            "🐱 Кстати, это слово можно теперь показывать котику!",
            "🌟 Отличная работа! Твое слово теперь в истории!",
            "🍪 Такое достижение стоит печеньки!",
            "📚 Коллекция схем слов пополняется!",
            "🤓 Теперь ты знаешь это слово лучше других!",
        ]
        print(f"💡 {random.choice(fun_facts)}")
        
    else:
        print(f"❌ Упс! Не удалось сохранить схему слова '{word}'. Попробуй еще раз!")
    
    return result_path

dictionary = load_dictionary("/workspaces/word-scheme/russian-words/russian.txt")
if not dictionary:
    print("❌ Не удалось загрузить словарь. Буду проверять слова по памяти... а она у меня, как у золотой рыбки!")

# Счетчик обработанных слов
word_count = 0

while True:
    # Случайный выбор забавного приглашения
    word = input(f"\n{random.choice(funny_prompts)}")
    
    result = validate_and_process_word(word, dictionary)
    
    if result == "exit":
        print(f"👋 Пока-пока! Обработано слов: {word_count}. Возвращайся с новыми словами!")
        break
    elif result == "not_in_dict":
        print(f"🤔 Слово '{word}' не найдено в словаре. Возможно оно введено с ошибкой, а возможно, ты изобрел новое слово!")
        choice = input("💡 Введите 1 для продолжения с этим словом (на свой страх и риск!) или новое слово для проверки: ")
        
        if choice == '1':
            print("🚀 Запускаю обработку! Надеюсь, твое слово не взорвет программу!")
            process_and_save_word(word)
            word_count += 1
        elif choice == word:
            print(f"😲 Опять '{choice}'? Ты настойчив! Так уж и быть! Запускаю обработку!🚀")
            process_and_save_word(word)
            word_count += 1
        elif choice in 'QqЙй':
            print(f"👋 Пока-пока! Обработано слов: {word_count}. Возвращайся с новыми словами!")
            break
        else:
            print(f"🔍 Проверяю новое слово: '{choice}'")
            # Используем новое слово для дальнейшей обработки
            word = choice
            new_result = validate_and_process_word(word, dictionary)
            
            if new_result == "exit":
                print(f"👋 Выходим! Обработано слов: {word_count}. До встречи!")
                break
            elif new_result == "not_in_dict":
                print("😅 И это слово не найдено! Может, попробуем что-то из классики? Например, 'котик' или 'печенька'?")
                continue
            else:
                # Слово прошло проверку
                process_and_save_word(word)
                word_count += 1
    elif result == "invalid":
        continue
    else:
        # Слово прошло проверку
        process_and_save_word(word)
        word_count += 1

    # Показываем прогресс каждые 5 слов
    if word_count % 5 == 0:
        progress_messages = [
            f"🎊 Поздравляю! Ты обработал уже {word_count} слов!",
            f"📈 Отличный темп! Уже {word_count} слов в коллекции!",
            f"🌟 Целая коллекция из {word_count} слов! Ты просто словознайка!",
            f"🏆 {word_count} слов разобрано! Ты на пути к мастерству!",
            f"📚 Уже {word_count} слов в твоей библиотеке схем!"
        ]
        print(f"\n🎯 {random.choice(progress_messages)}")
