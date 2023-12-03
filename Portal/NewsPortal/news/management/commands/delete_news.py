from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все новости из определенной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Категория новостей для удаления')

    def handle(self, *args, **options):
        category_name = options['category']
        try:
            category = Category.objects.get(name=category_name)
            confirmation = input(f"Вы уверены, что хотите удалить все новости из категории '{category_name}'? (y/n): ")
            if confirmation.lower() == 'y':
                Post.objects.filter(category=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Все новости из категории "{category_name}" успешно удалены.'))
            else:
                self.stdout.write(self.style.WARNING('Удаление новостей отменено.'))
        except Category.DoesNotExist:
            raise CommandError(f'Категория "{category_name}" не найдена.')