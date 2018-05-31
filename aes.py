import math
from sbox import s_box, inv_s_box

def encript (plain_text, key):
	'encript the plain text using the key'
	print(key)
	mode = 0
	key = key_expansion(key)
	rounds = 10
	print('encripting')
	text = text_to_matrix(plain_text)
	num_blocks = len(text)
	for n in range(num_blocks):
		for i in range(rounds):
			round_key = calc_round_key(key, i)
			text[n] = SubBytes(text[n], mode)
			text[n] = ShiftRows(text[n], mode)
			text[n] = MixColumns(text[n], mode)
			text[n] = AddRoundKey(text[n], round_key)
	print(text)
	return matrix_to_text(text)

def decript (encripted_text, key):
	'decript the cipher text using the key'
	print(key)
	mode = 1
	key = key_expansion(key)
	rounds = 10
	print('decripting')
	text = text_to_matrix(encripted_text)
	num_blocks = len(text)
	for n in range(num_blocks):
		for i in range(rounds):
			round_key = calc_round_key(key, i)
			text[n] = SubBytes(text[n], mode)
			text[n] = ShiftRows(text[n], mode)
			text[n] = MixColumns(text[n], mode)
			text[n] = AddRoundKey(text[n], round_key)
	print(text)
	return matrix_to_text(text)

def calc_round_key(key, num_round):
	'calculates the round key'
	round_key = key[4*num_round : 4*num_round + 4]
	l = []
	for i in range(4):
		l.append([])
		for j in range(4):
			l[i].append(round_key[i][2*j:2*j + 2])
	return l

def text_to_matrix(text):
	'converts a string to a matrix of hex'
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
	'converts a hex matrix to a single string'
	text = []
	for count in range(len(text_matrix)):
		for i in range(4):
			for j in range(4):
				if text_matrix[count][i][j] != '00':
					text.append(text_matrix[count][i][j])
	text = [chr( int(x,16) ) for x in text]
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

def inv_rot_word(word, n):
	return word[4 - n:] + word[: 4 - n]

def sub_word(word):
	l = []
	#apply the sbox
	for i in range(4):
		l.append(format(s_box[int((word)[i*2:i*2 + 1], 16) * 16 +  int((word)[i*2 + 1:i*2 + 2], 16) ], 'x'))
	#return a string
	return ''.join(l)

def mult_gf(a, b):
	'multiplication in gf(2^8)'
	#this function is probably incorrect
	if (format(a, 'b')[0] == '0'):
		return a
	else:
		a = format(a, 'x')
		a = rot_word(a, 1)
		a = format(int(a, 16) ^ int('00011011', 2), 'x')
		a = int(a, 16)
		if b > 1:
			mult_gf(a, b - 1)
		return a

def SubBytes(text, mode):
	'use sboxes to replace bytes'
	#adding zero of hex numns of len = 1
	for i in range(4):
		for j in range(4):
			if(len(text[i][j]) == 1):
				text[i][j] = '0' + text[i][j]
	if mode == 0: #encript
		#applying the sbox for each byte
		for i in range(4):
			for j in range(4):
				text[i][j] = format(s_box[int((text[i][j])[0:1] , 16) * 16 + int((text[i][j])[1:2], 16)] , 'x')
	else: #decript
		#applying the inv_sbox for each byte
		for i in range(4):
			for j in range(4):
				text[i][j] = format(inv_s_box[int((text[i][j])[0:1] , 16) * 16 + int((text[i][j])[1:2], 16)] , 'x')
	return text

def ShiftRows(text, mode):
	i = 0
	#shifting each row in i positions
	if(mode == 0): #encript
		for i in range(4):
			text[i] = rot_word(text[i], i)
	else: #decript
		for i in range(4):
			text[i] = inv_rot_word(text[i], i)
	return text

def MixColumns(text, mode):
	#converting the text to int, to use on the xor operations
	#esta funcao esta provavelmente incorreta, verificar aritmetica de corpo finito para multiplicacao
	for i in range(4):
		for j in range(4):
			text[i][j] = int(text[i][j], 16)
	aux = text
	if(mode == 0): #encript
		for j in range(4):
			text[0][j] = mult_gf(aux[0][j], 2) ^ mult_gf(aux[1][j], 3) ^ mult_gf(aux[2][j], 1) ^ mult_gf(aux[3][j], 1)
			text[1][j] = mult_gf(aux[0][j], 1) ^ mult_gf(aux[1][j], 2) ^ mult_gf(aux[2][j], 3) ^ mult_gf(aux[3][j], 1)
			text[2][j] = mult_gf(aux[0][j], 1) ^ mult_gf(aux[1][j], 1) ^ mult_gf(aux[2][j], 2) ^ mult_gf(aux[3][j], 3)
			text[3][j] = mult_gf(aux[0][j], 3) ^ mult_gf(aux[1][j], 1) ^ mult_gf(aux[2][j], 1) ^ mult_gf(aux[3][j], 2)
	else: #decript
		for j in range(4):
			text[0][j] = mult_gf(aux[0][j], 0x0E) ^ mult_gf(aux[1][j], 0x0B) ^ mult_gf(aux[2][j], 0x0D) ^ mult_gf(aux[3][j], 0x09)
			text[1][j] = mult_gf(aux[0][j], 0x09) ^ mult_gf(aux[1][j], 0x0E) ^ mult_gf(aux[2][j], 0x0B) ^ mult_gf(aux[3][j], 0x0D)
			text[2][j] = mult_gf(aux[0][j], 0x0D) ^ mult_gf(aux[1][j], 0x09) ^ mult_gf(aux[2][j], 0x0E) ^ mult_gf(aux[3][j], 0x0B)
			text[3][j] = mult_gf(aux[0][j], 0x0B) ^ mult_gf(aux[1][j], 0x0D) ^ mult_gf(aux[2][j], 0x09) ^ mult_gf(aux[3][j], 0x0E)
	#converting the text back to hex
	for i in range(4):
		for j in range(4):
			text[i][j] = format(text[i][j], 'x')
	return text

def AddRoundKey(text, key):
	'xor between the text and the round key'
	for i in range(4):
		for j in range(4):
			text[i][j] = format( int( text[i][j], 16) ^ int( key[i][j], 16) , 'x')
	return text