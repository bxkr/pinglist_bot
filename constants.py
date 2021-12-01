from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = 'TOKEN'
BOT = Bot(API_TOKEN, parse_mode='html')
HELLO_PM = 'Привет.\n\nЧтобы добавить бота в беседу, нажми кнопку ниже.'
ADD_TO_GROUP = '➕ Добавить в группу'
DEEPLINK_NAME = 'mentioner'
IM_IN = 'Я в '
SUPERGROUP = 'супергруппе (более 5 участников)'
GROUP = 'группе'
WHOLL_BE_MENTIONED = 'Какую группу хотите упомянуть?'
EMPTY_GROUP = 'Пустая группа (/mention_groups)'
EMPTY_GROUPS = 'Пока групп не существует (/mention_groups)'
ADD_GROUP = '➕ Добавить группу'
REMOVE_GROUP = '➖ Удалить группу'
REMOVE_FROM_GROUP = '➖ Удалить из группы'
LIST_GROUP_MEMBERS = '➿ Списки людей в группах (без упоминаний)'
CLOSE = '✖ Закрыть'
CLOSED = 'Хорошего дня :)'
BACK = '↩ Назад'
MANAGEMENT = 'Управление группами'
MANAGEMENT_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=ADD_GROUP, callback_data='mng-add-group'),
        InlineKeyboardButton(text=ADD_TO_GROUP, callback_data='mng-add-to-group')
    ],
    [
        InlineKeyboardButton(text=REMOVE_GROUP, callback_data='mng-remove-group'),
        InlineKeyboardButton(text=REMOVE_FROM_GROUP, callback_data='mng-remove-from-group')
    ],
    [
        InlineKeyboardButton(text=LIST_GROUP_MEMBERS, callback_data='mng-list')
    ],
    [
        InlineKeyboardButton(text=CLOSE, callback_data='close')
    ]
])
MANAGEMENT_BACK_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=BACK, callback_data='mng-back')
    ]
])
FAIL = 'Команда вызвана неверно!'
ADD_GROUP_M = 'Чтобы создать новую группу, ' \
              'отправьте команду ' \
              '/m_add_group {название} {имена пользователей (username) участников через запятую без @}\n' \
              'Например:\n' \
              '\n' \
              '<pre>/m_add_group abc one,two,three</pre>'
GROUP_ADDED = 'Создана группа {}. Кол-во пользователей: {}.'
ALREADY_CREATED = 'Группа уже существует!'
ADD_TO_GROUP_M = 'Чтобы добавить пользователя(-ей) в группу,' \
                 'отправьте команду ' \
                 '/m_add_to_group {название группы} {имена пользователей (username) через запятую без @}\n' \
                 'Например:\n' \
                 '\n' \
                 '<pre>/m_add_to_group abc one,two,three</pre>'
GROUP_NOT_FOUND = 'Такой группы не существует!'
USER_ALREADY_ADDED = 'Эти люди из указанного списка уже есть в группе: {}.\nДобавляю только новых...'
NO_NEW = 'Похоже, все люди из вашего списка уже есть в группе.'
ADDED_TO_GROUP = 'Группа: {}.\nНовых пользователей: {}.\nТеперь пользователей: {}.'
REMOVE_GROUP_M = 'Чтобы удалить группу, нажмите на кнопку с её названием:'
REMOVE_FROM_GROUP_FIRST_M = 'Чтобы удалить пользователя(-ей) из группы, для начала выберите её:'
REMOVE_FROM_GROUP_SECOND_M = 'Теперь при нажатии на кнопку с именем пользователя, вы удалите его:'
REMOVED_FROM_GROUP = 'Группа: {}.\nУдалено пользователей: {}.\nТеперь пользователей: {}.'
LIST_GROUP_MEMBERS_FIRST_M = 'Чтобы посмотреть людей в группе, для начала выберите её:'
LIST_GROUP_MEMBERS_SECOND_M = 'Это люди состоящие в группе {}:\n\n'
