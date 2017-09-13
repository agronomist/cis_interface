
#include "PsiInterface.hpp"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>


int main(int argc, char *argv[]) {

  int iterations = atoi(argv[1]);
  printf("Hello from C++ rpcFibCliPar: iterations = %d\n", iterations);
  
  // Create RPC connection with server
  PsiRpcClient rpc("cli_par_fib", "%d", "%d %d");
  
  // Send all of the requests to the server
  int ret;
  for (int i = 1; i <= iterations; i++) {
    printf("rpcFibCliPar(CPP): fib(->%-2d) ::: \n", i);
    ret = rpc.send(1, i);
    if (ret != 0) {
      printf("rpcFibCliPar(CPP): SEND FAILED\n");
      exit(-1);
    }
  }

  // Receive responses for all requests that were sent
  int fib = -1;
  int fibNo = -1;
  for (int i = 1; i <= iterations; i++) {
    ret = rpc.recv(2, &fibNo, &fib);
    if (ret < 0) {
      printf("rpcFibCliPar(CPP): RECV FAILED\n");
      exit(-1);
    }
    printf("rpcFibCliPar(CPP):  fib(%2d<-) = %-2d<-\n", fibNo, fib);
  }

  printf("Goodbye from C++ rpcFibCliPar\n");
  exit(0);
    
}

