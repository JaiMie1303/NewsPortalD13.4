from datetime import datetime, timedelta
from django_apscheduler.models import DjangoJob
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events
from apscheduler.schedulers.blocking import BlockingScheduler
from news.models import Post
from django.core.mail import send_mail


def send_manager_notifications():
    current_time = datetime.now()
    next_monday = current_time + timedelta(days=(7 - current_time.weekday() + 1) % 7)
    next_monday = next_monday.replace(hour=8, minute=0, second=0, microsecond=0)
    start_date = next_monday - timedelta(weeks=1)
    end_date = next_monday - timedelta(days=1)
    posts = Post.objects.filter(date_published__range=[start_date, end_date], category__name='news')
    managers = ['evgeniyasmirnova89@gmail.com']
    for manager_email in managers:
        message = "Здравствуйте!\n\nНовости, опубликованные за прошедшую неделю:\n\n"
        for post in posts:
            message += f"Заголовок: {post.title}\n"
            message += f"Содержание: {post.content}\n\n"
        message += "С уважением, Ваша компания"
        send_mail("Новости за прошедшую неделю", message, "Teardrop1303@yandex.ru", [manager_email])

    print("Сообщения отправлены менеджерам")


def create_scheduler_job():
    scheduler = BlockingScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(send_manager_notifications, trigger="cron", day_of_week="mon", hour=8)

    register_events(scheduler)
    scheduler.start()

if __name__ == "__main__":
    create_scheduler_job()