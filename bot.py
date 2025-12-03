import telebot
import json
import os
from telebot import types

# Замените на ваш токен от @BotFather
API_TOKEN = '8577124617:AAFwIzF4vSHLcYnW-WmDjA7V51zlku549To'

# Создаем бота
bot = telebot.TeleBot(API_TOKEN)

# Файл для хранения книг
BOOKS_FILE = 'books.json'

# Загружаем книги из файла
def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Сохраняем книги в файл
def save_books(books):
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

# Словарь для хранения состояния пользователей
user_states = {}

# Функция для отображения звезд рейтинга
def get_stars_rating(rating):
    stars = {
        1: "⭐",
        2: "⭐⭐", 
        3: "⭐⭐⭐",
        4: "⭐⭐⭐⭐",
        5: "⭐⭐⭐⭐⭐"
    }
    return stars.get(rating, "Без оценки")

# Создание главного меню с кнопками
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('📚 Добавить книгу')
    btn2 = types.KeyboardButton('🔍 Поиск книги')
    btn3 = types.KeyboardButton('📖 Мои книги')
    btn4 = types.KeyboardButton('✏️ Редактировать')
    btn5 = types.KeyboardButton('⭐ Оценить книгу')
    btn6 = types.KeyboardButton('ℹ️ Помощь')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

# Создание меню отмены
def create_cancel_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('❌ Отмена')
    markup.add(btn)
    return markup

# Создание меню выбора рейтинга
def create_rating_menu():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btn1 = types.KeyboardButton('⭐')
    btn2 = types.KeyboardButton('⭐⭐')
    btn3 = types.KeyboardButton('⭐⭐⭐')
    btn4 = types.KeyboardButton('⭐⭐⭐⭐')
    btn5 = types.KeyboardButton('⭐⭐⭐⭐⭐')
    btn6 = types.KeyboardButton('➡️ Пропустить')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

# Создание меню пропуска
def create_skip_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('➡️ Пропустить')
    markup.add(btn1)
    return markup

# Создание меню действий с книгой (с выходом в главное меню)
def create_book_actions_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('✏️ Редактировать')
    btn2 = types.KeyboardButton('🗑️ Удалить')
    btn3 = types.KeyboardButton('⭐ Оценить')
    btn4 = types.KeyboardButton('📖 Подробнее')
    btn5 = types.KeyboardButton('🔙 Назад')
    btn6 = types.KeyboardButton('➡️ Вперед')
    btn7 = types.KeyboardButton('🏠 В главное меню')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup

# Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    text = """
📚 Привет! Я бот-библиотекарь.

Выбери действие с помощью кнопок ниже:
    """
    bot.send_message(message.chat.id, text, reply_markup=create_main_menu())

# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
ℹ️ **ПОМОЩЬ - Все доступные действия:**

📚 **Добавить книгу** - добавить новую книгу в библиотеку
_Обязательные поля: автор, название_
_Необязательные: жанр, описание, комментарий, оценка_

🔍 **Поиск книги** - найти книгу по автору, названию или жанру
_Показываю краткую информацию с навигацией_

📖 **Мои книги** - посмотреть все твои книги списком
_Краткий формат: автор - название_

✏️ **Редактировать** - изменить информацию о любой книге
_Можно редактировать все поля по отдельности_

⭐ **Оценить книгу** - поставить оценку от 1 до 5 звезд
_Можно пропустить или изменить позже_

🗑️ **Удалить** - удалить книгу из библиотеки

🔍 **В поиске:**
- ✏️ Редактировать - изменить книгу
- 🗑️ Удалить - удалить книгу  
- ⭐ Оценить - поставить оценку
- 📖 Подробнее - полная информация
- 🔙/➡️ Навигация по результатам
- 🏠 В главное меню - выйти из поиска
    """
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=create_main_menu())

# Обработка кнопки "Добавить книгу"
@bot.message_handler(func=lambda message: message.text == '📚 Добавить книгу')
def add_book_button(message):
    chat_id = message.chat.id
    user_states[chat_id] = {
        'step': 'author',
        'book_data': {},
        'action': 'add'
    }
    bot.send_message(chat_id, "Давай добавим книгу! Введи автора:", reply_markup=create_cancel_menu())

# Обработка кнопки "Поиск книги"
@bot.message_handler(func=lambda message: message.text == '🔍 Поиск книги')
def search_button(message):
    chat_id = message.chat.id
    user_states[chat_id] = {'step': 'search'}
    bot.send_message(chat_id, "Введи название книги, автора или жанр для поиска:", reply_markup=create_cancel_menu())

# Обработка кнопки "Мои книги"
@bot.message_handler(func=lambda message: message.text == '📖 Мои книги')
def my_books_button(message):
    chat_id = message.chat.id
    books = load_books()
    user_books = books.get(str(chat_id), [])
    
    if not user_books:
        bot.send_message(chat_id, "📭 У тебя пока нет книг в библиотеке.", reply_markup=create_main_menu())
        return
    
    text = f"📚 Твои книги (всего: {len(user_books)}):\n\n"
    for i, book in enumerate(user_books, 1):
        text += f"{i}. **{book['title']}** - {book['author']}\n"
    
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_main_menu())

# Обработка кнопки "Редактировать"
@bot.message_handler(func=lambda message: message.text == '✏️ Редактировать')
def edit_book_button(message):
    chat_id = message.chat.id
    books = load_books()
    user_books = books.get(str(chat_id), [])
    
    if not user_books:
        bot.send_message(chat_id, "📭 У тебя нет книг для редактирования.", reply_markup=create_main_menu())
        return
    
    # Показываем список книг для редактирования
    text = "📚 Выбери книгу для редактирования:\n\n"
    for i, book in enumerate(user_books, 1):
        text += f"{i}. **{book['title']}** - {book['author']}\n"
    
    text += "\nВведи номер книги:"
    
    user_states[chat_id] = {
        'step': 'select_edit',
        'books_list': user_books
    }
    
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_cancel_menu())

# Обработка кнопки "Оценить книгу"
@bot.message_handler(func=lambda message: message.text == '⭐ Оценить книгу')
def rate_book_button(message):
    chat_id = message.chat.id
    books = load_books()
    user_books = books.get(str(chat_id), [])
    
    if not user_books:
        bot.send_message(chat_id, "📭 У тебя нет книг для оценки.", reply_markup=create_main_menu())
        return
    
    # Показываем список книг для оценки
    text = "📚 Выбери книгу для оценки:\n\n"
    for i, book in enumerate(user_books, 1):
        current_rating = book.get('rating', 0)
        stars = get_stars_rating(current_rating)
        text += f"{i}. **{book['title']}** - {book['author']} ({stars})\n"
    
    text += "\nВведи номер книги:"
    
    user_states[chat_id] = {
        'step': 'select_rate',
        'books_list': user_books
    }
    
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_cancel_menu())

# Обработка кнопки "Помощь"
@bot.message_handler(func=lambda message: message.text == 'ℹ️ Помощь')
def help_button(message):
    help_command(message)

# Обработка кнопки "В главное меню"
@bot.message_handler(func=lambda message: message.text == '🏠 В главное меню')
def main_menu_button(message):
    chat_id = message.chat.id
    if chat_id in user_states:
        del user_states[chat_id]
    bot.send_message(chat_id, "🏠 Возвращаю в главное меню.", reply_markup=create_main_menu())

# Обработка кнопки "Отмена"
@bot.message_handler(func=lambda message: message.text == '❌ Отмена')
def cancel_button(message):
    chat_id = message.chat.id
    if chat_id in user_states:
        del user_states[chat_id]
    bot.send_message(chat_id, "❌ Действие отменено.", reply_markup=create_main_menu())

# Обработка всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    user_text = message.text
    
    # Если пользователь в процессе добавления/редактирования книги
    if chat_id in user_states and user_states[chat_id]['step'] in ['author', 'title', 'genre', 'description', 'comment', 'rating']:
        handle_book_flow(chat_id, user_text)
        return
    
    # Если пользователь в процессе поиска
    if chat_id in user_states and user_states[chat_id]['step'] == 'search':
        handle_search_flow(chat_id, user_text)
        return
    
    # Если пользователь выбирает книгу для редактирования
    if chat_id in user_states and user_states[chat_id]['step'] == 'select_edit':
        handle_select_edit_flow(chat_id, user_text)
        return
    
    # Если пользователь выбирает книгу для оценки
    if chat_id in user_states and user_states[chat_id]['step'] == 'select_rate':
        handle_select_rate_flow(chat_id, user_text)
        return
    
    # Если пользователь выбирает рейтинг
    if chat_id in user_states and user_states[chat_id]['step'] == 'select_rating':
        handle_select_rating_flow(chat_id, user_text)
        return
    
    # Если пользователь выбирает поле для редактирования
    if chat_id in user_states and user_states[chat_id]['step'] == 'select_field':
        handle_select_field_flow(chat_id, user_text)
        return
    
    # Если пользователь работает с найденной книгой
    if chat_id in user_states and user_states[chat_id]['step'] == 'book_actions':
        handle_book_actions_flow(chat_id, user_text)
        return
    
    # Если сообщение не распознано, показываем меню
    bot.send_message(chat_id, "Выбери действие с помощью кнопок:", reply_markup=create_main_menu())

# Обработка добавления/редактирования книги
def handle_book_flow(chat_id, user_text):
    state = user_states[chat_id]
    step = state['step']
    book_data = state['book_data']
    
    # Проверяем, что сообщение не пустое и не отмена
    if not user_text or user_text.strip() == '':
        bot.send_message(chat_id, "❌ Пожалуйста, введи текст или используй кнопки.", reply_markup=create_cancel_menu())
        return
    
    if user_text == '❌ Отмена':
        cancel_button({'chat': {'id': chat_id}})
        return
    
    # Шаги процесса добавления/редактирования книги
    if step == 'author':
        book_data['author'] = user_text
        state['step'] = 'title'
        bot.send_message(chat_id, "Отлично! Теперь введи название книги:", reply_markup=create_cancel_menu())
    
    elif step == 'title':
        book_data['title'] = user_text
        state['step'] = 'genre'
        bot.send_message(chat_id, "Хорошо! Теперь введи жанр книги (или нажми 'Пропустить'):", reply_markup=create_skip_menu())
    
    elif step == 'genre':
        if user_text == '➡️ Пропустить':
            book_data['genre'] = "Не указан"
        else:
            book_data['genre'] = user_text
        state['step'] = 'description'
        bot.send_message(chat_id, "Теперь введи описание книги (или нажми 'Пропустить'):", reply_markup=create_skip_menu())
    
    elif step == 'description':
        if user_text == '➡️ Пропустить':
            book_data['description'] = "Нет описания"
        else:
            book_data['description'] = user_text
        state['step'] = 'comment'
        bot.send_message(chat_id, "Теперь введи твой комментарий к книге (или нажми 'Пропустить'):", reply_markup=create_skip_menu())
    
    elif step == 'comment':
        if user_text == '➡️ Пропустить':
            book_data['comment'] = "Нет комментария"
        else:
            book_data['comment'] = user_text
        state['step'] = 'rating'
        bot.send_message(chat_id, "Теперь оцени книгу от 1 до 5 звезд (или нажми 'Пропустить'):", reply_markup=create_rating_menu())
    
    elif step == 'rating':
        # Обработка оценки
        rating_map = {
            '⭐': 1,
            '⭐⭐': 2,
            '⭐⭐⭐': 3,
            '⭐⭐⭐⭐': 4,
            '⭐⭐⭐⭐⭐ 5': 5,
            '➡️ Пропустить': 0
        }
        
        if user_text in rating_map:
            book_data['rating'] = rating_map[user_text]
            
            # Завершаем процесс добавления/редактирования
            complete_book_process(chat_id)
        else:
            bot.send_message(chat_id, "❌ Пожалуйста, выбери оценку из предложенных вариантов.", reply_markup=create_rating_menu())

# Завершение процесса добавления/редактирования книги
def complete_book_process(chat_id):
    state = user_states[chat_id]
    book_data = state['book_data']
    
    # Проверяем обязательные поля
    if 'author' not in book_data or not book_data['author']:
        bot.send_message(chat_id, "❌ Ошибка: автор не указан.", reply_markup=create_main_menu())
        del user_states[chat_id]
        return
    
    if 'title' not in book_data or not book_data['title']:
        bot.send_message(chat_id, "❌ Ошибка: название не указано.", reply_markup=create_main_menu())
        del user_states[chat_id]
        return
    
    books = load_books()
    if str(chat_id) not in books:
        books[str(chat_id)] = []
    
    rating = book_data.get('rating', 0)
    stars = get_stars_rating(rating)
    
    if state['action'] == 'add':
        books[str(chat_id)].append(book_data)
        result_text = f"""
✅ Книга добавлена!

📖 **Название:** {book_data['title']}
👤 **Автор:** {book_data['author']}
🎭 **Жанр:** {book_data.get('genre', 'Не указан')}
📄 **Описание:** {book_data.get('description', 'Нет описания')}
💭 **Комментарий:** {book_data.get('comment', 'Нет комментария')}
⭐ **Оценка:** {stars}
        """
    else:
        # Редактирование существующей книги
        book_index = state['book_index']
        books[str(chat_id)][book_index] = book_data
        result_text = f"""
✏️ Книга обновлена!

📖 **Название:** {book_data['title']}
👤 **Автор:** {book_data['author']}
🎭 **Жанр:** {book_data.get('genre', 'Не указан')}
📄 **Описание:** {book_data.get('description', 'Нет описания')}
💭 **Комментарий:** {book_data.get('comment', 'Нет комментария')}
⭐ **Оценка:** {stars}
        """
    
    save_books(books)
    
    # Возвращаемся к поиску если нужно
    if state.get('return_to_search'):
        search_state = state.get('search_state')
        if search_state:
            user_states[chat_id] = search_state
            show_book_card(chat_id, search_state['current_book_index'])
        else:
            bot.send_message(chat_id, result_text, parse_mode='Markdown', reply_markup=create_main_menu())
            del user_states[chat_id]
    else:
        bot.send_message(chat_id, result_text, parse_mode='Markdown', reply_markup=create_main_menu())
        del user_states[chat_id]

# Обработка поиска
def handle_search_flow(chat_id, user_text):
    # Проверка на пустой запрос
    if not user_text or user_text.strip() == '' or user_text == '❌ Отмена':
        bot.send_message(chat_id, "❌ Поиск отменён.", reply_markup=create_main_menu())
        if chat_id in user_states:
            del user_states[chat_id]
        return
    
    search_query = user_text.lower()
    books = load_books()
    user_books = books.get(str(chat_id), [])
    
    if not user_books:
        bot.send_message(chat_id, "📭 У тебя пока нет книг в библиотеке.", reply_markup=create_main_menu())
        if chat_id in user_states:
            del user_states[chat_id]
        return
    
    # Ищем книги
    found_books = []
    for book in user_books:
        if (search_query in book['title'].lower() or 
            search_query in book['author'].lower() or
            search_query in book.get('genre', '').lower() or
            search_query in book.get('description', '').lower() or
            search_query in book.get('comment', '').lower()):
            found_books.append(book)
    
    if found_books:
        user_states[chat_id] = {
            'step': 'book_actions',
            'found_books': found_books,
            'current_book_index': 0
        }
        show_book_card(chat_id, 0)
    else:
        bot.send_message(chat_id, "❌ Книги по твоему запросу не найдены.", reply_markup=create_main_menu())
        if chat_id in user_states:
            del user_states[chat_id]

# Показать карточку книги (краткая информация)
def show_book_card(chat_id, book_index):
    state = user_states.get(chat_id)
    if not state:
        return
    
    book = state['found_books'][book_index]
    total_books = len(state['found_books'])
    
    rating = book.get('rating', 0)
    stars = get_stars_rating(rating)
    
    text = f"""
📚 Книга {book_index + 1} из {total_books}:

📖 **{book['title']}**
👤 **{book['author']}**
⭐ **{stars}**

Выбери действие:
    """
    
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_book_actions_menu())

# Показать детали книги (полная информация)
def show_book_details(chat_id, book_index):
    state = user_states.get(chat_id)
    if not state:
        return
    
    book = state['found_books'][book_index]
    total_books = len(state['found_books'])
    
    rating = book.get('rating', 0)
    stars = get_stars_rating(rating)
    
    text = f"""
📚 Книга {book_index + 1} из {total_books}:

📖 **Название:** {book['title']}
👤 **Автор:** {book['author']}
🎭 **Жанр:** {book.get('genre', 'Не указан')}
📄 **Описание:** {book.get('description', 'Нет описания')}
💭 **Комментарий:** {book.get('comment', 'Нет комментария')}
⭐ **Оценка:** {stars}
    """
    
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_book_actions_menu())

# Обработка действий с книгой
def handle_book_actions_flow(chat_id, user_text):
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "❌ Сессия истекла. Начни заново.", reply_markup=create_main_menu())
        return
    
    current_index = state['current_book_index']
    current_book = state['found_books'][current_index]
    
    if user_text == '✏️ Редактировать':
        # Начинаем редактирование найденной книги
        books = load_books()
        user_books = books.get(str(chat_id), [])
        
        # Находим индекс книги в основном списке
        book_found = False
        for i, book in enumerate(user_books):
            if (book['title'] == current_book['title'] and 
                book['author'] == current_book['author']):
                user_states[chat_id] = {
                    'step': 'select_field',
                    'book_data': book.copy(),
                    'book_index': i,
                    'return_to_search': True,
                    'search_state': state
                }
                
                rating = book.get('rating', 0)
                stars = get_stars_rating(rating)
                
                text = f"""
✏️ Редактирование книги:

**{book['title']}** - {book['author']}
Текущая оценка: {stars}

Выбери поле для редактирования:
1. Автор
2. Название  
3. Жанр
4. Описание
5. Комментарий
6. Оценка

Введи номер поля:
                """
                bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_cancel_menu())
                book_found = True
                break
        
        if not book_found:
            bot.send_message(chat_id, "❌ Ошибка: книга не найдена в твоей библиотеке.", reply_markup=create_book_actions_menu())
    
    elif user_text == '🗑️ Удалить':
        # Удаляем книгу
        books = load_books()
        user_books = books.get(str(chat_id), [])
        
        for i, book in enumerate(user_books):
            if (book['title'] == current_book['title'] and 
                book['author'] == current_book['author']):
                deleted_book = user_books.pop(i)
                books[str(chat_id)] = user_books
                save_books(books)
                
                # Обновляем список найденных книг
                state['found_books'].pop(current_index)
                if state['found_books']:
                    if current_index >= len(state['found_books']):
                        state['current_book_index'] = len(state['found_books']) - 1
                    show_book_card(chat_id, state['current_book_index'])
                else:
                    bot.send_message(chat_id, 
                                   f"🗑️ Книга удалена:\n**{deleted_book['title']}** - {deleted_book['author']}\n\n📭 Больше книг по запросу не найдено.",
                                   parse_mode='Markdown', reply_markup=create_main_menu())
                    del user_states[chat_id]
                return
    
    elif user_text == '⭐ Оценить':
        # Оцениваем книгу
        books = load_books()
        user_books = books.get(str(chat_id), [])
        
        for i, book in enumerate(user_books):
            if (book['title'] == current_book['title'] and 
                book['author'] == current_book['author']):
                user_states[chat_id] = {
                    'step': 'select_rating',
                    'book_data': book,
                    'book_index': i,
                    'return_to_search': True,
                    'search_state': state
                }
                current_rating = book.get('rating', 0)
                stars = get_stars_rating(current_rating)
                bot.send_message(chat_id, 
                               f"Выбери оценку для книги:\n**{book['title']}**\nТекущая оценка: {stars}",
                               parse_mode='Markdown', reply_markup=create_rating_menu())
                return
    
    elif user_text == '📖 Подробнее':
        # Показываем детали
        show_book_details(chat_id, current_index)
    
    elif user_text == '🔙 Назад':
        # Возвращаемся к предыдущей книге
        if current_index > 0:
            state['current_book_index'] = current_index - 1
            show_book_card(chat_id, current_index - 1)
        else:
            bot.send_message(chat_id, "Это первая книга в списке.", reply_markup=create_book_actions_menu())
    
    elif user_text == '➡️ Вперед':
        # Переход к следующей книге
        new_index = current_index + 1
        if new_index < len(state['found_books']):
            state['current_book_index'] = new_index
            show_book_card(chat_id, new_index)
        else:
            bot.send_message(chat_id, "Это последняя книга в списке.", reply_markup=create_book_actions_menu())
    
    elif user_text == '🏠 В главное меню':
        # Выходим в главное меню
        del user_states[chat_id]
        bot.send_message(chat_id, "🏠 Возвращаю в главное меню.", reply_markup=create_main_menu())
    
    else:
        bot.send_message(chat_id, "❌ Неизвестная команда.", reply_markup=create_book_actions_menu())

# Обработка выбора книги для редактирования
def handle_select_edit_flow(chat_id, user_text):
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "❌ Сессия истекла. Начни заново.", reply_markup=create_main_menu())
        return
    
    books_list = state['books_list']
    
    try:
        book_number = int(user_text)
        if 1 <= book_number <= len(books_list):
            selected_book = books_list[book_number - 1]
            
            # Находим книгу в основном списке
            books = load_books()
            user_books = books.get(str(chat_id), [])
            
            for i, book in enumerate(user_books):
                if (book['title'] == selected_book['title'] and 
                    book['author'] == selected_book['author']):
                    
                    user_states[chat_id] = {
                        'step': 'select_field',
                        'book_data': book.copy(),
                        'book_index': i
                    }
                    
                    rating = book.get('rating', 0)
                    stars = get_stars_rating(rating)
                    
                    text = f"""
✏️ Редактирование книги:

**{book['title']}** - {book['author']}
Текущая оценка: {stars}

Выбери поле для редактирования:
1. Автор
2. Название  
3. Жанр
4. Описание
5. Комментарий
6. Оценка

Введи номер поля:
                    """
                    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=create_cancel_menu())
                    return
            
            bot.send_message(chat_id, "❌ Ошибка: книга не найдена.", reply_markup=create_main_menu())
        else:
            bot.send_message(chat_id, f"❌ Неверный номер. Введи число от 1 до {len(books_list)}", reply_markup=create_cancel_menu())
    except ValueError:
        bot.send_message(chat_id, "❌ Пожалуйста, введи номер книги (число).", reply_markup=create_cancel_menu())

# Обработка выбора книги для оценки
def handle_select_rate_flow(chat_id, user_text):
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "❌ Сессия истекла. Начни заново.", reply_markup=create_main_menu())
        return
    
    books_list = state['books_list']
    
    try:
        book_number = int(user_text)
        if 1 <= book_number <= len(books_list):
            selected_book = books_list[book_number - 1]
            
            # Находим книгу в основном списке
            books = load_books()
            user_books = books.get(str(chat_id), [])
            
            for i, book in enumerate(user_books):
                if (book['title'] == selected_book['title'] and 
                    book['author'] == selected_book['author']):
                    
                    user_states[chat_id] = {
                        'step': 'select_rating',
                        'book_data': book,
                        'book_index': i
                    }
                    
                    current_rating = book.get('rating', 0)
                    stars = get_stars_rating(current_rating)
                    
                    bot.send_message(chat_id, 
                                   f"Выбери оценку для книги:\n**{book['title']}** - {book['author']}\nТекущая оценка: {stars}",
                                   parse_mode='Markdown', reply_markup=create_rating_menu())
                    return
            
            bot.send_message(chat_id, "❌ Ошибка: книга не найдена.", reply_markup=create_main_menu())
        else:
            bot.send_message(chat_id, f"❌ Неверный номер. Введи число от 1 до {len(books_list)}", reply_markup=create_cancel_menu())
    except ValueError:
        bot.send_message(chat_id, "❌ Пожалуйста, введи номер книги (число).", reply_markup=create_cancel_menu())

# Обработка выбора рейтинга
def handle_select_rating_flow(chat_id, user_text):
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "❌ Сессия истекла. Начни заново.", reply_markup=create_main_menu())
        return
    
    book_data = state['book_data']
    book_index = state['book_index']
    
    rating_map = {
        '⭐': 1,
        '⭐⭐': 2,
        '⭐⭐⭐': 3,
        '⭐⭐⭐⭐': 4,
        '⭐⭐⭐⭐⭐': 5,
        '➡️ Пропустить': 0
    }
    
    if user_text not in rating_map:
        bot.send_message(chat_id, "❌ Пожалуйста, выбери оценку из предложенных вариантов.", reply_markup=create_rating_menu())
        return
    
    new_rating = rating_map[user_text]
    
    # Обновляем рейтинг в базе данных
    books = load_books()
    user_books = books.get(str(chat_id), [])
    user_books[book_index]['rating'] = new_rating
    save_books(books)
    
    stars = get_stars_rating(new_rating)
    
    if new_rating == 0:
        message_text = f"✅ Оценка убрана!\n**{book_data['title']}**"
    else:
        message_text = f"✅ Оценка обновлена!\n**{book_data['title']}**\nНовая оценка: {stars}"
    
    # Возвращаемся к поиску если нужно
    if state.get('return_to_search'):
        search_state = state.get('search_state')
        if search_state:
            user_states[chat_id] = search_state
            show_book_card(chat_id, search_state['current_book_index'])
        else:
            bot.send_message(chat_id, message_text, parse_mode='Markdown', reply_markup=create_main_menu())
            del user_states[chat_id]
    else:
        bot.send_message(chat_id, message_text, parse_mode='Markdown', reply_markup=create_main_menu())
        del user_states[chat_id]

# Обработка выбора поля для редактирования
def handle_select_field_flow(chat_id, user_text):
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "❌ Сессия истекла. Начни заново.", reply_markup=create_main_menu())
        return
    
    field_map = {
        '1': {'step': 'author', 'message': 'Введи нового автора:'},
        '2': {'step': 'title', 'message': 'Введи новое название:'},
        '3': {'step': 'genre', 'message': 'Введи новый жанр (или нажми "Пропустить"):', 'menu': create_skip_menu},
        '4': {'step': 'description', 'message': 'Введи новое описание (или нажми "Пропустить"):', 'menu': create_skip_menu},
        '5': {'step': 'comment', 'message': 'Введи новый комментарий (или нажми "Пропустить"):', 'menu': create_skip_menu},
        '6': {'step': 'rating', 'message': 'Выбери новую оценку (или нажми "Пропустить"):', 'menu': create_rating_menu}
    }
    
    if user_text not in field_map:
        bot.send_message(chat_id, "❌ Неверный номер поля. Введи число от 1 до 6", reply_markup=create_cancel_menu())
        return
    
    field_info = field_map[user_text]
    state['step'] = field_info['step']
    state['action'] = 'edit'
    
    if 'menu' in field_info:
        bot.send_message(chat_id, field_info['message'], reply_markup=field_info['menu']())
    else:
        bot.send_message(chat_id, field_info['message'], reply_markup=create_cancel_menu())

# Запуск бота
if __name__ == '__main__':
    print("Бот с исправлениями запущен...")
    bot.polling()