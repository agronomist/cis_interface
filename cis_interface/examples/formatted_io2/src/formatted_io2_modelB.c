#include <stdio.h>
// Include methods for input/output channels
#include "PsiInterface.h"

#define MYBUFSIZ 1000

int main(int argc, char *argv[]) {
  // Initialize input/output channels
  psiAsciiTableInput_t in_channel = psiAsciiTableInput("inputB", 0, 1);
  psiAsciiTableOutput_t out_channel = psiAsciiTableOutput("outputB", "%6s\t%d\t%f\n", 0, 1);

  // Declare resulting variables and create buffer for received message
  int flag = 1;
  char name[MYBUFSIZ];
  int count = 0;
  double size = 0.0;

  // Loop until there is no longer input or the queues are closed
  while (flag >= 0) {
  
    // Receive input from input channel
    // If there is an error, the flag will be negative
    // Otherwise, it is the size of the received message
    flag = psiRecv(in_channel, &name, &count, &size);
    if (flag < 0) {
      printf("Model B: No more input.\n");
      break;
    }

    // Print received message
    printf("Model B: %s, %d, %f\n", name, count, size);

    // Send output to output channel
    // If there is an error, the flag will be negative
    flag = psiSend(out_channel, name, count, size);
    if (flag < 0) {
      printf("Model B: Error sending output.\n");
      break;
    }

  }
  
  return 0;
}
