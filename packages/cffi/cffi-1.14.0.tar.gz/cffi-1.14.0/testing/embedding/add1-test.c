#include <stdio.h>

#ifdef _MSC_VER
#include <windows.h>
#endif

extern int add1(int, int);


int main(void)
{
    int x, y;
    x = add1(40, 2);
    y = add1(100, -5);
    printf("got: %d %d\n", x, y);
#ifdef _MSC_VER
    if (x == 0 && y == 0)
        Sleep(2000);
#endif
    return 0;
}
