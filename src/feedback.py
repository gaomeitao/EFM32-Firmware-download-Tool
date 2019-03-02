#! /usr/bin/env python  
# -*- coding: UTF-8 -*-  
import smtplib  
from email.mime.text import MIMEText
from email.header import Header
class feedback:
    def __init__(self):
        self.mailto='major.gao@dewav.com'          #收件人(列表)
        self.mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址
        self.mail_user="pythontool"                           #用户名
        self.mail_pass="dewav1987"                             #密码
        self.mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com
    def send_mail(self,sub,content):
        me="<"+self.mail_user+"@"+self.mail_postfix+">"
        msg = MIMEText(content,'plain','utf-8')
        msg['Subject'] = Header(sub, 'utf-8').encode()
        msg['From'] = me
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)                            #连接服务器
            server.login(self.mail_user,self.mail_pass)               #登录操作
            server.sendmail(me,self.mailto, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False
    def feedback_mail(self,content):
        if self.send_mail("DownloadToolFeedBack",content):  #邮件主题和邮件内容
            #这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信
            print "done!"
            return True
        else:
            print "failed!"
            return False
