import imaplib
import smtplib
import ssl
from email.header import Header, decode_header
from email.mime.text import MIMEText
from email.parser import Parser
from email.utils import parseaddr

from imbox import Imbox


class MailAccount:
    def __init__(self, account):
        self.smtp_host = account.smtp_host
        self.smtp_port = account.smtp_port
        self.imap_host = account.imap_host
        self.imap_port = account.imap_port
        self.address = account.email
        self.key = account.key

    # 此函数通过使用smtplib实现发送邮件
    def send_email_by_smtp(self, to, subject, context):
        # 用于发送邮件的邮箱。修改成自己的邮箱
        sender_email_address = self.address
        # 用于发送邮件的邮箱的密码。修改成自己的邮箱的密码
        sender_email_password = self.key
        # 用于发送邮件的邮箱的smtp服务器，也可以直接是IP地址
        # 修改成自己邮箱的sntp服务器地址；qq邮箱不需要修改此值
        smtp_server_host = self.smtp_host
        # 修改成自己邮箱的sntp服务器监听的端口；qq邮箱不需要修改此值
        smtp_server_port = self.smtp_port
        # 要发往的邮箱
        receiver_email = to
        # 要发送的邮件主题
        message_subject = subject
        # 要发送的邮件内容
        message_context = context

        # 邮件对象，用于构建邮件
        # 如果要发送html，请将plain改为html
        message = MIMEText(message_context, 'plain', 'utf-8')
        # 设置发件人（声称的）
        message["From"] = "%s" % Header(sender_email_address, "utf-8")
        # 设置收件人（声称的）
        message["To"] = "%s" % Header(receiver_email, "utf-8")
        # 设置邮件主题
        message["Subject"] = Header(message_subject, "utf-8")

        # 连接smtp服务器。如果没有使用SSL，将SMTP_SSL()改成SMTP()即可其他都不需要做改动
        email_client = smtplib.SMTP_SSL(smtp_server_host, smtp_server_port)
        try:
            # 验证邮箱及密码是否正确
            email_client.login(sender_email_address, sender_email_password)
        except Exception:
            raise Exception('邮箱地址或密钥错误')
        else:
            # 发送邮件
            email_client.sendmail(sender_email_address, receiver_email, message.as_string())
        finally:
            # 关闭连接
            email_client.close()

    def getAllMails(self):
        imbox = Imbox(hostname=self.imap_host,
                   username=self.address,
                   password=self.key,
                   ssl=False,
                   ssl_context=ssl.create_default_context(),
                   starttls=False)
        return imbox.messages()
