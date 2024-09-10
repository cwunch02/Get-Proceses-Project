#include "types.h"
#include "user.h"

int main(void) {
  int num_procs = getprocs();
  printf(1, "Number of processes: %d\n", num_procs);
  exit();
}
