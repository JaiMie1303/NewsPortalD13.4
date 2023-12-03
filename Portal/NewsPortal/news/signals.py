from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Post, Subscription


@receiver(post_save, sender=Post)
def send_news_notification(sender, instance, created, **kwargs):
    if created:
        subscribers = Subscription.objects.filter(category=instance.category)
        for subscriber in subscribers:
            user = subscriber.user
            subject = 'Новая новость'
            message = f'Появилась свежая новость в категории {instance.category}: {instance.title}'
            send_mail(subject, message, 'Teardrop1303@yandex.ru', [user.email])