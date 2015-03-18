#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char **argv){
  FILE *fp;
  unsigned long int lo;
  unsigned short int sh;
  unsigned char ch;

  if(argc!=2){
    printf("Use: %s <file>\n",argv[0]);
    exit(1);
  }

  fp=fopen(argv[1],"rb");
  if(fp==NULL)exit(1);
  
  fread(&lo,sizeof(unsigned long int),1,fp);
  printf("%ld\n",lo);

  for(;;){
    fread(&lo,sizeof(unsigned long int),1,fp);
    fread(&sh,sizeof(unsigned short int),1,fp);
    fread(&ch,sizeof(unsigned char),1,fp);
    if(feof(fp))break;
    printf("%-9ld %-4d %-2d\n",lo,sh,ch);
  }

  fclose(fp);
}