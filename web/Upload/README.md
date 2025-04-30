## upload

先随便登录一个用户，随便上传一个文件后被重定向到`/upload?file_path=xxxxx` ，测试发现任意文件读取，读 `/proc/self/cmdline` 定位文件路径 `/app/app.py` ，进而获取源代码。看到 `admin` 用户存在命令注入漏洞，那么就是试图以 `admin` 登录进而 `rce` ，最后用普通用户读取命令输出即可。

以 `admin` 登录有两种思路：

1.  注意到 `secretkey` 是从环境变量中读取，所以可以读 `/proc/self/environ` 进而伪造 `session`
2.  `admin` 密码的哈希其实是可以查出来的，密码为 `backdoor`

Firstly, login as a certain user, upload a file and then be redirected to  `/upload?file_path=xxxxx`. Upon testing, you notice that arbitrary file reading is possible. By reading `/proc/self/cmdline`, you can locate the file path `/app/app.py`. From there, you can retrieve the source code. You notice that there is a command injection vulnerability for the `admin` user, so you try to log in as `admin` to gain `rce`. Finally, you can read the command output as a normal user.

There are two approaches to log in as `admin`:

1.  Notice that the `secretkey` is read from the environment variable, so you can read `/proc/self/environ` to forge a `session`
2.  The hash of the `admin` password can be found, and the password is `backdoor`