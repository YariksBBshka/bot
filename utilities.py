from telebot import types

def small_keyboard_creator(matrix_of_butts):
	keyboard = types.InlineKeyboardMarkup(row_width=len(matrix_of_butts))
	for i in range(len(matrix_of_butts)):
		butt = types.InlineKeyboardButton(matrix_of_butts[i][0], callback_data = matrix_of_butts[i][1])
		keyboard.add(butt)
	return keyboard

def large_keyboard_creator(list_of_butts,size=True, row=3):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=size, row_width = row)
	for key in list_of_butts:
		butt = types.KeyboardButton(key)
		keyboard.add(butt)
	return keyboard

def add_to_file(message,str):
	with open(f'temp_input_of_{message.chat.id}.txt','a',encoding='utf-16') as f:
		f.write(str+' ')
	return 0

def add_to_report(message,str):
	with open(f'temp_report_to_{message.chat.id}.txt','a',encoding='utf-16') as f:
		f.write(str+' ')
	return 0

def list_to_matrix(a,b):
	c=[]
	if len(a)==len(b):
		for i in range(len(a)):
			c.append([str(a[i]),str(b[i])])
		return c
	return 0

def file_to_matrix(file):
	with open(file,'r',encoding='utf-16') as t:
		matr = t.read().split('\n')
		matr.remove('')
		for i in range(len(matr)):
			matr[i] = matr[i].split()
		return matr

def matrix_sorting(matr,sort_type=0,):#sort_type: 0 - времени, 1 - знаку (типу), 2 - по валюте, 3 - сумме, 4 - категории
		for i in range(len(matr)):
			key = matr[i].pop(sort_type)
			matr[i].insert(0, key)
		matr = sorted(matr)
		for i in range(len(matr)):
			key = matr[i].pop(0)
			matr[i].insert(sort_type, key)
		return matr

def time_shorting(time):
	return time[4:7]+" "+time[8:10]