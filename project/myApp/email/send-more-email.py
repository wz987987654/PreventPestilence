from email.header import Header #处理邮件主题
from email.mime.text import MIMEText # 处理邮件内容
from email.utils import parseaddr, formataddr #用于构造特定格式的收发邮件地址
import smtplib #用于发送邮件
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
from_addr = '18360939363@163.com'
password = '211416038A'
to_addrs = ['1290278122@qq.com','1287572725@qq.com','1185675202@qq.com','18360939363@163.com']#这里存放批量的邮件地址，或者我们也可以从本地存放邮件地址的文件中读取
smtp_server = 'smtp.163.com'
msg = MIMEText('请注意，今日预警指数为C级。', 'plain','utf-8')
msg['From'] = _format_addr('发送<%s>'%from_addr)
msg['Subject'] = Header('这是邮件主题：疾病预警系统通知','utf-8').encode()
server = smtplib.SMTP(smtp_server,25)
server.login(from_addr, password)
for to_addr in to_addrs:
  msg['To'] = _format_addr('接收<%s>'%to_addr)
  try:
      server.sendmail(from_addr, to_addr, msg.as_string())
  except:
       print('发送失败，再次尝试')
       server.sendmail(from_addr, to_addr, msg.as_string())
  print('发送邮件到'+to_addr)
server.quit()