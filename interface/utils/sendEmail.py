# -*- coding:UTF-8 -*-
# 发送html内容的邮件
import smtplib, time, os
from email.mime.text import MIMEText
from email.header import Header


class SendEmail():
     def __init__(self,receiver,subject):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.receiver = receiver
        self.subject = subject+'自动化测试结果_'+t

     def sendemail(self,mail_body,subtype):
         # 发送邮箱服务器
         smtpserver = 'mail.cias.cn'
         # 发送邮箱用户/密码
         username = 'autotest@cias.cn'
         password = 'AT_123456'
        # 发送邮箱
         sender = 'autotest@cias.cn'


         # 组装邮件内容和标题，中文需参数‘utf-8’，单字节字符不需要
         msg = MIMEText(mail_body, _subtype=subtype, _charset='utf-8')
         msg['Subject'] = Header(self.subject, 'utf-8')
         msg['From'] = sender
         msg['To'] = ",".join(self.receiver)
         # 登录并发送邮件
         smtp = smtplib.SMTP(smtpserver,port=587,timeout=15)
         try:
             
         # smtp.set_debuglevel(1)
             smtp.connect(smtpserver,587)
             smtp.starttls()
             smtp.login(username, password)
             smtp.sendmail(sender, self.receiver, msg.as_string())
         except:
            print("邮件发送失败！")
         else:
            print("邮件发送成功！")
         finally:
             smtp.quit()


# def send_mail_html(file):
#     '''发送html内容邮件'''
#     # 发送邮箱
#     sender = 'zhangkai@192.168.20.190'
#     # 接收邮箱
#     receiver = 'gongxingrui@192.168.20.190'
#     # 发送邮件主题
#     t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     subject = '自动化测试结果_' + t
#     # 发送邮箱服务器
#     smtpserver = '192.168.20.190'
#     # 发送邮箱用户/密码
#     username = 'zhangkai'
#     password = '123456'
#
#     # 读取html文件内容
#     f = open(file, 'rb')
#     mail_body = f.read()
#     f.close()
#
#     # 组装邮件内容和标题，中文需参数‘utf-8’，单字节字符不需要
#     msg = MIMEText(mail_body, _subtype='html', _charset='utf-8')
#     msg['Subject'] = Header(subject, 'utf-8')
#     msg['From'] = sender
#     msg['To'] = receiver
#     # 登录并发送邮件
#     try:
#         smtp = smtplib.SMTP()
#         smtp.connect(smtpserver)
#         smtp.login(username, password)
#         smtp.sendmail(sender, receiver, msg.as_string())
#     except:
#         print("邮件发送失败！")
#     else:
#         print("邮件发送成功！")
#     finally:
#         smtp.quit()
#
#

if __name__ == "__main__":

    receivers = ['subing@cias.cn','subing@cias.cn']
    html = """
    <html>  
      <head></head>  
      <body>  
        <p>你好！<br>  
           本次自动化执行测试结果为：<br>  
           查看详细内容请 <a href="http://www.baidu.com">点击</a><br> 
        </p> 
      </body>  
    </html>  
    """
    # f.close()
    email = SendEmail(receivers, '共享查勘')
    email.sendemail(html, 'html')