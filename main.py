from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import create_startgroup_link

from constants import *
from data import get_groups, get_group_members, add_group, add_to_group, chat_m, remove_group, remove_from_group
from filters import ChatType, RegExp

from time import sleep

dp = Dispatcher()
dp.message.bind_filter(ChatType)
dp.callback_query.bind_filter(RegExp)


def create_groups_keyboard(message: Message, callback_query_prefix: str, with_button: str) -> InlineKeyboardMarkup:
    groups = get_groups(message)
    keyboard = []
    for key in groups:
        keyboard.append(InlineKeyboardButton(text=groups[key], callback_data=callback_query_prefix + str(key)))
    keyboard = [keyboard[i:i + 5] for i in range(0, len(keyboard), 5)]
    match with_button:
        case 'back':
            keyboard += [[InlineKeyboardButton(text=BACK, callback_data='mng-back')]]
        case 'close':
            keyboard += [[InlineKeyboardButton(text=CLOSE, callback_data='close')]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_remove_members_keyboard(message: Message, index: int) -> InlineKeyboardMarkup:
    members = get_group_members(message, index)
    keyboard = []
    for username in members:
        keyboard.append(InlineKeyboardButton(text=username, callback_data=f'rms{index},{username}'))
    keyboard = [keyboard[i:i + 5] for i in range(0, len(keyboard), 5)]
    keyboard += [[InlineKeyboardButton(text=BACK, callback_data='mng-back')]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(commands={'start'}, chat_type='private')
async def pm_start(message: Message):
    await message.answer(HELLO_PM, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=ADD_TO_GROUP, url=await create_startgroup_link(BOT, DEEPLINK_NAME))
        ]]
    ))


@dp.callback_query(re=r'group\d+')
async def group_call(callback: CallbackQuery):
    data = callback.data[5:]
    members = get_group_members(callback.message, int(data))
    if members:
        await callback.message.delete()
        await \
            callback.message.answer(', '.join(['@' + u for u in members]))
    else:
        await callback.message.edit_text(EMPTY_GROUP)


@dp.message(commands={'direct_mention'}, chat_type='group')
async def command_group_call(message: Message):
    args = message.text.split()
    members =\
        get_group_members(message, list(get_groups(message).keys())[list(get_groups(message).values()).index(args[1])])
    if members:
        await message.answer(', '.join(['@' + u for u in members]))
    else:
        await message.answer(EMPTY_GROUP)


@dp.message(commands={'start'}, chat_type='group')
async def start_group(message: Message):
    chat_m(message)
    await message.answer(IM_IN + (SUPERGROUP if message.chat.type == 'supergroup' else GROUP))


@dp.message(commands={'mention'}, chat_type='group')
async def mention(message: Message):
    if len(get_groups(message)):
        await message.answer(WHOLL_BE_MENTIONED, reply_markup=create_groups_keyboard(message, 'group', 'close'))
    else:
        await message.answer(EMPTY_GROUPS)


@dp.message(commands={'mention_groups'}, chat_type='group')
async def gm(message: Message):
    await message.answer(MANAGEMENT, reply_markup=MANAGEMENT_KEYBOARD)


@dp.callback_query(re='close')
async def close(callback: CallbackQuery):
    await callback.answer(CLOSED)
    await callback.message.delete()


@dp.callback_query(re=r'mng-(add-group|add-to-group|remove-group|remove-from-group|back|list)')
async def manager_call(callback: CallbackQuery):
    cb_data = callback.data[4:]
    if cb_data == 'add-group':
        await callback.message.edit_text(ADD_GROUP_M, reply_markup=MANAGEMENT_BACK_KEYBOARD)
    if cb_data == 'add-to-group':
        await callback.message.edit_text(ADD_TO_GROUP_M, reply_markup=MANAGEMENT_BACK_KEYBOARD)
    if cb_data == 'remove-group':
        await callback.message.edit_text(REMOVE_GROUP_M,
                                         reply_markup=create_groups_keyboard(callback.message, 'rm', 'back'))
    if cb_data == 'remove-from-group':
        await callback.message.edit_text(REMOVE_FROM_GROUP_FIRST_M,
                                         reply_markup=create_groups_keyboard(callback.message, 'rmf', 'back'))
    if cb_data == 'list':
        await callback.message.edit_text(LIST_GROUP_MEMBERS_FIRST_M,
                                         reply_markup=create_groups_keyboard(callback.message, 'ls', 'back'))
    if cb_data == 'back':
        await callback.message.edit_text(MANAGEMENT, reply_markup=MANAGEMENT_KEYBOARD)


@dp.message(commands={'m_add_group'}, chat_type='group')
async def m_add_group(message: Message):
    args = message.text.split()
    if len(args) == 3:
        name = args[1]
        if name not in get_groups(message).values():
            members = args[2].split(',')
            add_group(message, name, members)
            await message.answer(GROUP_ADDED.format(name, len(members)))
        else:
            await message.answer(ALREADY_CREATED)
    else:
        await message.answer(FAIL)


@dp.message(commands={'m_add_to_group'}, chat_type='group')
async def m_add_to_group(message: Message):
    args = message.text.split()
    if len(args) == 3:
        name = args[1]
        if name in get_groups(message).values():
            index = list(get_groups(message).keys())[list(get_groups(message).values()).index(name)]
            members = args[2].split(',')
            concurrent = [i for i in members if i in get_group_members(message, index)]
            if concurrent:
                conc_message = await message.answer(USER_ALREADY_ADDED.format(', '.join(concurrent)))
                sleep(2)
                members = [i for i in members if i not in concurrent]
                if not members:
                    await conc_message.edit_text(NO_NEW)
                    return
                await conc_message.delete()
            add_to_group(message, index, members)
            await message.answer(ADDED_TO_GROUP.format(name, len(members), len(get_group_members(message, index))))
        else:
            await message.answer(GROUP_NOT_FOUND)
    else:
        await message.answer(FAIL)


@dp.callback_query(re=r'rm\d+')
async def m_remove_group(callback: CallbackQuery):
    to_rm = callback.data[2:]
    remove_group(callback.message, int(to_rm))
    await callback.message.edit_text(REMOVE_GROUP_M,
                                     reply_markup=create_groups_keyboard(callback.message, 'rm', 'back'))


@dp.callback_query(re=r'rmf\d+')
async def m_remove_group(callback: CallbackQuery):
    index = int(callback.data[3:])
    await callback.message.edit_text(REMOVE_FROM_GROUP_SECOND_M,
                                     reply_markup=create_remove_members_keyboard(callback.message, index))


@dp.callback_query(re=r'rms\d+,\S+')
async def m_remove_from_group(callback: CallbackQuery):
    args = callback.data[3:].split(',')
    index = int(args[0])
    username = args[1]
    remove_from_group(callback.message, index, username)
    await callback.message.edit_text(REMOVE_FROM_GROUP_SECOND_M,
                                     reply_markup=create_remove_members_keyboard(callback.message, index))


@dp.callback_query(re=r'ls\d+')
async def m_list_groups_people(callback: CallbackQuery):
    index = int(callback.data[2:])
    people = get_group_members(callback.message, index)
    await callback.message.edit_text(LIST_GROUP_MEMBERS_SECOND_M.format(get_groups(callback.message)[index]) +
                                     '\n'.join([f'{i}. {item}' for (i, item) in enumerate(people, start=1)]),
                                     reply_markup=MANAGEMENT_BACK_KEYBOARD)


if __name__ == '__main__':
    dp.run_polling(BOT)
