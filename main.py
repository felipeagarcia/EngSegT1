import sys
import aes

if __name__ == '__main__':
	#if no argv is provided, exit the program
	if(len(sys.argv) == 1):
		print("No arguments provided")
		exit()
	mode = sys.argv[1]
	keyf_name = sys.argv[2]
	if(mode == 'C'): #encript mode
		if(len(sys.argv)  == 5):
			plain_text_file_name = sys.argv[3]
			encrpited_text_file_name = sys.argv[4]
			#reading key file
			with open(keyf_name, 'r') as key_file:
				key = key_file.read()
			#reading plain text file
			with open(plain_text_file_name, 'r') as plain_text_file:
				plain_text = plain_text_file.read()
			#oppening encripted text file and writing the
			#encripted text on it
			with open(encrpited_text_file_name, 'w') as encrpited_text_file:
				encripted_text = aes.encript(plain_text, key)
				encrpited_text_file.write(encripted_text)
			print(plain_text)
			print(encripted_text)

		else:
			print("please provide the correct number of arguments")
			exit()



	elif (mode == 'D'): #decript mode
		if(len(sys.argv)  == 5):
			plain_text_file_name = sys.argv[4]
			encrpited_text_file_name = sys.argv[3]
			with open(keyf_name, 'r') as key_file:
				key = key_file.read()
			with open(encrpited_text_file_name, 'r') as encrpited_text_file:
				encripted_text = encrpited_text_file.read()
			with open(plain_text_file_name, 'w') as plain_text_file:
				plain_text = aes.decript(encripted_text, key)
				plain_text_file.write(plain_text)
			print(encripted_text)
			print(plain_text)
		else:
			print("please provide the correct number of arguments")
			exit()

	elif (mode == 'K'): #key mode
		if(len(sys.argv)  == 4):
			keyf_name = sys.argv[2]
			with open(keyf_name, 'w') as key_file:
				key_file.write(sys.argv[3])
		else:
			print("please provide the correct number of arguments")
			exit()