from celery import Celery
from django.core.mail import send_mail
from celery import shared_task

app = Celery('your_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def send_manager_notifications():
    recipients = ['evgeniyasmirnova89@gmail.com']
    subject = 'Новости за прошедшую неделю'
    message = 'Здравствуйте!\n\nВаши новости за прошедшую неделю: ...'
    sender = 'Teardrop1303@yandex.ru'
    send_mail(subject, message, sender, recipients)


@shared_task
def send_notification_to_managers(post_title):
    manager_emails = ['evgeniyasmirnova89@gmail.com']
    subject = f"Уведомление о новой новости: {post_title}"
    message = "Появилась новая новость на новостном портале. Пожалуйста, проверьте."
    from_email = "Teardrop1303@yandex.ru"
    recipient_list = manager_emails
    send_mail(subject, message, from_email, recipient_list)