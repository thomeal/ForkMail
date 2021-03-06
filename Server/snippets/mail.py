import smtplib
import ssl
from email.header import Header
from email.mime.text import MIMEText

from imbox import Imbox


class MailAccount:
    def __init__(self, account):
        self.address = account.email
        self.key = account.key
        self.smtpHost = account.smtp_host
        self.imapHost = account.imap_host

    def send_email_by_smtp(self, to, subject, context):
        sender_email_address = self.address
        sender_email_password = self.key
        smtp_server_host = self.smtpHost
        smtp_server_port = 25
        receiver_email = to
        message_subject = subject
        message_context = context
        message = MIMEText(message_context, 'plain', 'utf-8')
        message["From"] = "%s" % Header(sender_email_address, "utf-8")
        message["To"] = "%s" % Header(receiver_email, "utf-8")
        message["Subject"] = "%s" % Header(message_subject, "utf-8")

        email_client = smtplib.SMTP(smtp_server_host, smtp_server_port)
        try:
            email_client.login(sender_email_address, sender_email_password)
        except Exception:
            raise Exception('邮箱地址或密钥错误')
        else:
            email_client.sendmail(sender_email_address, receiver_email, message.as_string())
        finally:
            email_client.close()

    def getAllMails(self):
        imbox = Imbox(hostname=self.imapHost,
                      username=self.address,
                      password=self.key,
                      ssl=False,
                      ssl_context=ssl.create_default_context(),
                      starttls=False)
        return imbox.messages()

    def deleteMail(self,id):
        imbox = Imbox(hostname=self.imapHost,
                      username=self.address,
                      password=self.key,
                      ssl=False,
                      ssl_context=ssl.create_default_context(),
                      starttls=False)
        return imbox.delete(id)
