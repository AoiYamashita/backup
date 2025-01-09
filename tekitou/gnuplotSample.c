#include <stdio.h>
#include <stdlib.h>
 
#define GNUPLOT "gnuplot -persist"
 
int main(void)
{
    FILE *gp;
    
    if ((gp = popen(GNUPLOT, "w")) == NULL) {
        fprintf(stderr, "Error: cannot open \"%s\".\n", GNUPLOT);
        exit(1);
    }
    
    fprintf(gp, "plot sin(x)");
    fprintf(gp, ",cos(x)\n");
    
    if (pclose(gp) == EOF) {
        fprintf(stderr, "Error: cannot close \"%s\".\n", GNUPLOT);
        exit(2);
    }
    
    return 0;
}