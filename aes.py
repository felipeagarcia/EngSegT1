import math
from sbox import s_box

def encript (plain_text, key):
	key = key_expansion(key)
	rounds = 10
	print('encripting')
	text = text_to_matrix(plain_text)
	num_blocks = len(text)
	for n in range(num_blocks):
		for i in range(rounds):
			round_key = key[4*i : 4*i + 4]
			print('before',text[n])
			text[n] = SubBytes(text[n])
			print('sub', text[n])
			text[n] = ShiftRows(text[n])
			print('rot', text[n])
			MixColumns(text[n])
			AddRoundKey(text[n], round_key)
			print('text',text[n])
	return matrix_to_text(text)

def decript (encripted_text, key):
	encripted_text = encripted_text + "decripted"
	return encripted_text

def text_to_matrix(text):
	text_matrix = []
	text = list(text)
	#converting text to ascii
	text = [ord(x) for x in text]
	#converting ascii to hex
	text = [format(x, 'x') for x in text]
	#adding zero of hex numns of len = 1
	for i in range(len(text)):
		if(len(text[i]) == 1):
			text[i] = '0' + text[i]
	pos = 0
	for count in range(math.ceil(len(text)/16)):
		text_matrix.append([])
		for i in range(4):
			text_matrix[count].append([])
			for j in range(4):
				try:
					text_matrix[count][i].append(text[pos])
					pos = pos + 1
				except:
					text_matrix[count][i].append('00')
	return text_matrix

def matrix_to_text(text_matrix):
	text = []
	for count in range(len(text_matrix)):
		for i in range(4):
			for j in range(4):
				if text_matrix[count][i][j] != '00':
					text.append(text_matrix[count][i][j])
	text = [chr(int(x,16)) for x in text]
	return ''.join(text)


def key_expansion(key, num_bytes= 16):
	#separating key in a list
	key = list(key)
	#converting to hex
	key = [format(int(x), 'x') for x in key]
	#adding '0' when necessary
	for i in range(len(key)):
		if(len(key[i]) == 1):
			key[i] = '0' + key[i]
	n = len(key)
	if n > num_bytes :
		print("The key is larger than the value allowed")
		exit(-1)
	elif (n < num_bytes):
		print("key size is incorrect")
		exit(-1)
	rc = ['01', '02', '04', '08', '10', '20',
		  '40', '80', '1B', '36', '6c', 'd8']
	#round constant
	rcon = [ x + '000000' for x in rc]
	word = []
	for i in range(4):
		word.append(key[4*i] + key[4*i + 1] +
					key[4*i + 2] + key[4*i + 3]
					)
	for i in range(4, 44):
		temp = word[i - 1]
		if (i % 4 == 0):
			temp = int(sub_word(rot_word(temp, 2)),16) ^ int(rcon[int(i/4)], 16)
		else:
			temp = int(word[i - 1], 16)
		word.append(format((int(word[i-4],16) ^ temp), 'x'))
	return word

def rot_word(word, n):
    return word[n:] + word[:n]

def sub_word(word):
	l = []
	print(word)
	for i in range(4):
		l.append(format(s_box[int((word)[i*2:i*2 + 1], 16) * 16 +  int((word)[i*2 + 1:i*2 + 2], 16) ], 'x'))
	return ''.join(l)

def SubBytes(text):
	#adding zero of hex numns of len = 1
	for i in range(4):
		for j in range(4):
			if(len(text[i][j]) == 1):
				text[i][j] = '0' + text[i][j]
	for i in range(4):
		for j in range(4):
			text[i][j] = format(s_box[int((text[i][j])[0:1] , 16) * 16 + int((text[i][j])[1:2], 16)] , 'x')
	return text

def ShiftRows(text):
	i = 0
	for i in range(4):
		text[i] = rot_word(text[i], i)
	return text

def MixColumns(plain_text):
	return plain_text

def AddRoundKey(plain_text, key):
	return plain_text