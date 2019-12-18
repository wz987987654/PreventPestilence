import smtplib
from email.mime.text import MIMEText   # 导入模块

class SendEmail:

    def send_emil(self, username, passwd, recv, title, content, mail_host='smtp.163.com', port=25):
        msg = MIMEText(content)      #邮件内容
        msg['Subject'] = title
        msg['From'] = username
        msg['To'] = recv
        smtp = smtplib.SMTP(mail_host, port=port)   # 定义邮箱服务类型
        smtp.login(username, passwd)      # 登录邮箱
        smtp.sendmail(username, recv, msg.as_string())   #发送邮件
        smtp.quit()
        print('email 发送成功.')

if __name__ == '__main__':
    email_user = '18360939363@163.com'  # 发送者账号
    email_pwd = '211416038A'  # 发送者密码,授权码
    maillist = '1290278122@qq.com'   # 接收者邮箱
    title = '测试邮件标题'
    content = '这里是邮件内容'
    SendEmail().send_emil(email_user, email_pwd, maillist, title, content)