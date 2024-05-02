from aiogram import Bot,Dispatcher,types, F
from aiogram.filters import CommandStart
from aiogram.methods import DeleteWebhook
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
import sqlite3 as sq
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from datetime import datetime, timedelta
import random

Token = '6374810081:AAFTDgsJgvHTFMX1tg4vZyCyHmTMtvqbE4o'

Admin_Id = 823388511

bot= Bot(token=Token)
dp = Dispatcher()

with sq.connect('refers.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS refers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,            
                polzavatel TEXT,
                refer_id INTEGER,
                refer_name TEXT,
                language TEXT DEFAULT qwe,
                balance REAL DEFAULT 0,
                balance_RUB REAL DEFAULT 0,
                Vigoda_Ref REAL DEFAULT 0
    )
""")

with sq.connect('refers.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                summa_popolnenie REAL,
                summa_popolnenie_RUB REAL,
                data_popolnenite TEXT,
                summa_vivoda INTEGER,
                data_vivoda TEXT
    )
""")
    
with sq.connect('refers.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS activi(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                tarif TEXT,
                summaN INTEGER,
                summaT REAL,
                data_priobreteniya TEXT,
                data_konec DATE,
                data_pribavleniya DATE,
                Valuta TEXT
    )
""")

with sq.connect('refers.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Past_assets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                tarif TEXT,
                summaN INTEGER,
                summaT REAL,
                data_priobreteniya TEXT,
                data_konec DATE,
                data_pribavleniya DATE
    )
""")

class MyCallback(CallbackData, prefix="my"):
    foo: str

user_messages = {}
user_messages2 = {}
user_messages3 = {}
user_messages4 = {}
user_messages5 = {}
user_messages6 = {}
user_messages7 = {}
user_messages8 = {}
user_messages9 = {}

def continue_keyboard(language):
    builder = InlineKeyboardBuilder()
    if language == 'English':
        builder.button(
            text='✅Continue',
            callback_data=MyCallback(foo="continue") 
        )
    else:
        builder.button(
            text='✅Продолжить',
            callback_data=MyCallback(foo="continue") 
        )
    return builder.as_markup()

def VIBORPOPOL():
    builder = InlineKeyboardBuilder()

    builder.button(
            text='USDT',
            callback_data=MyCallback(foo="usdt") 
        )
    builder.button(
            text='Рубли',
            callback_data=MyCallback(foo="rublesp") 
        )
    builder.adjust(1)
    return builder.as_markup()

def VIBORvaluti():
    builder = InlineKeyboardBuilder()

    builder.button(
            text='USDT',
            callback_data=MyCallback(foo="usdtvaluta") 
        )
    builder.button(
            text='Рубли',
            callback_data=MyCallback(foo="rublesvaluta") 
        )
    builder.adjust(1)
    return builder.as_markup()

def VIBORvaluti2():
    builder = InlineKeyboardBuilder()

    builder.button(
            text='USDT',
            callback_data=MyCallback(foo="usdtvaluta2") 
        )
    builder.button(
            text='Рубли',
            callback_data=MyCallback(foo="rublesvaluta2") 
        )
    builder.adjust(1)
    return builder.as_markup()

def VIBORvaluti3():
    builder = InlineKeyboardBuilder()

    builder.button(
            text='USDT',
            callback_data=MyCallback(foo="usdtvaluta3") 
        )
    builder.button(
            text='Рубли',
            callback_data=MyCallback(foo="rublesvaluta3") 
        )
    builder.adjust(1)
    return builder.as_markup()


def USDQWE():
    builder = InlineKeyboardBuilder()

    builder.button(
            text='USDT',
            callback_data=MyCallback(foo="USDDP") 
        )
    builder.button(
            text='USDC',
            callback_data=MyCallback(foo="USDC") 
        )
    builder.adjust(1)
    return builder.as_markup()

def vernytsa(language):
    builder = InlineKeyboardBuilder()
    if language == 'English':
        builder.button(
                text='Вернуться',
                callback_data=MyCallback(foo="vernytsa") 
            )
    else:
        builder.button(
                text='Back to main menu',
                callback_data=MyCallback(foo="vernytsa") 
            )
    builder.adjust(1)
    return builder.as_markup()

phrases = {
    'Russia': {
        'welcome_message': "🤖Добро пожаловать в главное меню!",
        'invite_yourself_error': "Вы не можете пригласить сами себя.",
        'choose_language': "Выберите язык",
        'privetsvyi': '🤖Приветствую тебя в боте Steam Parser, здесь ты можешь инвестировать и зарабатывать на нашей работе.',
        'odin_var': 'Выберите один из вариантов!',
        'lic_cabinet': """
👤Ваш ID: {chat_id}
🏦Баланс  $: {balance_ob_usdt}  
🏦Баланс  ₽: {total_rub}
💳В работе: {total_investments}$ / {total_investments2_RUB}₽
📈Прибыль $: {total_profit}
📈Прибыль ₽: {total_profit_Rub}
💸Доступно для вывода: {balance}$ / {balance_Rub}₽
""",
        'summa_popolneniya': """
Укажите сумму пополнения
❗️Минимальная сумма пополнения: 100$""",
        'sposob_oplati': 'Выберите способ оплаты',
        'oplata': """
⚠️ Переведите {USDT} USDT по данному адресу.   ⬇️

✅Сеть: USDT [TRC20]""",
        'oplatau':""" ⚠️ Переведите {USDS} USDC по данному адресу⬇️

✅Сеть: USDT [TRC20]""",
        'info_oplata': 'Ваш перевод обрабатывается, ожидайте',
        'FAQ': 'ℹ️Выберите интересующий вас вопрос',
        'change_language': 'Язык успешно изменён',
        'vibor_invest' :'Выберите один из варинатов',
        'vibor_tarif': 'Выберите тариф!',
        'history_message': "История пополнений и выводов:",
        'replenishment_history': "История пополнений:",
        'no_replenishment_history': "У вас пока нет истории пополнений.",
        'withdrawal_history': "\nИстория выводов:",
        'no_withdrawal_history': "\nУ вас пока нет истории выводов.",
        'withdrawal_amount_prompt': "Введите сумму вывода (от 1 до {0}):",
        'withdrawal_amount_error': 'Введите целое число!',
        'insufficient_balance_error': "У вас недостаточно средств для вывода.",
        'withdrawal_request_sent': "Сумма для вывода передана администраторам: {0}$. Ожидайте!",
        'withdrawal_request_sent2': "Сумма для вывода передана администраторам: {0}₽. Ожидайте!",
        'vvedite100': 'Введите сумму больше либо равную 100!',
        'summa_vvedeniya': 'Введите сумму, которую хотите инвестировать',
        'tariff_purchased': 'Тариф {tariff} куплен на: {saved_message}$. Баланс обновлен.',
        'tariff_purchased2' : 'Тариф {tariff} куплен на: {saved_message}₽. Баланс обновлен.',
        'activity_info': "Информация об активе:",
        'tariff': 'Тариф',
        'initial_amount': 'Начальная сумма',
        'current_amount': 'Текущая сумма',
        'purchase_date': 'Дата приобретения',
        'end_date': 'Дата окончания',
        'no_active_subs': 'У вас нет активных подписок.',
        'net_historytarif':'У вас нет истории тарифов.',
        'history_messagetarif': 'История тарифов:',
        '123initial_amount': 'Сумма инвестиции:',
        'obj_summa': 'Общая сумма:',
        'profitna': 'Профит на',
        'FAQVOPROS': 'Посетите раздел 📚Ч.З.В в главном меню,возможно ваш вопрос был задан ранее.Также вы можете написать свой вопрос напрямую нам⬇️',
        'zero_balance_error':'У вас нет денег на счету'


    },



    'English': {
        'welcome_message': "🤖Welcome to the main menu!",
        'invite_yourself_error': "You cannot invite yourself.",
        'choose_language': "Choose language",
        'privetsvyi' : '🤖I welcome you to the Steam Parser bot, here you can invest and earn money from our work.',
        'lic_cabinet': """
👤Your ID: {chat_id}
💵Balance: {balance} USDT / {balance_Rub}₽
💳Active investments {total_investments} USDT:
📈Total earned {total_profit} USDT:
""",
        'summa_popolneniya': """
Specify the amount of replenishment
❗️Minimum replenishment amount: 100 USDT.""",
        'sposob_oplati': 'Select a Payment Method',
        'oplata': """
⚠️ To top up your balance, you just need to transfer {USDT} USDT to the wallet address below. ⬇️

✅Network: USDT [TRC20]""",
        'info_oplata': 'Your transaction is being processed, please wait',
        'FAQ': 'ℹ️Select the question you are interested in',
        'change_language': 'Language successfully changed',
        'vibor_language': 'Change language',
        'vibor_invest' :'Choose one of the options',
        'vibor_tarif': 'Select tariff!',
        'history_message': "Replenishment and withdrawal history:",
        'replenishment_history': "Replenishment history:",
        'no_replenishment_history': "You don't have any replenishment history yet.",
        'withdrawal_history': "\nWithdrawal history:",
        'no_withdrawal_history': "\nYou don't have any withdrawal history yet.",
        'replenishment_amount': "Replenishment amount",
        'replenishment_date': "Replenishment date",
        'withdrawal_amount': "Withdrawal amount",
        'withdrawal_date': "Withdrawal date",
        'withdrawal_amount_prompt': "Enter the withdrawal amount (from 1 to {0}):",
        'withdrawal_amount_error': 'Enter an integer!',
        'insufficient_balance_error': "You don't have enough balance for withdrawal.",
        'withdrawal_request_sent': "Withdrawal request for {0} has been submitted to the administrators. Please wait!",
        'vvedite100': 'Enter an amount greater than or equal to 100!',
        'summa_vvedeniya': 'Enter the amount you want invest',
        'tariff_purchased': 'Tariff {tariff} purchased for: {saved_message} USDT. Balance updated.',
        'tariff_purchased2' : "Tariff {tariff} purchased for: {saved_message} RUB. Balance updated.",
        'activity_info': "Activity Information:",
        'tariff': 'Tariff',
        'initial_amount': 'Initial Amount',
        'current_amount': 'Current Amount',
        'purchase_date': 'Purchase Date',
        'end_date': 'End Date',
        'no_active_subs': 'You have no active subscriptions.',
        'odin_var': 'Choose one of the options!',
        'net_historytarif':'You have no fare history.',
        'history_messagetarif': 'Tariff history:',
        '123initial_amount': 'Investment amount:',
        'obj_summa': 'Total amount:',
        'profitna': 'Profit On',
        'FAQVOPROS': 'Visit the 📚FAQ section in the main menu, your question may have been asked earlier. You can also write your question directly to us⬇️',
        'zero_balance_error':'You have no money in your account'
    }
}

def podpiska_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="💻Перейти в канал", url="https://t.me/+886AoeO7uWZhYjQ6")
    )
    builder.button(
        text='✅Проверить подписку',
        callback_data=MyCallback(foo='proverka')
    )
    builder.adjust(1)

    return builder.as_markup()

def remove_keyboard():
    return ReplyKeyboardRemove(remove_keyboard=True)

def startkeyboard(language):
    builder = ReplyKeyboardBuilder()
    if language == 'Russia': 
        builder.button(text='🏦Личный кабинет')
        builder.button(text='👥Реферальная программа')
        builder.button(text='📚Часто задаваемые вопросы')
        builder.button(text='📤Техническая поддержка')
    else:
        builder.button(text='🏦Personal Area')
        builder.button(text='👥Referral program')
        builder.button(text='📚FAQ')
        builder.button(text='📤Support')
    builder.adjust(1)
    return builder.as_markup(resize_keyboard = True)

def FAQ(language):
    builder = InlineKeyboardBuilder()
    if language == 'Russia':
        builder.button(
            text='1',
            callback_data=MyCallback(foo='1')
        )    
        builder.button(
            text='2',
            callback_data=MyCallback(foo='2')
        )
        builder.button(
            text='3',
            callback_data=MyCallback(foo='3')
        )
        builder.button(
            text='4',
            callback_data=MyCallback(foo='4')
        )
        builder.button(
            text='5',
            callback_data=MyCallback(foo='5')
        )

    else:
        builder.button(
            text='1',
            callback_data=MyCallback(foo='1')
        )    
        builder.button(
            text='2',
            callback_data=MyCallback(foo='2')
        )
        builder.button(
            text='3',
            callback_data=MyCallback(foo='3')
        )
        builder.button(
            text='4',
            callback_data=MyCallback(foo='4')
        )
        builder.button(
            text='5',
            callback_data=MyCallback(foo='5')
        )
        

    builder.adjust(1)
    return builder.as_markup()

def supp(language):
    builder = InlineKeyboardBuilder()
    if language == 'Russia':
        builder.row(types.InlineKeyboardButton(
                text="Поддержка", url="https://t.me/alexme8")
            )
    else:
        builder.row(types.InlineKeyboardButton(
                text="Support", url="https://t.me/alexme8")
            )
    return builder.as_markup()

def depandvivod(language='Russia'):
    builder = InlineKeyboardBuilder()

    if language == 'Russia':
        builder.button(
            text='Пополнить баланс',
            callback_data=MyCallback(foo='dep')
        )
        builder.button(
            text='Инвестировать',
            callback_data=MyCallback(foo='invest')
        )
        builder.button(
            text='Вывод средств',
            callback_data=MyCallback(foo='vivod')
        )
        
    else:
        builder.button(
            text='Top up the balance',
            callback_data=MyCallback(foo='dep')
        )
        builder.button(
            text='To invest',
            callback_data=MyCallback(foo='invest')
        )
        builder.button(
            text='Withdrawal of funds',
            callback_data=MyCallback(foo='vivod')
        )

    builder.adjust(1)
    return builder.as_markup()

def VIBORVIVOD123():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='USDT',
        callback_data=MyCallback(foo="USDTVIVOD") 
    )
    builder.button(
        text='RUB',
        callback_data=MyCallback(foo="RUBVIVOD") 
    )
    builder.adjust(1)
    return builder.as_markup()

def vnhistory_keyboard(language):
    builder = InlineKeyboardBuilder()
    if language == 'Russia': 
        builder.button(
                text='История выводов и пополнений',
                callback_data=MyCallback(foo='history_vivod')
            )
        builder.button(
                text='История операций',
                callback_data=MyCallback(foo='historytarif')
            )
    else:
        builder.button(
                text='History of withdrawals and deposits',
                callback_data=MyCallback(foo='history_vivod')
            )
        builder.button(
                text='Operations history',
                callback_data=MyCallback(foo='historytarif'))
    builder.adjust(1)
    return builder.as_markup()


def sposob_oplati(language='Russia'):
    builder = InlineKeyboardBuilder()
    if language == 'Russia':
        builder.button(
            text='Криптовалюта',
            callback_data=MyCallback(foo='kripta')
        )
        builder.button(
            text='Рубли',
            callback_data=MyCallback(foo='rubles')
        )
    else:
        builder.button(
            text='Cryptocurrency', 
           callback_data=MyCallback(foo='kripta'))    
        builder.button(
            text='Russian rubles',
            callback_data=MyCallback(foo='rubles')
        )
    builder.adjust(1)
    return builder.as_markup()

def oplatil(language='Russia'):
    builder = InlineKeyboardBuilder()
    if language == 'Russia':
        builder.button(
            text='Готово✅',
            callback_data=MyCallback(foo='oplatil')
        )     
    else:
        builder.button(
            text='Done✅',
            callback_data=MyCallback(foo='oplatil')
        )  
    return builder.as_markup()

def language():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='🇷🇺 Russia',
        callback_data=MyCallback(foo="Russia") 
    )
    builder.button(
        text='🇬🇧 English',
        callback_data=MyCallback(foo="English") 
    )
    builder.adjust(1)
    return builder.as_markup()

def language():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='🇷🇺 Russia',
        callback_data=MyCallback(foo="Russia") 
    )
    builder.button(
        text='🇬🇧 English',
        callback_data=MyCallback(foo="English") 
    )
    builder.adjust(1)
    return builder.as_markup()

def invest(language):
    if language == 'Russia':
        builder = InlineKeyboardBuilder()
        builder.button(
            text='Тарифы',
            callback_data=MyCallback(foo="tarifi") 
        )
        builder.button(
            text='Активы',
            callback_data=MyCallback(foo="activi") 
        )
    else:
        builder = InlineKeyboardBuilder()
        builder.button(
            text='Tariff',
            callback_data=MyCallback(foo="tarifi") 
        )
        builder.button(
            text='Assets',
            callback_data=MyCallback(foo="activi") 
        )
    builder.adjust(1)
    return builder.as_markup()

def refers(language):
    builder = InlineKeyboardBuilder()
    if language == 'Russia':
        builder.button(
                text='Приглашение',
                callback_data=MyCallback(foo="priglash") 
            )
        builder.button(
                text='Бонусы',
                callback_data=MyCallback(foo="bonuces") 
            )
    else:
        builder.button(
                text='Invitation',
                callback_data=MyCallback(foo="priglash") 
            )
        builder.button(
                text='Bonuses',
                callback_data=MyCallback(foo="bonuces") 
            )
    builder.adjust(1)
    return builder.as_markup()
    

def tarifi_keyboard(language):
    builder = InlineKeyboardBuilder()
    if language == 'Russia':
        builder.button(
            text='Вклад 1 Месяц(≈20%)',
            callback_data=MyCallback(foo="month") 
        )
        builder.button(
            text='Вклад 3 Месяца(≈80%)',
            callback_data=MyCallback(foo="month3") 
        )
        builder.button(
            text='Вклад Пол Года (≈200%)',
            callback_data=MyCallback(foo="month6") 
        )
    else:
        builder.button(
            text='Deposit 1 Month (≈20%)',
            callback_data=MyCallback(foo="month") 
        )
        builder.button(
            text='Deposit 3 Months (≈80%)',
            callback_data=MyCallback(foo="month3") 
        )
        builder.button(
            text='Deposit Half a Year (≈200%)',
            callback_data=MyCallback(foo="month6") 
        )
    builder.adjust(1)
    return builder.as_markup()

def get_language(user_id):
    with sq.connect('refers.db') as con:
        cur = con.cursor()
        cur.execute("SELECT language FROM refers WHERE user_id=?", (user_id,))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return 'russia'

async def get_user_language(user_id):
        with sq.connect('refers.db') as con:
            cur = con.cursor()
            cur.execute("SELECT language FROM refers WHERE user_id=?", (user_id,))
            language = cur.fetchone()
            return language[0] if language else None

@dp.message(CommandStart())
async def cmd_start(message: types.Message):

    user_language = await get_user_language(message.from_user.id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    text = message.text.split() 

    if len(text) > 1:
        refer_id = text[1]

        if refer_id == str(message.from_user.id):
            await message.answer(phrases_dict['invite_yourself_error'])
            return

        with sq.connect('refers.db') as con:
            cur = con.cursor()
            cur.execute("SELECT polzavatel FROM refers WHERE user_id=?", (refer_id,))
            refer_name = cur.fetchone()
            if refer_name:
                refer_name = refer_name[0]
            else:
                refer_name = None

    else:
        refer_id = None
        refer_name = None

    user_id = message.from_user.id
    user_name = message.from_user.first_name

    with sq.connect('refers.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM refers WHERE user_id=?", (user_id,))
        existing_user = cur.fetchone()

    if existing_user:
        await message.answer(phrases_dict['welcome_message'], reply_markup=startkeyboard(language=user_language))
        return

    with sq.connect('refers.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO refers (user_id, polzavatel, refer_id, refer_name) VALUES (?, ?, ?, ?)", (user_id, user_name, refer_id, refer_name))

    await message.answer(phrases_dict['choose_language'], reply_markup=language())

@dp.message((F.text == '📤Техническая поддержка') | (F.text == '📤Support'))
async def cmd_supp(message:types.Message):
    user_id = message.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await message.answer(phrases_dict['FAQVOPROS'],reply_markup=supp(language=user_language))

@dp.message((F.text == '📚Часто задаваемые вопросы') | (F.text == '📚FAQ'))
async def cmd_FAQ(message:types.Message):
    user_id = message.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await message.answer(phrases_dict['FAQ'],reply_markup=FAQ(language=user_language))

@dp.message((F.text == '🏦Личный кабинет') | (F.text == '🏦Personal Area'))
async def cmd_lic_cabinet(message: types.Message):
    user_id = message.from_user.id

    with sq.connect('refers.db') as con:
        cur = con.cursor()
        cur.execute("SELECT balance FROM refers WHERE user_id=?", (user_id,))
        balance_data = cur.fetchone()

    cur.execute("SELECT balance_RUB FROM refers WHERE user_id=?", (user_id,))
    balance_Rub1 = cur.fetchone()
    balance_Rub = int(balance_Rub1[0]) if balance_Rub1 else 0  # Преобразование в целое число, если значение есть, иначе 0

    if balance_data:
        balance = balance_data[0]
    else:
        balance = 0

    if balance % 1 == 0:  # Проверяем, есть ли у баланса дробная часть
        balance = int(balance)  # Преобразуем в целое число, если дробная часть отсутствует

    if balance % 1 != 0 and len(str(balance).split('.')[1]) > 2:
        new_balance = round(balance, 2)
        with sq.connect('refers.db') as con:
            cur = con.cursor()
            cur.execute("UPDATE refers SET balance=? WHERE user_id=?", (new_balance, user_id))
            con.commit()
        balance = new_balance  
    
    total_profit = 0
    total_investments = 0
    total_investments2_RUB = 0
    total_profit_Rub = 0
    cur = con.cursor()
    cur.execute("SELECT SummaT, SummaN FROM activi WHERE user_id=? AND `Valuta`='USDT'", (user_id,))
    investments_data = cur.fetchall()
    for investment_data in investments_data:
        summaT, summaN = investment_data
        profit = summaT - summaN
        total_profit += profit
    total_profit = round(total_profit, 2)


    cur.execute("SELECT SummaT, SummaN FROM activi WHERE user_id=? AND `Valuta`='RUB'", (user_id,))
    investments_data = cur.fetchall()
    for investment_data in investments_data:
        summaT, summaN = investment_data
        profit = summaT - summaN
        total_profit_Rub += profit
    total_profit_Rub = round(total_profit, 2)

    cur.execute("SELECT SUM(summaN) FROM activi WHERE user_id=? AND `Valuta`='USDT'", (user_id,))
    total_investments_data = cur.fetchone()
    if total_investments_data[0]:
            total_investments = total_investments_data[0]

    cur.execute("SELECT SUM(summaN) FROM activi WHERE user_id=? AND `Valuta`='RUB'", (user_id,))
    total_investments_data2 = cur.fetchone()
    if total_investments_data2[0]:
            total_investments2_RUB = total_investments_data2[0]

    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    
    balance_ob_usdt = balance + total_investments
    balance_ob_rub = balance_Rub + total_investments2_RUB
    total_investments_rub = total_investments2_RUB
    
    # Преобразование баланса и сумм в работе в целые числа, если дробная часть равна нулю
    balance = int(balance) if balance % 1 == 0 else balance
    balance_Rub = int(balance_Rub) if balance_Rub % 1 == 0 else balance_Rub
    total_investments = int(total_investments) if total_investments % 1 == 0 else total_investments
    total_investments_rub = int(total_investments_rub) if total_investments_rub % 1 == 0 else total_investments_rub
    balance_Rub = int(balance_Rub) if balance_Rub % 1 == 0 else balance_Rub
    message_text = phrases_dict['lic_cabinet'].format(
        balance=balance,
        chat_id=user_id,
        total_investments=total_investments,
        total_profit=total_profit,
        balance_Rub=balance_Rub,
        balance_ob_usdt=balance_ob_usdt,
        total_investments2_RUB=total_investments_rub,
        total_rub=balance_ob_rub,
        total_profit_Rub = total_profit_Rub
    )
    await message.answer(message_text, reply_markup=depandvivod(language=user_language))

@dp.message((F.text == '👥Реферальная программа') | (F.text == '👥Referral program'))
async def cmd_referrals(message: types.Message):
    user_id = message.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id,phrases_dict['odin_var'],reply_markup=refers(language=user_language))


@dp.callback_query(MyCallback.filter(F.foo == "priglash"))
async def my_callback_rda(query: types.CallbackQuery, callback_data: MyCallback):
    user_id = query.from_user.id

    with sq.connect('refers.db') as con:
        cur = con.cursor()
        cur.execute("SELECT refer_id, refer_name FROM refers WHERE user_id=?", (user_id,))
        result = cur.fetchone() 
        if result:
            refer_id, refer_name = result
        else:
            refer_id, refer_name = None, None

        cur.execute("SELECT COUNT(*) FROM refers WHERE refer_id=?", (user_id,))
        count = cur.fetchone()[0]
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        if refer_name:
            message_refers = f'''🔍Получайте доход в USDT,приглашая партнеров по реферальной ссылке.
            \n 🔗Реферальная ссылка: https://t.me/parser245bot?start={query.from_user.id}
            ❌1 уровень: 7%
            ❌2 уровень: 5%
            ❌3 уровень: 3%
            👤Приглашено:
            1 уровень: {count} - 0.0 USDT
            2 уровень: 0 - 0 USDT
            3 уровень: 0 - 0 USDT
            💵Заработано на рефералах:
            1 уровень: 0.0 USDT
            2 уровень: 0.0 USDT
            3 уровень: 0.0 USDT
            Пополните счет от 1000 USDT чтобы открыть партнерскую программу 
            👥Ваш пригласитель: {refer_name}
            ➡️1 уровень доступен когда личный баланс выше 1000$ и оборот структуры выше 3000$ 
            ➡️2 уровень доступен когда оборот структуры выше 5000$
            ➡️3 уровень доступен когда оборот структуры выше 10000$
            '''
        else:
            message_refers = f'''🔍Получайте доход в USDT,приглашая партнеров по реферальной ссылке.
            \n 🔗Реферальная ссылка: https://t.me/parser245bot?start={query.from_user.id}
            ❌1 уровень: 7%
            ❌2 уровень: 5%
            ❌3 уровень: 3%
            👤Приглашено:
            1 уровень: {count} - 0.0 USDT
            2 уровень: 0 - 0 USDT
            3 уровень: 0 - 0 USDT
            💵Заработано на рефералах:
            1 уровень: 0.0 USDT
            2 уровень: 0.0 USDT
            3 уровень: 0.0 USDT
            Пополните счет от 1000 USDT чтобы открыть партнерскую программу 
            👥Ваш пригласитель: None
            ➡️1 уровень доступен когда личный баланс выше 1000$ и оборот структуры выше 3000$ 
            ➡️2 уровень доступен когда оборот структуры выше 5000$
            ➡️3 уровень доступен когда оборот структуры выше 10000$
            '''
    else:
        if refer_name:
            message_refers = f"""
        🔍Earn income in USDT by inviting partners using a referral link.
            \n 🔗Referral link: https://t.me/parser245bot?start={query.from_user.id}
            ❌1 level: 7%
            ❌2 level: 5%
            ❌level 3: 3%
            👤Invited:
            Level 1: {count} - 0.0 USDT
            Level 2: 0 - 0 USDT
            Level 3: 0 - 0 USDT
            💵Earned from referrals:
            Level 1: 0.0 USDT
            Level 2: 0.0 USDT
            Level 3: 0.0 USDT
            Top up your account with 1000 USDT to open an affiliate program
            👥Your inviter: None
            ➡️Level 1 is available when the personal balance is above $1000 and the structure’s turnover is above $3000
            ➡️Level 2 is available when the structure’s turnover is above $5000
            ➡️Level 3 is available when the structure’s turnover is above $10,000
        """
        else:
            message_refers = f"""
        🔍Earn income in USDT by inviting partners using a referral link.
            \n 🔗Referral link: https://t.me/parser245bot?start={query.from_user.id}
            ❌1 level: 7%
            ❌2 level: 5%
            ❌level 3: 3%
            👤Invited:
            Level 1: {count} - 0.0 USDT
            Level 2: 0 - 0 USDT
            Level 3: 0 - 0 USDT
            💵Earned from referrals:
            Level 1: 0.0 USDT
            Level 2: 0.0 USDT
            Level 3: 0.0 USDT
            Top up your account with 1000 USDT to open an affiliate program
            👥Your inviter: {refer_name}
            ➡️Level 1 is available when the personal balance is above $1000 and the structure’s turnover is above $3000
            ➡️Level 2 is available when the structure’s turnover is above $5000
            ➡️Level 3 is available when the structure’s turnover is above $10,000"""
    await bot.send_message(user_id,message_refers)

@dp.callback_query(MyCallback.filter(F.foo == "continue"))
async def my_callback_rda(query: types.CallbackQuery, callback_data: MyCallback):
    chat_id = query.from_user.id
    user_language = await get_user_language(chat_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    keyboard = startkeyboard(language=user_language)

    await bot.send_message(chat_id,phrases_dict['welcome_message'],reply_markup=keyboard)

@dp.callback_query(MyCallback.filter(F.foo == "vivod"))
async def my_callback_rda(query: types.CallbackQuery, callback_data: MyCallback):
    user_id = query.from_user.id
    await bot.send_message(user_id,'Какую валюту вы хотите вывести?',reply_markup=VIBORVIVOD123())


@dp.callback_query(MyCallback.filter(F.foo == "USDTVIVOD"))
async def my_callback_rda(query: types.CallbackQuery, callback_data: MyCallback):
    user_id = query.from_user.id
    user_messages2[user_id] = {'waiting_for_message': True}

    cur.execute("SELECT balance FROM refers WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]

    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    if current_balance == 0.0:
        await bot.send_message(user_id, phrases_dict['zero_balance_error'])
        user_messages2[user_id] = {'waiting_for_message': False}
    else:
        await bot.send_message(user_id, phrases_dict['withdrawal_amount_prompt'].format(current_balance))

def is_waiting_for_message(message: types.Message) -> bool:
    user_id = message.from_user.id
    return user_messages2.get(user_id, {}).get('waiting_for_message', False)

@dp.message(is_waiting_for_message)
async def handle_saved_message(message: types.Message):
    user_id = message.from_user.id

    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    
    if message.text.lower() == "cancel":
        user_messages2[user_id]['waiting_for_message'] = False
        await message.answer("Операция отменена.")
        return
    
    while True:
        try:
            saved_message = int(message.text)
            break
        except ValueError:
            await message.answer(phrases_dict['withdrawal_amount_error'])
            return

    cur.execute("SELECT balance FROM refers WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]

    if current_balance < saved_message:
        await message.answer(phrases_dict['insufficient_balance_error'])
        return

    updated_balance = current_balance - saved_message

    cur.execute("UPDATE refers SET balance=? WHERE user_id=?", (updated_balance, user_id))
    con.commit()

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
    cur.execute("INSERT INTO history (user_id, username, summa_vivoda, data_vivoda) VALUES (?, ?, ?, ?)", (user_id, message.from_user.username, saved_message, current_datetime))
    con.commit()

    user_messages2[user_id]['waiting_for_message'] = False

    await message.answer(phrases_dict['withdrawal_request_sent'].format(saved_message))

@dp.callback_query(MyCallback.filter(F.foo == "RUBVIVOD"))
async def my_callback_rda(query: types.CallbackQuery, callback_data: MyCallback):
    user_id = query.from_user.id
    user_messages9[user_id] = {'waiting_for_message': True}

    cur.execute("SELECT balance_RUB FROM refers WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]

    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    if current_balance == 0.0:
        await bot.send_message(user_id, phrases_dict['zero_balance_error'])
        user_messages9[user_id] = {'waiting_for_message': False}
    else:
        await bot.send_message(user_id, phrases_dict['withdrawal_amount_prompt'].format(current_balance))

def is_waiting_for_message(message: types.Message) -> bool:
    user_id = message.from_user.id
    return user_messages9.get(user_id, {}).get('waiting_for_message', False)

@dp.message(is_waiting_for_message)
async def handle_saved_message(message: types.Message):
    user_id = message.from_user.id

    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    
    if message.text.lower() == "cancel":
        user_messages9[user_id]['waiting_for_message'] = False
        await message.answer("Операция отменена.")
        return
    
    while True:
        try:
            saved_message = int(message.text)
            break
        except ValueError:
            await message.answer(phrases_dict['withdrawal_amount_error'])
            return

    cur.execute("SELECT balance_RUB FROM refers WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]

    if current_balance < saved_message:
        await message.answer(phrases_dict['insufficient_balance_error'])
        return

    updated_balance = current_balance - saved_message

    cur.execute("UPDATE refers SET balance_RUB=? WHERE user_id=?", (updated_balance, user_id))
    con.commit()

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
    cur.execute("INSERT INTO history (user_id, username, summa_vivoda, data_vivoda) VALUES (?, ?, ?, ?)", (user_id, message.from_user.username, saved_message, current_datetime))
    con.commit()

    user_messages9[user_id]['waiting_for_message'] = False

    await message.answer(phrases_dict['withdrawal_request_sent2'].format(saved_message))

async def check_channel_subscription(user_id: int):
    try:

        chat_member = await bot.get_chat_member(chat_id=-1001991232896, user_id=user_id)

        return chat_member.status == 'member'
    except Exception as e:
        print(f"Ошибка при проверке подписки на канал: {e}") 
        return False

@dp.callback_query(MyCallback.filter((F.foo == 'Russia') | (F.foo == 'English')))
async def my_callback_rda(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    selected_language = callback_data.foo
    
    with sq.connect('refers.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM refers WHERE user_id = ?", (user_id,))
        existing_entry = cur.fetchone()
        if existing_entry:
            cur.execute("UPDATE refers SET language = ? WHERE user_id = ?", (selected_language, user_id))
        con.commit()
    
    await query.answer("Your language has been saved successfully!")

    await query.message.delete()
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
     
    await bot.send_message(user_id, phrases_dict['welcome_message'], reply_markup=startkeyboard(user_language))

@dp.callback_query(MyCallback.filter(F.foo == "Change"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id,phrases_dict['change_language'],reply_markup=language())

@dp.callback_query(MyCallback.filter(F.foo == "invest"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    
    await bot.send_message(user_id,phrases_dict['vibor_invest'],reply_markup=invest(language=user_language))

@dp.callback_query(MyCallback.filter(F.foo == "tarifi"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    
    await bot.send_message(user_id,phrases_dict['vibor_tarif'],reply_markup=tarifi_keyboard(language=user_language))

@dp.callback_query(MyCallback.filter(F.foo == "dep"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_messages[user_id] = {'waiting_for_message': True}

    cur.execute("SELECT balance FROM refers WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]

    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id, phrases_dict['summa_popolneniya'])

    user_messages[user_id] = {'waiting_for_message': True}

def is_waiting_for_message(message: Message) -> bool:
    user_id = message.from_user.id

    return user_messages.get(user_id, {}).get('waiting_for_message', False)

@dp.message(is_waiting_for_message)
async def handle_saved_message(message: Message):
    user_id = message.from_user.id

    if message.text.lower() == "cancel":
        user_messages[user_id]['waiting_for_message'] = False
        await message.answer("Операция отменена.")
        return

    while True:
        try:
            saved_message = int(message.text)
            if saved_message <= 99:
                user_language = await get_user_language(user_id)
                if user_language == 'Russia':
                    phrases_dict = phrases['Russia']
                else:
                    phrases_dict = phrases['English']
                await message.answer(phrases_dict['vvedite100'])
                return  
            else:
                break
        except ValueError:
            await message.answer(phrases_dict['withdrawal_amount_error'])
            return  

    user_messages[user_id]['waiting_for_message'] = False
    user_messages[user_id]['saved_message'] = saved_message
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await message.answer(phrases_dict['sposob_oplati'],reply_markup=sposob_oplati(language=user_language))

@dp.callback_query(MyCallback.filter(F.foo == "kripta"))
async def check_subscription_callback(query: types.CallbackQuery):
    await query.message.answer('Выберите способ оплаты',reply_markup=USDQWE())
                               
@dp.callback_query(MyCallback.filter(F.foo == "rubles"))
async def check_subscription_callback(query: types.CallbackQuery):
    await query.message.answer('Выберите способ оплаты',reply_markup=USDQWE())

@dp.callback_query(MyCallback.filter(F.foo == "USDDP"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    saved_message = user_messages.get(user_id, {}).get('saved_message')
    if saved_message is not None:
        await bot.delete_message(chat_id=user_id, message_id=query.message.message_id)
         
        user_language = await get_user_language(user_id)
        if user_language == 'Russia':
            phrases_dict = phrases['Russia']
        else:
            phrases_dict = phrases['English']
        await bot.send_message(user_id, phrases_dict['oplata'].format(USDT=saved_message))
        await bot.send_message(user_id, 'TQGo9Z5oiwiLCog7MceFjBN2yXAwZKG7oE',reply_markup=oplatil(language=user_language))
    else:
        await bot.send_message(user_id, 'Что-то пошло не так. Пожалуйста, попробуйте еще раз.')

@dp.callback_query(MyCallback.filter(F.foo == "USDC"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    saved_message = user_messages.get(user_id, {}).get('saved_message')
    if saved_message is not None:
        await bot.delete_message(chat_id=user_id, message_id=query.message.message_id)
         
        user_language = await get_user_language(user_id)
        if user_language == 'Russia':
            phrases_dict = phrases['Russia']
        else:
            phrases_dict = phrases['English']
        await bot.send_message(user_id, phrases_dict['oplatau'].format(USDS=saved_message))
        await bot.send_message(user_id, 'TQGo9Z5oiwiLCog7MceFjBN2yXAwZKG7oE',reply_markup=oplatil(language=user_language))
    else:
        await bot.send_message(user_id, 'Что-то пошло не так. Пожалуйста, попробуйте еще раз.')

@dp.callback_query(MyCallback.filter(F.foo == "oplatil"))
async def check_subscription_callback(query: types.CallbackQuery):    
    user_id = query.from_user.id
    saved_message = user_messages.get(user_id, {}).get('saved_message')
    if saved_message is not None:
        user = await bot.get_chat(user_id)
        user_language = await get_user_language(user_id)
        if user_language == 'Russia':
            phrases_dict = phrases['Russia']
        else:
            phrases_dict = phrases['English']
        message_to_admin = f"Пользователь {user.first_name} (ID: {user_id}) оплатил(а) сумму {saved_message}."

        await bot.send_message(Admin_Id, message_to_admin) 
        await bot.send_message(user_id,phrases_dict['info_oplata'],reply_markup=vernytsa(language=user_language))  

@dp.callback_query(MyCallback.filter(F.foo == "vernytsa"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await query.message.answer(phrases_dict['welcome_message'],reply_markup=startkeyboard(language=user_language))

@dp.callback_query(MyCallback.filter(F.foo == "proverka"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    is_subscribed = await check_channel_subscription(user_id)
    if is_subscribed:
        await bot.send_message(user_id, "Вы подписаны ✅",reply_markup=startkeyboard())
    else:
        await bot.send_message(user_id, "Вы не подписаны на наш канал ❌")

@dp.message(F.text == 'Изменить баланс')
async def change_cmd(message: types.Message):
    user_id = message.from_user.id
    user_messages[user_id] = {'waiting_for_chat_id': True}

    await message.answer("Введите chat_id пользователя которому вы хотите поменять баланс")

def is_waiting_for_chat_id(message: types.Message) -> bool:
    user_id = message.from_user.id
    return user_messages.get(user_id, {}).get('waiting_for_chat_id', False)

def is_waiting_for_destination_chat_id(message: types.Message) -> bool:
    user_id = message.from_user.id
    return user_messages.get(user_id, {}).get('waiting_for_destination_chat_id', False)

@dp.message(is_waiting_for_chat_id)
async def handle_chat_id(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.text

    user_messages[user_id]['chat_id'] = chat_id
    user_messages[user_id]['waiting_for_chat_id'] = False
    user_messages[user_id]['waiting_for_destination_chat_id'] = True

    await message.answer("Теперь введите сумму на которую вы хотите поменять")

@dp.message(is_waiting_for_destination_chat_id)
async def handle_destination_chat_id(message: types.Message):
    user_id = message.from_user.id
    destination_chat_id = message.text

    user_messages[user_id]['destination_chat_id'] = destination_chat_id
    user_messages[user_id]['waiting_for_destination_chat_id'] = False
    user_messages[user_id]['amount'] = destination_chat_id
    await message.answer('Выберите валюту на которую хотите поменять',reply_markup=VIBORPOPOL())
    
@dp.callback_query(MyCallback.filter(F.foo == "usdt"))
async def history(query: types.CallbackQuery):
    user_id = query.from_user.id
    destination_chat_id = user_messages[user_id]['amount']
    
    cur.execute('SELECT * FROM refers WHERE user_id = ?', (user_messages[user_id]['chat_id'],))
    existing_user = cur.fetchone()
    user_chat = existing_user[3]
    if user_chat == None:
        username = existing_user[2]
        cur.execute('SELECT balance FROM refers WHERE user_id = ?', (user_messages[user_id]['chat_id'],))
        current_balance = cur.fetchone()[0] 
        new_balance = current_balance + int(destination_chat_id)  
        cur.execute('UPDATE refers SET balance = ? WHERE user_id = ?', (new_balance, user_messages[user_id]['chat_id']))

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
        cur.execute("""INSERT INTO history (user_id, username, summa_popolnenie, data_popolnenite) 
                       VALUES (?, ?, ?, ?)""", (user_messages[user_id]['chat_id'], username, destination_chat_id, current_datetime))
        con.commit()

        await query.message.answer(f"Баланс пользователя {user_messages[user_id]['chat_id']} успешно изменен. Общая сумма: {new_balance}")
    else: 
        username = existing_user[2]
        refer_id = existing_user[3]  # Получаем ID пользователя, который пригласил текущего пользователя
        refer_bonus = int(destination_chat_id) * 0.1  # Вычисляем бонус для реферера (10% от пополнения)
        
        # Обновляем баланс текущего пользователя
        cur.execute('SELECT balance FROM refers WHERE user_id = ?', (user_messages[user_id]['chat_id'],))
        current_balance = cur.fetchone()[0] 
        new_balance = current_balance + int(destination_chat_id)  
        cur.execute('UPDATE refers SET balance = ? WHERE user_id = ?', (new_balance, user_messages[user_id]['chat_id']))
        
        # Получаем старое значение Vigoda_Ref
        cur.execute('SELECT Vigoda_Ref FROM refers WHERE user_id = ?', (refer_id,))
        old_refer_vigoda = cur.fetchone()[0]
        
        # Начисляем бонус рефереру
        cur.execute('SELECT balance FROM refers WHERE user_id = ?', (refer_id,))
        refer_balance = cur.fetchone()[0]
        new_refer_balance = refer_balance + refer_bonus
        cur.execute('UPDATE refers SET balance = ? WHERE user_id = ?', (new_refer_balance, refer_id))
        
        # Обновляем выгоду для реферера
        new_refer_vigoda = old_refer_vigoda + refer_bonus
        cur.execute('UPDATE refers SET Vigoda_Ref = ? WHERE user_id = ?', (new_refer_vigoda, refer_id))
        con.commit()
        
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
        cur.execute("""INSERT INTO history (user_id, username, summa_popolnenie, data_popolnenite) 
                       VALUES (?, ?, ?, ?)""", (user_messages[user_id]['chat_id'], username, destination_chat_id, current_datetime))
        con.commit()

        await query.message.answer(f"Баланс пользователя {user_messages[user_id]['chat_id']} успешно изменен. Общая сумма: {new_balance}")

@dp.callback_query(MyCallback.filter(F.foo == "rublesp"))
async def handle_rubles_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    destination_chat_id = user_messages[user_id]['amount']
    
    cur.execute('SELECT * FROM refers WHERE user_id = ?', (user_messages[user_id]['chat_id'],))
    existing_user = cur.fetchone()
    user_chat = existing_user[3]
    if user_chat == None:
        username = existing_user[2]
        cur.execute('SELECT balance_RUB FROM refers WHERE user_id = ?', (user_messages[user_id]['chat_id'],))  # Запрос для баланса в RUB
        current_balance = cur.fetchone()[0] 
        new_balance = current_balance + int(destination_chat_id)  
        cur.execute('UPDATE refers SET balance_RUB = ? WHERE user_id = ?', (new_balance, user_messages[user_id]['chat_id']))  # Обновляем баланс в RUB

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
        cur.execute("""INSERT INTO history (user_id, username, summa_popolnenie_RUB, data_popolnenite) 
                       VALUES (?, ?, ?, ?)""", (user_messages[user_id]['chat_id'], username, destination_chat_id, current_datetime))
        con.commit()

        await query.message.answer(f"Баланс пользователя {user_messages[user_id]['chat_id']} в рублях успешно изменен. Общая сумма: {new_balance}")
    else: 
        username = existing_user[2]
        refer_id = existing_user[3]  # Получаем ID пользователя, который пригласил текущего пользователя
        refer_bonus = int(destination_chat_id) * 0.1  # Вычисляем бонус для реферера (10% от пополнения)
        
        # Обновляем баланс текущего пользователя
        cur.execute('SELECT balance_RUB FROM refers WHERE user_id = ?', (user_messages[user_id]['chat_id'],))  # Запрос для баланса в RUB
        current_balance = cur.fetchone()[0] 
        new_balance = current_balance + int(destination_chat_id)  
        cur.execute('UPDATE refers SET balance_RUB = ? WHERE user_id = ?', (new_balance, user_messages[user_id]['chat_id']))  # Обновляем баланс в RUB
        
        # Получаем старое значение Vigoda_Ref
        cur.execute('SELECT Vigoda_Ref FROM refers WHERE user_id = ?', (refer_id,))
        old_refer_vigoda = cur.fetchone()[0]
        
        # Начисляем бонус рефереру
        cur.execute('SELECT balance_RUB FROM refers WHERE user_id = ?', (refer_id,))
        refer_balance = cur.fetchone()[0]
        new_refer_balance = refer_balance + refer_bonus
        cur.execute('UPDATE refers SET balance_RUB = ? WHERE user_id = ?', (new_refer_balance, refer_id))  # Обновляем баланс в RUB для реферера
        
        # Обновляем выгоду для реферера
        new_refer_vigoda = old_refer_vigoda + refer_bonus
        cur.execute('UPDATE refers SET Vigoda_Ref = ? WHERE user_id = ?', (new_refer_vigoda, refer_id))
        con.commit()
        
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
        cur.execute("""INSERT INTO history (user_id, username, summa_popolnenie_RUB, data_popolnenite) 
                       VALUES (?, ?, ?, ?)""", (user_messages[user_id]['chat_id'], username, destination_chat_id, current_datetime))
        con.commit()

        await query.message.answer(f"Баланс пользователя {user_messages[user_id]['chat_id']} в рублях успешно изменен. Общая сумма: {new_balance}")


@dp.callback_query(MyCallback.filter(F.foo == "history_vivod"))
async def history(query: types.CallbackQuery):
    user_id = query.from_user.id
    popolnenie_history = []
    vivod_history = []
    with sq.connect('refers.db') as con:
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, user_id INTEGER, summa_popolnenie INTEGER, summa_vivoda INTEGER, date_popolnenie TEXT, date_vivoda TEXT)")

        cur.execute("SELECT * FROM history WHERE user_id=? AND summa_popolnenie > 0 ORDER BY id DESC", (user_id,))
        rows = cur.fetchall()
        for index, row in enumerate(rows, start=1):
            popolnenie_history.append((index,) + row[1:])

        cur.execute("SELECT * FROM history WHERE user_id=? AND summa_vivoda > 0 ORDER BY id DESC", (user_id,))
        rows = cur.fetchall()
        for index, row in enumerate(rows, start=1):
            vivod_history.append((index,) + row[1:])
    
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']

    message = phrases_dict['history_message'] + "\n"
    if popolnenie_history:
        message += phrases_dict['replenishment_history'] + "\n"
        for row in popolnenie_history:
            if user_language == 'Russia':
                message += f"ID: {row[0]}, Сумма пополнения: {row[3]}, Дата пополнения: {row[4]}\n"
            else:
                message += f"ID: {row[0]}, {phrases['English']['replenishment_amount']}: {row[3]}, {phrases['English']['replenishment_date']}: {row[4]}\n"
    else:
        message += phrases_dict['no_replenishment_history'] + "\n"
    
    if vivod_history:
        message += phrases_dict['withdrawal_history'] + "\n"
        for row in vivod_history:
            if user_language == 'Russia':
                message += f"ID: {row[0]}, Сумма вывода: {row[5]}, Дата вывода: {row[6]}\n"
            else:
                message += f"ID: {row[0]}, {phrases['English']['withdrawal_amount']}: {row[5]}, {phrases['English']['withdrawal_date']}: {row[6]}\n"
    else:
        message += phrases_dict['no_withdrawal_history']
    
    await bot.send_message(user_id, message)

@dp.callback_query(MyCallback.filter(F.foo == "month"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    await bot.send_message(user_id,'В какой валюте вы хотите инвестировать?',reply_markup=VIBORvaluti())

@dp.callback_query(MyCallback.filter(F.foo == "usdtvaluta"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_messages3[user_id] = {'waiting_for_message': True, 'tariff': '1 month 20%'}
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id, phrases_dict['summa_vvedeniya'])

@dp.callback_query(MyCallback.filter(F.foo == "rublesvaluta"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_messages6[user_id] = {'waiting_for_message': True, 'tariff': '1 month 20%'}
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id, phrases_dict['summa_vvedeniya'])

@dp.callback_query(MyCallback.filter(F.foo == "month3"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    await bot.send_message(user_id,'В какой валюте вы хотите инвестировать?',reply_markup=VIBORvaluti2())

@dp.callback_query(MyCallback.filter(F.foo == "usdtvaluta2"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_messages4[user_id] = {'waiting_for_message': True, 'tariff': '3 month 80%'}
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id, phrases_dict['summa_vvedeniya'])

@dp.callback_query(MyCallback.filter(F.foo == "rublesvaluta2"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_messages7[user_id] = {'waiting_for_message': True, 'tariff': '3 month 80%'}
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id, phrases_dict['summa_vvedeniya'])

@dp.callback_query(MyCallback.filter(F.foo == "month6"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    await bot.send_message(user_id,'В какой валюте вы хотите инвестировать?',reply_markup=VIBORvaluti3())


@dp.callback_query(MyCallback.filter(F.foo == "usdtvaluta3"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_messages5[user_id] = {'waiting_for_message': True, 'tariff': '6 month 200%'}
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id, phrases_dict['summa_vvedeniya'])

@dp.callback_query(MyCallback.filter(F.foo == "rublesvaluta3"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_messages8[user_id] = {'waiting_for_message': True, 'tariff': '6 month 200%'}
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id, phrases_dict['summa_vvedeniya'])

def is_waiting_for_message_usdt(message: types.Message) -> bool:
    user_id = message.from_user.id
    return (user_messages3.get(user_id, {}).get('waiting_for_message', False) or 
            user_messages4.get(user_id, {}).get('waiting_for_message', False) or 
            user_messages5.get(user_id, {}).get('waiting_for_message', False))

def is_waiting_for_message(message: types.Message) -> bool:
    user_id = message.from_user.id
    return (user_messages6.get(user_id, {}).get('waiting_for_message', False) or 
            user_messages7.get(user_id, {}).get('waiting_for_message', False) or 
            user_messages8.get(user_id, {}).get('waiting_for_message', False))

@dp.message(is_waiting_for_message)
async def handle_saved_message(message: types.Message):
    user_id = message.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    while True:
        try:
            saved_message = int(message.text)
            break
        except ValueError:
            await message.answer(phrases_dict['withdrawal_amount_error'])
            return
    
    tariff = None
    for user_messages in [user_messages6, user_messages7, user_messages8]:
        if user_id in user_messages:
            tariff = user_messages[user_id]['tariff']
            del user_messages[user_id]
            break

    if tariff is None:
        await message.answer("Ошибка. Попробуйте снова.")
        return

    cur.execute("SELECT balance_RUB FROM refers WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]

    if current_balance < saved_message:
        await message.answer(phrases_dict['insufficient_balance_error'])
        return

    new_balance = current_balance - saved_message
    cur.execute("UPDATE refers SET balance_RUB=? WHERE user_id=?", (new_balance, user_id))
    con.commit()

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    data_prib = datetime.datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    valuta = 'RUB'
    cur.execute("INSERT INTO activi (user_id, username, tarif, summaN, summaT, data_priobreteniya, data_konec,data_pribavleniya,Valuta) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)",
                    (user_id, message.from_user.first_name, tariff, saved_message, saved_message, current_date, end_date,data_prib,valuta))
    con.commit()

    await message.answer(phrases_dict['tariff_purchased2'].format(tariff=tariff, saved_message=saved_message))


@dp.callback_query(MyCallback.filter(F.foo == "history"))
async def check_history_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    await bot.send_message(user_id,phrases_dict['odin_var'],reply_markup=vnhistory_keyboard(language=user_language))

@dp.callback_query(MyCallback.filter(F.foo == 'historytarif'))
async def historytarif_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    cur.execute("SELECT tarif, summaN, summaT, data_priobreteniya FROM activi WHERE user_id = ?", (user_id,))
    data = cur.fetchall()

    if not data:
        await bot.send_message(user_id,phrases_dict['net_historytarif'])
    else:
        message = phrases_dict['history_messagetarif'] + "\n"
        for row in data: 
            tarif, summaN, summaT, data_priobreteniya = row
            profit = round(summaT - summaN, 2)
            today_date = datetime.date.today().strftime("%d.%m.%Y")
            message += f"{phrases_dict['tariff']}: {tarif}\n" 
            message += f"{phrases_dict['123initial_amount']} {summaN} USD\n"  
            message += f"{phrases_dict['profitna']} {today_date}: {profit} USD\n" 
            message += f"{phrases_dict['obj_summa']} {summaT} USD\n\n"  
    await bot.send_message(user_id,message)

@dp.message(is_waiting_for_message_usdt)
async def handle_saved_message(message: types.Message):
    user_id = message.from_user.id
    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    while True:
        try:
            saved_message = int(message.text)
            break
        except ValueError:
            await message.answer(phrases_dict['withdrawal_amount_error'])
            return
    
    tariff = None
    for user_messages in [user_messages3, user_messages4, user_messages5]:
        if user_id in user_messages:
            tariff = user_messages[user_id]['tariff']
            del user_messages[user_id]
            break

    if tariff is None:
        await message.answer("Ошибка. Попробуйте снова.")
        return

    cur.execute("SELECT balance FROM refers WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]

    if current_balance < saved_message:
        await message.answer(phrases_dict['insufficient_balance_error'])
        return

    new_balance = current_balance - saved_message
    cur.execute("UPDATE refers SET balance=? WHERE user_id=?", (new_balance, user_id))
    con.commit()

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    data_prib = datetime.datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    valuta = 'USDT'
    cur.execute("INSERT INTO activi (user_id, username, tarif, summaN, summaT, data_priobreteniya, data_konec,data_pribavleniya,Valuta) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)",
                    (user_id, message.from_user.first_name, tariff, saved_message, saved_message, current_date, end_date,data_prib,valuta))
    con.commit()

    await message.answer(phrases_dict['tariff_purchased'].format(tariff=tariff, saved_message=saved_message))

@dp.callback_query(MyCallback.filter(F.foo == "bonuces"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id
    
    # Получаем количество приглашенных пользователей
    cur.execute("SELECT COUNT(*) FROM refers WHERE refer_id=?", (user_id,))
    count = cur.fetchone()[0]
    
    # Получаем выгоду реферала
    cur.execute("SELECT Vigoda_Ref FROM refers WHERE user_id=?", (user_id,))
    vigoda_ref = cur.fetchone()[0]
    
    await query.message.answer(f'Вы заработали {vigoda_ref} USD с {count} приглашенных пользователей.')


import datetime

@dp.callback_query(MyCallback.filter(F.foo == "activi"))
async def check_subscription_callback(query: types.CallbackQuery):
    user_id = query.from_user.id

    user_language = await get_user_language(user_id)
    if user_language == 'Russia':
        phrases_dict = phrases['Russia']
    else:
        phrases_dict = phrases['English']
    
    with sq.connect('refers.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM activi WHERE user_id=?", (user_id,))
        active_info = cur.fetchall()

    if active_info:
        message_text = phrases_dict['activity_info'] + "\n"  
        for index, row in enumerate(active_info, start=1):
            initial_amount = row[4]  
            current_amount = row[5]
            purchase_date = datetime.datetime.strptime(row[8], '%Y-%m-%d').date()   
            end_date = datetime.datetime.strptime(row[7], '%Y-%m-%d').date()
            today_date = datetime.date.today()
            if today_date >= end_date: 
                days_passed = (end_date - purchase_date).days
                if row[3] == "1 month 20%":
                    coefficient = 0.0065
                elif row[3] == "3 month 80%":
                    coefficient = 0.0095
                elif row[3] == "6 month 200%":
                    coefficient = 0.02
                else:
                    coefficient = 0  
                profit = initial_amount * coefficient * days_passed
                current_amount += profit
                current_amount = round(current_amount, 2)  
                balance = cur.execute("SELECT balance FROM refers WHERE user_id=?", (user_id,)).fetchone()[0]
                balance += profit
                cur.execute("UPDATE refers SET balance=? WHERE user_id=?", (balance, user_id))
                con.commit()
                await bot.send_message(user_id,f'Ваша подписка {row[6]} по тарифу {row[3]} сегодня истекла ')
                continue  

            if purchase_date != today_date:
                days_passed = (today_date - purchase_date).days
                if row[3] == "1 month 20%":
                    coefficient = random.choice([0.006,0.007])
                elif row[3] == "3 month 80%":
                    coefficient = random.choice([0.009,0.01])
                elif row[3] == "6 month 200%":
                    coefficient = random.choice([0.011,0.012,0.013])
                else:
                    coefficient = 0  
                profit = initial_amount * coefficient * days_passed
                current_amount += profit
                current_amount = round(current_amount, 2)  
            
            cur.execute("UPDATE activi SET summaT=?, data_pribavleniya=? WHERE id=?", (current_amount, today_date, row[0]))
            con.commit()
            currency_info = "RUB" if row[9] == "RUB" else "USDT"
            message_text += f"{index}. {phrases_dict['tariff']}: {row[3]}, {phrases_dict['initial_amount']}: {initial_amount} {currency_info}, {phrases_dict['current_amount']}: {current_amount} {currency_info}, {phrases_dict['purchase_date']}: {purchase_date}, {phrases_dict['end_date']}: {row[7]}\n"

        if message_text != phrases_dict['activity_info'] + "\n":
            await bot.send_message(user_id, message_text)
        else:
            await bot.send_message(user_id, phrases_dict['no_active_subs'])  
    else:
        await bot.send_message(user_id, phrases_dict['no_active_subs'])


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

asyncio.run(main())