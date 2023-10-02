import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery, InputMediaPhoto
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram.error import BadRequest

with open('token.txt', 'r') as token_file:
    token = token_file.read().strip()

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

user_data = {}

def start_menu(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    user_data.setdefault(chat_id, {})['menu'] = 'StartMenu'
    start_menu_config = config['StartMenu']
    query.edit_message_text(text=start_menu_config['message'])
    delete_user_messages(update, context)
    message_id = send_menu_message(context, chat_id, start_menu_config)
    user_data[chat_id].setdefault('bot_messages', []).append(message_id)

def button_click(update, context):
    query = update.callback_query
    if query.message is None:
        return

    chat_id = query.message.chat_id
    menu_id = query.data
    current_menu = config[user_data[chat_id]['menu']]
    button = next((b for b in current_menu['buttons'] if b['id'] == menu_id), None)

    if button:
        user_data[chat_id]['menu'] = button['next_menu']
        next_menu = config[button['next_menu']]
        delete_user_messages(update, context)

        if 'image' in next_menu and next_menu['image']:
            caption = next_menu['message']
            media = InputMediaPhoto(media=next_menu['image'], caption=caption, parse_mode='Markdown')
            reply_markup = create_inline_keyboard(next_menu['buttons'])
            query.message.edit_media(media=media, reply_markup=reply_markup)
        else:
            message = next_menu.get('message', '')
            reply_markup = create_inline_keyboard(next_menu['buttons'])
            query.message.edit_caption(caption=message, reply_markup=reply_markup, parse_mode='Markdown')

def create_inline_keyboard(buttons):
    keyboard = [[] for _ in range(max(button['line'] for button in buttons) + 1)]
    for button in buttons:
        line = button['line']
        keyboard[line].append(InlineKeyboardButton(button['label'], callback_data=button['id']))
    return InlineKeyboardMarkup(keyboard)

def start_command(update, context):
    chat_id = update.message.chat_id
    user_data.setdefault(chat_id, {})['menu'] = 'StartMenu'
    start_menu_config = config['StartMenu']

    # Delete all previous bot messages
    if 'bot_messages' in user_data[chat_id]:
        for message_id in user_data[chat_id]['bot_messages']:
            try:
                context.bot.delete_message(chat_id, message_id)
            except BadRequest:
                pass
        user_data[chat_id]['bot_messages'] = []

    delete_user_messages(update, context)
    message_id = send_menu_message(context, chat_id, start_menu_config)
    user_data[chat_id].setdefault('bot_messages', []).append(message_id)

    user_data[chat_id]['chat_id'] = chat_id

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    user_id = query.from_user.id
    user_name = query.from_user.username
    if data == 'delete':
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        context.bot.send_message(chat_id=query.message.chat_id, text=f"User {user_name} ({user_id}) clicked delete")
    elif data == 'keep':
        context.bot.send_message(chat_id=query.message.chat_id, text=f"User {user_name} ({user_id}) clicked keep")
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text="Unknown button clicked")

def delete_user_messages(update, context):
    if update.message:
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        context.bot.delete_message(chat_id, update.message.message_id)

def send_menu_message(context, chat_id, menu_config):
    keyboard = [[] for _ in range(max(button['line'] for button in menu_config['buttons']) + 1)]
    for button in menu_config['buttons']:
        keyboard[button['line']].append(InlineKeyboardButton(button['label'], callback_data=button['id']))
    reply_markup = InlineKeyboardMarkup(keyboard)

    if 'image' in menu_config and menu_config['image']:
        message = context.bot.send_photo(
            chat_id=chat_id,
            photo=menu_config['image'],
            caption=menu_config['message'],
            reply_markup=reply_markup
        )
    else:
        message = context.bot.send_message(
            chat_id=chat_id,
            text=menu_config['message'],
            reply_markup=reply_markup
        )
    return message.message_id

updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CallbackQueryHandler(button_click, pattern='.*'))
dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(MessageHandler(Filters.all, delete_user_messages))

updater.start_polling()
updater.idle()