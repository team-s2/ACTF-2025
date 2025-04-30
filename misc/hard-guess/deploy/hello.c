#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

int main(){
    setuid(0);
    setgid(0);
    char choice = 'n';
    printf("Are you Tomoya?\ny/n:\n> ");
    scanf("%c", &choice);

    if (getenv("LD_PRELOAD"))
        unsetenv("LD_PRELOAD");
    if (getenv("LD_LIBRARY_PATH"))
        unsetenv("LD_LIBRARY_PATH");
    if (getenv("LD_AUDIT"))
        unsetenv("LD_AUDIT");
    if (getenv("LD_DEBUG"))
        unsetenv("LD_DEBUG");
    if (getenv("LIBRARY_PATH"))
        unsetenv("LIBRARY_PATH");

    setenv("PATH", "/bin", 1);

    if (choice == 'y')
        system("echo 'Hello!'");
    else if (choice == 'n')
        system("bash -c \"echo 'Who are you?'\"");
    else
        printf("emm? ...");
    return 0;
}