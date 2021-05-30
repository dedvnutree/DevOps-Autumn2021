from django.db import models
import datetime
from datetime import date
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
from shop.settings import EMAIL_HOST_USER


class MailRecipient(models.Model):
    mail_address = models.CharField(max_length=40)
    send_on = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=1))

    def __str__(self):
        return self.mail_address

    @classmethod
    def add_as_recipient(self, mail):
        if not MailRecipient.objects.filter(mail_address=mail):
            MailRecipient.objects.create(mail_address=mail)

    @classmethod
    def remove_as_recipient(self, mail):
        MailRecipient.objects.filter(mail_address=mail).delete()

    def send_scheduled_mail(self):
        subject = "Напоминание от ИкеяДляБедных"
        message = "Кажется вы забыли кое-что в корзине на нашем сайте. Ссылка: http://127.0.0.1:8000/catalog/basket"
        # recipient_list = list(self.recipients_list.values_list('mail_address', flat=True))
        mail = EmailMessage(
            subject=subject,
            body=message,
            from_email=EMAIL_HOST_USER,
            to=(self.mail_address,),
        )
        mail.content_subtype = 'html'
        mail.send()
        self.send_on = self.send_on + datetime.timedelta(days=7)
        self.save()


class DelayedMail(models.Model):
    # recipients_list = models.ManyToManyField(MailRecipient, related_name='mail_list')

    def __str__(self):
        return "DelayedMail model"

    @classmethod
    def get_today_mail(cls):
        today = date.today()
        return MailRecipient.objects.filter(send_on__year=today.year, send_on__month=today.month, send_on__day=today.day)
        # return cls.objects.filter(send_on__year=today.year, send_on__month=today.month, send_on__day=today.day)


