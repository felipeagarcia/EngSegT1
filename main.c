#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <errno.h>

char *stringToBinary(char *s)
{
  if (s == NULL) {
    // NULL might be 0 but you cannot be sure about it
    return NULL;
  }
  // get length of string without NUL
  size_t slen = strlen(s);

  // we cannot do that here, why?
  // if(slen == 0){ return s;}

  errno = 0;
  // allocate "slen" (number of characters in string without NUL)
  // times the number of bits in a "char" plus one byte for the NUL
  // at the end of the return value
  char *binary = malloc(slen * CHAR_BIT + 1);
  if(binary == NULL){
     fprintf(stderr,"malloc has failed in stringToBinary(%s): %s\n",s, strerror(errno));
     return NULL;
  }
  // finally we can put our shortcut from above here
  if (slen == 0) {
    *binary = '\0';
    return binary;
  }
  char *ptr;
  // keep an eye on the beginning
  char *start = binary;
  int i;

  // loop over the input-characters
  for (ptr = s; *ptr != '\0'; ptr++) {
    /* perform bitwise AND for every bit of the character */
    // loop over the input-character bits
    for (i = CHAR_BIT - 1; i >= 0; i--, binary++) {
      *binary = (*ptr & 1 << i) ? '1' : '0';
    }
  }
  // finalize return value
  *binary = '\0';
  // reset pointer to beginning
  binary = start;
  return binary;
}


int main(int argc, char *argv[]){
	char a[] = {"HelloWorld"};
	printf("%s\n", stringToBinary(a));
	printf("%s\n", argv[1]);
	printf("%s\n", argv[2]);
	if(argv == NULL)
		return 0;
	char *mode = argv[1];
	char *key_name = argv[2];

	if(strcmp(mode, "D") == 0){ // decript
		printf("Decript mode\n");
		FILE *keyf = fopen(key_name, "r");
		if (keyf == NULL){
			printf("Error while oppening file\n");
			return -1;
		}
		char key[8];
		fread(key, 8 * sizeof(char), 1, keyf);
		printf("my key is: %s\n", key);


	} else if(strcmp(mode, "C") == 0){ // encript
		printf("Encript mode\n");
		FILE *keyf = fopen(key_name, "r");
		if (keyf == NULL){
			printf("Error while oppening file\n");
			return -1;
		}
		char key[8];
		fread(key, 8 * sizeof(char), 1, keyf);
		printf("my key is: %s\n", key);


	} else if(strcmp(mode, "K") == 0){ // key mode
		printf("Key generate mode\n");
		FILE *keyf = fopen(key_name, "w");
		if (keyf == NULL){
			printf("Error while oppening file\n");
			return -1;
		}
		fwrite(argv[3] , 1 , sizeof(argv[3]) , keyf);


	}
	return EXIT_SUCCESS;
	
}