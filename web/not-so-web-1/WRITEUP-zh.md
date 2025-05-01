# Writeup - not-so-web-1

考察 cookie 伪造，IV 可控，通过 CBC 异或翻转将用户名改成 admin 即可登陆

https://cryptohack.org/courses/symmetric/flipping_cookie

SSTI 部分就是一个直接的，网上搜到的 payload 基本都可以用

> 值得一提的是测试的时候会发现 eval 还有一些没被过滤的关键字似乎是被拦了，猜测是赛方服务器防火墙的骚操作。

这个题的设置难度基本是有手就会，核心目的是给第二道放个烟雾弹来着。