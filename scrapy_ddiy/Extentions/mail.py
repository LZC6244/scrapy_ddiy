# -*- coding: utf-8 -*-

import base64
import logging
import smtplib
from os import path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def is_contain_chinese(string):
    # 判断字符串是否含有中文
    for s in string:
        if '\u4e00' <= s <= '\u9fa5':
            return True
    return False


class EmailSender(object):

    def __init__(self, email_host='smtphz.qiye.163.com', email_port=465, email_pass=''):
        self.msg = MIMEMultipart()
        self.init_flag = False
        self.logger = logging.getLogger(__name__)
        self.email_host = email_host
        self.email_port = email_port
        if email_pass:
            self.email_pass = email_pass
        else:
            # 设置一个初始值，避免每次都输入授权码
            self.email_pass = 'xxxxxxxxxxx'
            # self.logger.error('Please Enter The  Password!')

    def init(self, from_addr, to_addrs, subject):
        """
        :param from_addr: 发件人
        :param to_addrs: 收件人
        :param subject: 邮件标题
        :return:
        """
        to_addrs_s = ''
        if not isinstance(to_addrs, str):
            for i in list(to_addrs):
                to_addrs_s += i + ','
            to_addrs_s = to_addrs_s.strip(',')
        else:
            to_addrs_s = to_addrs

        self.msg['From'] = from_addr
        self.msg['To'] = to_addrs_s
        self.msg['Subject'] = subject
        self.init_flag = True

    def attach_text(self, text=''):
        # 添加邮件正文 （ 纯文本 ）
        msg_text = MIMEText(text, 'plain', 'utf8')
        self.msg.attach(msg_text)

    def attach_html(self, text=''):
        # 添加邮件正文 （ html ）
        # html 格式不固定，故请将 html 源码全部输入
        # 此处不通过 MIMEImage 定义图片ID，在 HTML 文本中引用 （ ... ）
        msg_text = MIMEText(text, 'html', 'utf8')
        self.msg.attach(msg_text)

    def attach_file(self, file=''):
        # 添加邮件附件
        if not path.exists(file):
            raise ValueError(f'Path {file} not exists.')
        with open(file, 'rb') as f:
            # 不使用这种，没有文件关闭操作
            # att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att = MIMEText(f.read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            # 获取文件名
            filename = path.split(file)[1]
            # 判断文件名是否含有中文
            if is_contain_chinese(filename):
                # 处理中文文件名 （ add_header 的第三种写法 ）
                att.add_header("Content-Disposition", "attachment", filename=("gbk", "", filename))
            else:
                # 文件名不含中文 （ add_header 的第一种写法 ）
                att.add_header('content-disposition', 'attachment', filename=filename)
                # 或者可以这样写
                # att['Content-Disposition'] = 'attachment;filename="%s"' % filename
            self.msg.attach(att)

    @staticmethod
    def html_img(file):
        # 将图片转换成 base64 编码
        # 然后根据 html 语法填写成 html 语句
        with open(file, 'rb') as f:
            # base64编码后的字符串
            s_b64 = base64.b64encode(f.read())
            s_b64 = str(s_b64, encoding='utf-8')
            # 图片文件的后缀
            f_suffix = file.split('.')[-1]
            img = '<img src="data:image/%s;base64,%s"/>' % (f_suffix, s_b64)
            return img

    def send(self):
        if not self.init_flag:
            raise AttributeError('[ init ] must be called before the send method.')
        from_addr = self.msg['From']
        to_addrs = self.msg['To']
        try:
            # 在创建客户端对象的同时，使用SSL加密连接到邮箱服务器
            client = smtplib.SMTP_SSL(host=self.email_host, port=self.email_port)
            login_result = client.login(from_addr, self.email_pass)
            if login_result and login_result[0] == 235:
                self.logger.info('[ EmailSender ] Login successful.')
                # print(login_result)
                client.sendmail(from_addr, to_addrs, self.msg.as_string())
                self.logger.info('[ EmailSender ] Email sent successfully.')
                client.close()
            else:
                self.logger.info('[ EmailSender ] Login failed: ', login_result[0], login_result[1])
        except Exception as e:
            self.logger.error('[ EmailSender ] Connection to mail server error: %s.' % e)


if __name__ == '__main__':
    email = EmailSender(email_host='smtp.qq.com', email_pass='xxx')
    content = '这是lzc发送过来的邮件。请注意查收！'
    email.init(from_addr='xxx@qq.com', to_addrs=['xxx@qq.com'], subject='测-试')
    email.attach_text(text=content)
    email.attach_file(r'C:\xxx\xx.jpg')
    email.attach_file(r'C:\xxx\xx.txt')
    email.send()
