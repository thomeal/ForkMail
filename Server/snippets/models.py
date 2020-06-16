from django.db import models


class User(models.Model):
    mobile = models.CharField('mobile', primary_key=True, max_length=15)
    nickname = models.CharField('nickname', max_length=20, default=mobile)
    password = models.CharField('password', null=False, max_length=20)

    class Meta:
        db_table = 'user'


class Email(models.Model):
    email = models.CharField('email', primary_key=True, max_length=40)
    key = models.CharField('key', null=False, max_length=100)
    user = models.ForeignKey(User, to_field='mobile', on_delete=models.CASCADE)
    smtp_host = models.CharField('smtp_host', null=False, max_length=50)
    smtp_port = models.CharField('smtp_port', null=False, max_length=50)
    imap_host = models.CharField('imap_host', null=False, max_length=50)
    imap_port = models.CharField('imap_port', null=False, max_length=50)

    class Meta:
        db_table = 'email'
        unique_together = ('user', 'email')
