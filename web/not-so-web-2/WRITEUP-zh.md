# Writeup - not-so-web-2

## Unintended Solution

正如挑战1中所讨论的，本次挑战中的cookie验证部分应该是健壮且安全的。然而，我刚刚犯了一个非常愚蠢的错误，让这个 cookie 设计变成了一个笑话。

> writeup 评价: 乐子检验

```py
    try:
        PKCS1_v1_5.new(public_key).verify(msg_hash, sig)
        valid = True
        # valid = PKCS1_v1_5.new(public_key).verify(msg_hash, sig)
    except (ValueError, TypeError):
        valid = False
```

也就是说，一旦你的签名没有引发任何异常，你就会得到“valid = True”。F**k，我在用人工智能帮忙编写加密代码的时候应该更小心点儿T.T

> 有趣的是，如果不仔细审核代码，可能会错过这个明显的错误，而且就比赛过程中的私聊，很多人是直接随便试出来的。

以管理员身份登录后，SSTI 部分与上一题略有不同，要绕过一些简单的检查。

```py
    if payload:
        for char in payload:
            if char in "'_#&;":
                abort(403)
                return
```

网上稍微搜一搜 SSTI 绕过或者用轮子 [fenjing](https://github.com/Marven11/Fenjing/tree/main) 就可以轻松搞定

## Intended Solution

假设 Cookie 设计正确，选手在审核完代码时应该会感到疑惑（咳咳，应该），洞在哪

其实题目也并不生硬，是有提示的，答案是与 HTTPS 有关（应该思考，为什么第一个题使用 HTTP，而这个题使用 HTTPS？）。

例如，使用 HTTP 访问网站将获得如下结果：

![https](./https-http.png)

Duang，看到 nginx/1.11.13, 超级无敌过气版本

那么你可能已经知道这里出了什么问题，漏洞存在于 nginx 中，而不是 web 应用程序本身。老版本 + nginx，应当直接想到：[heartbleeding CVE-2014-0160](https://www.heartbleed.com/)。

然后呢，使用类似[vulhub](https://github.com/vulhub/vulhub/tree/master/openssl/CVE-2014-0160)的 PoC，可以利用越界堆读取漏洞泄露服务器数据。预期解答是利用此漏洞泄露真正的管理员密码实现登陆打 SSTI