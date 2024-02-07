#include <stdio.h>
#include <string.h>

int sleep(int t)
{
    printf("%d\n", t);

    // ref
    // LD_PRELOAD: https://www.cnblogs.com/net66/p/5609026.html
    // read file: https://stackoverflow.com/questions/3463426/in-c-how-should-i-read-a-text-file-and-print-all-strings

    int c;

    FILE *f;
    f = fopen("flag.txt", "r");

    if (f)
    {
        while ((c = getc(f)) != EOF)
        {
            putchar(c);
        }

        fclose(f);
    }

    return 0;
}
