import numpy as np
from sbox import s_box

def encript (plain_text, key):
	plain_text = plain_text + "encripted"
	key = [0xEA,  0xD2, 0x73, 0x21, 0xB5, 0x8D, 0xBA, 0xD2, 0x31, 0x2B, 0xF5, 0x60, 0x7F, 0x8D, 0x29, 0x2F]
	print([hex(x) for x in key])
	key = key_expansion(key)
	print(key)
	return plain_text

def decript (encripted_text, key):
	encripted_text = encripted_text + "decripted"
	return encripted_text


def key_expansion(key, num_bytes= 16):

	#converting the key to ascii
	#key = [ord(x) for x in key]

	n = len(key)
	if n > num_bytes :
		print("The key is larger than the value allowed")
		exit(-1)
	keys = ''
	for i in range(n):
		keys = keys + str(key)

	rc = ['01', '02', '04', '08', '10', '20', '40', '80', '1B', '36', '6c', 'd8']
	rcon = [ x + '000000' for x in rc]
	word = []
	for i in range(4):
		word.append(format(key[4*i], 'x') + format(key[4*i + 1], 'x') +
					format(key[4*i + 2], 'x') + format(key[4*i + 3], 'x')
					)
	for i in range(4, 44):
		temp = word[i - 1]
		if (i % 4 == 0):
			temp = int(sub_word(rot_word(temp)),16) ^ int(rcon[int(i/4)], 16)
		else:
			temp = int(word[i - 1], 16)
		word.append(format((int(word[i-4],16) ^ temp), 'x'))
	return word

def rot_word(word):
    return word[2:] + word[:2]

def sub_word(word):
	l = []
	if(len(word) == 7):
		word = '0' + word
	for i in range(0,4):
		l.append(format(s_box[int((word)[i*2:i*2 + 1], 16) * 16 +  int((word)[i*2 + 1:i*2 + 2], 16) ], 'x'))
	return ''.join(l)

