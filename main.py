
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import chat, message
from tarjima import defTelefon
from brand_name import TelefonNomi,TelefonHaqida,defPhone
import sqlite3

API_TOKEN = 'Sizning telegram token'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start','restart'])
async def send_welcome(message: types.Message):
    await message.reply(f"🤓Assalom aleykum✋\n{message.chat.full_name}\n📱Telefonlar olamiga🌎\nXUSH KELDINGIZ‼️")
    await message.answer("🔘Kerakli tugmani bosing⤵️",reply_markup=get_keyboard())
    con=sqlite3.connect("baza.db")
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS login(id INTEGER,brend STRING,telefon STRING)""")
    con.commit()
    user_id=message.chat.id
    brend=""
    telefon=""
    cur.execute('SELECT id FROM login WHERE id=?',[(user_id)])
    data=cur.fetchone()
    if data is None:
        cur.execute('INSERT INTO login VALUES (?,?,?)',(user_id, brend, telefon))
        con.commit()
    else:
        cur.execute('UPDATE login SET brend=? WHERE id=?',(brend, user_id))
        cur.execute('UPDATE login SET telefon=? WHERE id=?',(telefon, user_id))
        con.commit()

@dp.message_handler(Text(equals="🤖Botdan foydalanish"))
async def send_help(message: types.Message):
    await message.reply("Yo'riqnoma🤖\n1.Brendlar tugmasini bosing.\n2.Brendlar ichidan brendni tanlang.\n3.Brendga tegishli telefon modelini tugmasini bosing.\n4.O'zingizga kerakli ma'lumotlarni oling va yaqinlaringizga ham ulashing.")

@dp.message_handler(Text(equals="🧑‍💻Admin"))
async def send_admin(message: types.Message):
    await message.reply("💻Dasturchi: Turdiyev Alisher\nMurojaat uchun: @Xxuligan")

@dp.message_handler(Text(equals="⬅️exit"))
async def send_exit(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    con=sqlite3.connect("baza.db")
    cur=con.cursor()
    cur.execute('UPDATE login SET telefon=? WHERE id=?',("", message.chat.id))
    cur.execute('UPDATE login SET brend=? WHERE id=?',("", message.chat.id)) 
    con.commit()
    await message.answer("🔘Kerakli tugmani bosing⤵️",reply_markup=get_keyboard())

@dp.message_handler(Text(equals="🌎Brendlar"))
async def send_brend(message: types.Message):
    buttons = []
    mal=defPhone()
    
    if mal:
        for m,n in mal.items():
            buttons.append(types.InlineKeyboardButton(text=str(m), callback_data=str(n)))
        keyboard1 = types.InlineKeyboardMarkup(row_width=2)
        keyboard1.add(*buttons[0:60])
        keyboard2 = types.InlineKeyboardMarkup(row_width=2)
        keyboard2.add(*buttons[60:117])
        await message.answer("🤖Botda mavjud brendlar⤵️", reply_markup=keyboard1)
        await message.answer("🤖Botda mavjud brendlar⤵️", reply_markup=keyboard2)
        

    else:"🆘Texnik xatolik.\nAdmin ga murojaat qiling!!!"

@dp.callback_query_handler()
async def send_value(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await bot.delete_message(call.message.chat.id, call.message.message_id-1)
    user_id=call.message.chat.id
    brend=str(call.data)
    con=sqlite3.connect("baza.db")
    cur=con.cursor()
    cur.execute('UPDATE login SET brend=? WHERE id=?',(brend, user_id))
    con.commit()
    cal_p=TelefonNomi(user_id)
    cur.execute('UPDATE login SET telefon=? WHERE id=?',(str(cal_p), user_id))
    con.commit()
    buttons=[]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['⬅️exit']+list(cal_p)+['⬅️exit']
    keyboard.add(*buttons)
    await bot.send_message(call.message.chat.id,"📲Kerakli telefonni tanlang⤵️",reply_markup=keyboard)
    

@dp.message_handler(Text(equals="👥Foydalanuvchilar"))
async def send_users(message: types.Message):
    con=sqlite3.connect("baza.db")
    cur=con.cursor()
    c=cur.execute("SELECT id FROM login")
    await message.answer(f"🤖Botdan foydalanuvchilar soni: {str(len(c.fetchall()))} ta.")

@dp.message_handler()
async def message_phones(message: types.Message):
    malumot=TelefonHaqida(message.chat.id,message.text)
    if malumot:
               
        await message.reply(defTelefon(malumot['malumot']))
        await message.reply_photo(malumot['rasm'])
    else:
        await message.reply(f"📵{message.text}📵 telefon brendda mavjud emas⛔️")

def get_keyboard():
    buttons=["🌎Brendlar","🤖Botdan foydalanish","🧑‍💻Admin","👥Foydalanuvchilar"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)