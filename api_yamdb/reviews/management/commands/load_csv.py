import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comments,
    Genre,
    Review,
    Title,
    TitleGenre,
)
from users.models import User

CSV_DIR = settings.DATA_TO_LOAD_DIR


class Command(BaseCommand):
    help = 'Наполнение отдельных таблиц базы данными'

    def add_arguments(self, parser):
        parser.add_argument('csv_files', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        csv_files = kwargs['csv_files']
        equals = {
            'category.csv': Category,
            'comments.csv': Comments,
            'genre_title.csv': TitleGenre,
            'genre.csv': Genre,
            'review.csv': Review,
            'titles.csv': Title,
            'users.csv': User
        }
        for file_name in csv_files:
            csv_file_path = os.path.join(CSV_DIR, file_name)
            if file_name in equals:
                model = equals[file_name]
                try:
                    with open(csv_file_path, mode='r') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            model.objects.create(**row)
                    print(f'Данные для модели {model} загружены.')
                except Exception as e:
                    print(f'Ошибка загрузки данных в модель {model}: {e}')
            else:
                print(f'Не найдена модель для данных {file_name}')
