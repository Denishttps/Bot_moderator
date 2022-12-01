from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import callback_query
import button
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import time
import aiogram
import config


bot = Bot(token=config.API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   await message.reply("Привет! " + str(message.from_user.first_name) + "\nНажимай на кнопку 'меню', и начинай работать")

# должны быть функции 'бан+', 'мут+', 'кик', 'ид+', 'рп', 'тест учасника чата±', 'приветствие', 'прощание', 'команды работоспособности'и может что-то ещё

#команда бан. 

@dp.message_handler(is_reply=True, commands=['Ban', 'Бан', 'бан', 'чс', 'Чс', 'ban'], commands_prefix=['/', '!', '.', ' '], is_chat_admin=True)
async def bancmd(msg: types.Message):
  if msg.chat.type != 'private':
    try:
      ban = await bot.ban_chat_member(chat_id=msg.chat.id, user_id=msg.reply_to_message.from_user.id) #бан
      admin = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
      if ban == True:
        await msg.reply_to_message.reply(f'🔴 <a href="tg://openmessage?user_id={msg.reply_to_message.from_user.id}">{msg.reply_to_message.from_user.first_name}</a>, бан навсегда\n👤 <b>Модератор:</b> <a href="tg://openmessage?user_id={admin.user.id}">{admin.user.first_name}</a>', reply_markup=button.unban) 
      else:
        await msg.answer('Пользователь и так уже забанен', reply_markup=button.unban)
    except:
      await msg.answer(f'⚠️ <b>У меня нет прав модератора, а именно: блокировать/разблокировать участников.</b>')


#мут
@dp.message_handler(is_reply=True, commands=['mute', 'Мут', 'мут', 'Mute'], commands_prefix=['/', '!', '.'], is_chat_admin=True)
async def bancmd(msg: types.Message):
  if msg.chat.type != 'private':
    admin = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
    mute = await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=time()+3600)
    if mute == True:
      await msg.answer(f'🔇 <a href="tg://openmessage?user_id={msg.reply_to_message.from_user.id}">{msg.reply_to_message.from_user.first_name}</a> лишается права слова навсегда\n<b>Модератор:</b> <a href="tg://openmessage?user_id={admin.user.id}">{admin.user.first_name}</a>', reply_markup=button.unmute)
    else:
      await msg.answer('Пользователь и так уже заглушен', reply_markup=button.unmute)

      
#id
@dp.message_handler(is_reply=True, commands=['id', 'ид', 'айди', 'uid'], commands_prefix=['.', '!', '/'])
async def idcmd(msg: types.Message):
  #await msg.answer(f'{msg.reply_to_message.from_user}')
  if msg.reply_to_message.from_user.is_bot == True:
    reply = msg.reply_to_message
    await msg.answer(f'🆔 бота <a href="tg://openmessage?user_id={reply.from_user.id}"><b>{reply.from_user.first_name}</b></a> равен <code>{reply.from_user.id}</code>', reply_markup=button.yid)
  elif msg.reply_to_message.from_user.is_bot == False:
    reply = msg.reply_to_message
    #🆔 пользователя Denis равен @827521748
    await msg.answer(f'🆔 пользователя <a href="tg://openmessage?user_id={reply.from_user.id}"><b>{reply.from_user.first_name}</b></a> равен <code>{reply.from_user.id}</code>', reply_markup=button.yid)

@dp.message_handler(commands=['id', 'ид', 'айди', 'uid'], commands_prefix=['.', '!', '/'])
async def idtcmd(msg: types.Message):
  await msg.answer(f'🆔 пользователя <a href="tg://openmessage?user_id={msg.from_user.id}"><b>{msg.from_user.first_name}</b></a> равен <code>{msg.from_user.id}</code>')


#test user
@dp.message_handler(is_reply=True, text='Кто ты')
async def uinfocmd(msg: types.Message):
  member = await bot.get_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
  admin = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
  if msg.chat.type != 'private':
    await msg.reply(f'<b>{member.user}\n\n\n{member.status}</b>')
  else:
    await msg.reply(f'<b>Команда </b><code>test</code> <b>не работает в приватных чатах</b>')


@dp.callback_query_handler(text='mid')
async def call_but(call: types.CallbackQuery):
  await bot.answer_callback_query(call.id)
  await call.message.answer(f' Ваш 🆔: <code>{call.from_user.id}</code>')


@dp.callback_query_handler(text='unban', is_chat_admin=True)
async def unbancall(call: types.CallbackQuery):
  msg = call.message
  for i in msg.entities:
    if i.type in ["text_link"]:
      si = i.url.split('tg://openmessage?user_id=')
      member = await bot.get_chat_member(msg.chat.id, si[1])
      #print(member.status)
      if member.status == 'kicked':
        unban = await bot.unban_chat_member(chat_id=call.message.chat.id, user_id=si[1])
        if unban == True:
          await call.message.reply(f'Пользователь разблокирован.')
        else:
          await msg.reply('Пользователь и не был заблокирован')


@dp.callback_query_handler(text='unmute', is_chat_admin=True)
async def unbancall(call: types.CallbackQuery):
  msg = call.message
  for i in msg.entities:
    if i.type in ["text_link"]:
      si = i.url.split('tg://openmessage?user_id=')
      member = await bot.get_chat_member(msg.chat.id, si[1])
      if member.status == 'restricted':
        unban = await bot.promote_chat_member(chat_id=call.message.chat.id, user_id=si[1])
        if unban == True:
          await call.message.reply(f'Пользователю разрешено говорить')
        else:
          await msg.reply('Пользователь и не был в мьюте')


@dp.message_handler()
async def msgall(msg: types.Message):
  text = msg.text.lower()
  if text == 'бот':
    await msg.reply('✅ На месте', reply=False)
  elif text == 'пинг':
    await msg.answer('ПОНГ')
  elif text == 'хикка':
    await msg.answer('🌗Hikka здесь ')
  else:
    if msg.chat.type == 'private':
      await msg.answer('Нет такой команды')







if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
