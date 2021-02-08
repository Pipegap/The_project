import csv
import telebot
from telebot import types
import datetime




bot = telebot.TeleBot("1530077921:AAGeapWSK817Uf85GiJoQOUY0xTEdrxZo1o")
date = ""
remove_board = types.ReplyKeyboardRemove()
homework = ""
subject = ""
password = "1234"
Ychenic_subject = ""
@bot.message_handler(commands = ['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Учитель")
	item2 = types.KeyboardButton("Ученик")
	markup.add(item1, item2)

	bot.send_message(message.chat.id, "Кто вы?", reply_markup=markup)
@bot.message_handler(content_types = ['text'])
def working(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Математика")
	item2 = types.KeyboardButton("Русский язык")
	item3 = types.KeyboardButton("Химия")
	item4 = types.KeyboardButton("Физика")
	item5 = types.KeyboardButton("История")
	item6 = types.KeyboardButton("Биология")
	markup.add(item1, item2, item3, item4, item5, item6)
	if message.text == 'Учитель':
		bot.send_message(message.chat.id, "Введите пароль!", reply_markup=remove_board)
		bot.register_next_step_handler(message, get_password)
	if message.text == 'Ученик':
		bot.send_message(message.chat.id, "Выбирите предмет", reply_markup=markup)
		bot.register_next_step_handler(message, get_date_range)
@bot.message_handler(content_types = ['text'])
def get_date_range(message):
	global Ychenic_subject
	Ychenic_subject = message.text
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Все активные домашние задания.")
	item2 = types.KeyboardButton("Ближайшее домашнее задание.")
	markup.add(item1,item2)
	bot.send_message(message.chat.id, "Вы выбрали предмет - " + Ychenic_subject, reply_markup=markup)
	print("Задание выбрано!")
	bot.register_next_step_handler(message, get_homework)
@bot.message_handler(content_types = ['text'])
def get_homework(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Математика")
	item2 = types.KeyboardButton("Русский язык")
	item3 = types.KeyboardButton("Химия")
	item4 = types.KeyboardButton("Физика")
	item5 = types.KeyboardButton("История")
	item6 = types.KeyboardButton("Биология")
	item7 = types.KeyboardButton("Вернуться к выбору роли.")
	markup.add(item1, item2, item3, item4, item5, item6, item7)

	markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item = types.KeyboardButton("Учитель")
	item_two = types.KeyboardButton("Ученик")
	markup2.add(item, item_two)
	global Ychenic_subject
	today = datetime.datetime.today()
	base = 0
	x = []
	y = datetime.datetime.strptime("01.01.9999", "%d.%m.%Y")
	with open('data_base.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		if message.text ==  "Все активные домашние задания.":
			print("Выбрано все активные домашние задния!")
			for row in reader:
				row_date = datetime.datetime.strptime(row['date'], "%d.%m.%Y")
				if (Ychenic_subject + ".") == row['subject'] and row_date > today:
					bot.send_message(message.chat.id, row['date'] + row['homework'], reply_markup=markup)
					bot.register_next_step_handler(message, get_date_range)
					base = 1
		#if message.text == "Вернуться к выбору роли.":
		#	message.text = "/start"
		#	bot.send_message(message.chat.id, "Кто вы?", reply_markup=markup2)
		#	bot.register_next_step_handler(message, working)
			if base == 0:
				bot.send_message(message.chat.id, "Заданий на " + Ychenic_subject + " нет", reply_markup=markup)
				bot.send_message(message.chat.id, "Выбирите другой предмет.")
				bot.register_next_step_handler(message, get_date_range)
		if message.text == "Ближайшее домашнее задание.":
			print("Выбрано ближайшее домашние задание!")
			for row in reader:
				row_date = datetime.datetime.strptime(row['date'], "%d.%m.%Y")
				if (Ychenic_subject + ".") == row['subject'] and row_date > today:
					x.append(row_date)
			y = min(x)
			reader2 = csv.DictReader(csvfile)
			csvfile.seek(0)
			for row1 in reader2:
				row_date2 = datetime.datetime.strptime(row1['date'], "%d.%m.%Y")
				if (Ychenic_subject + ".") == row1['subject'] and row_date2 == y:
					bot.send_message(message.chat.id, row1["subject"] + row1["homework"])

def get_password(message):
	if message.text == password:
		bot.send_message(message.chat.id, "Вы учитель. Теперь вы можете задать задание вашему классу! Укажите срок сдачи в формате ДД.ММ.ГГГГ." )
		bot.register_next_step_handler(message, write_date)
	else:
		bot.send_message(message.chat.id, "Пароль не верный. Попробуйте ещё раз.")
		bot.register_next_step_handler(message, get_password)
@bot.message_handler(content_types=['text'])
def write_date(message):
	global date
	try:
		y = datetime.datetime.strptime(message.text, "%d.%m.%Y")
		date = message.text

		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("Математика.")
		item2 = types.KeyboardButton("Русский язык.")
		item3 = types.KeyboardButton("Химия.")
		item4 = types.KeyboardButton("Физика.")
		item5 = types.KeyboardButton("История.")
		item6 = types.KeyboardButton("Биология.")
		markup.add(item1, item2, item3, item4, item5, item6)

		bot.send_message(message.chat.id, "Срок здачи - " + date)
		bot.send_message(message.chat.id, "Теперь укажите предмет, по которому вы задаёте домашние задание.",
						 reply_markup=markup)
		bot.register_next_step_handler(message, write_subject)
	except:
		bot.send_message(message.chat.id, "Неправильно введена дата. Попробуйте ущё раз!")
		bot.register_next_step_handler(message, write_date)


@bot.message_handler(content_types=['text'])
def write_subject(message):
	global subject
	subject = message.text

	bot.send_message(message.chat.id, "Предмет - " + subject)
	bot.send_message(message.chat.id, "Теперь можете записать всё ваше домашние задание для класса. ",  reply_markup=remove_board)
	bot.register_next_step_handler(message, write_homework)
@bot.message_handler(content_types=['text'])
def write_homework(message):
	global homework
	homework = message.text

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Вернуться к выбору роли.")
	item2 = types.KeyboardButton("Новое домашнее задание.")
	markup.add(item1, item2)

	bot.send_message(message.chat.id, "Домашние задание по  " + subject + " на " + date + " сохранено.", reply_markup=markup)
	now = datetime.datetime.now()
	with open('data_base.csv', mode='a') as data_file:
		data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		data_writer.writerow([date,subject,homework, now.strftime("%d-%m-%Y %H:%M")])
	bot.register_next_step_handler(message, return_to_start)

@bot.message_handler(content_types=['text'])
def return_to_start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Вернуться к выбору роли.")
	item2 = types.KeyboardButton("Новое домашнее задание.")
	markup.add(item1, item2)
	markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
	x = types.KeyboardButton("Учитель")
	y = types.KeyboardButton("Ученик")
	markup2.add(x, y)

	if message.text == "Вернуться к выбору роли.":
		message.text = '/start'
		bot.send_message(message.chat.id, "Кто вы?", reply_markup=markup2 )
		bot.register_next_step_handler(message, working)
	if message.text == "Новое домашнее задание.":
		bot.send_message(message.chat.id,"Теперь вы можете задать задание вашему классу! Укажите срок сдачи в формате ДД.ММ.ГГГГ.", reply_markup=remove_board)
		bot.register_next_step_handler(message, write_date)



bot.polling(none_stop = True)
