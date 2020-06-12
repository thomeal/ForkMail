import imaplib
import smtplib
from email import parser, message
from email.header import Header, decode_header
from email.mime.text import MIMEText


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


class Email:
    def __init__(self, smtp_host, smtp_port, imap_host, imap_port, address, key):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.imap_host = imap_host
        self.imap_port = imap_port
        self.address = address
        self.key = key

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

    # 此函数通过使用imaplib实现接收邮件
    def recv_email_by_imap4(self):
        # 要进行邮件接收的邮箱。改成自己的邮箱
        email_address = self.address
        # 要进行邮件接收的邮箱的密码。改成自己的邮箱的密码
        email_password = self.key
        # 邮箱对应的imap服务器，也可以直接是IP地址
        # 改成自己邮箱的imap服务器；qq邮箱不需要修改此值
        imap_server_host = self.imap_host
        # 邮箱对应的pop服务器的监听端口。改成自己邮箱的pop服务器的端口；qq邮箱不需要修改此值
        imap_server_port = self.imap_port

        try:
            # 连接imap服务器。如果没有使用SSL，将IMAP4_SSL()改成IMAP4()即可其他都不需要做改动
            email_server = imaplib.IMAP4_SSL(host=imap_server_host, port=imap_server_port)
        except Exception:
            raise Exception('服务器失去连接')
        try:
            # 验证邮箱及密码是否正确
            email_server.login(email_address, email_password)
        except Exception:
            raise Exception('邮箱地址或密钥错误')

        # 邮箱中其收到的邮件的数量
        email_server.select()
        email_count = len(email_server.search(None, 'ALL')[1][0].split())
        # 通过fetch(index)读取第index封邮件的内容；这里读取最后一封，也即最新收到的那一封邮件
        typ, byte_content = email_server.fetch(f'{email_count}'.encode(), '(RFC822)')
        # 将邮件内存由byte转成str

        email_content = byte_content[0][1].decode()

        # 关闭select
        email_server.close()
        # 关闭连接
        email_server.logout()


if __name__ == "__main__":
    # 实例化
    email_client = Email('smtp.qq.com', 465, 'imap.qq.com', 993, '1134372723@qq.com', 'odtgbaxmzscqjffe')
    # 调用通过smtp发送邮件的发送函数
    # email_client.send_email_by_smtp('180300507@stu.hit.edu.cn', 'SMTP测试', 'HelloSMTP')
    # 调用通过imap4接收邮件的接收函数
    email_client.recv_email_by_imap4()

    exit(0)
