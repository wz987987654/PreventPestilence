import smtplib #登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText #负责构建邮件格式

subject = "学习邮件"
content = "孩子不学习，多半是欠的，抄五遍就好了"
sender = "18360939363@163.com"
password = "211416038A" #授权码
recver = "2910424339@qq.com,1287572725@qq.com,1185675202@qq.com,2529614014@qq.com,"



message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
smtp.close()
