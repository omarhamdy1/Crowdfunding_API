import json
from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Collect, Payment


MOCK_DATA = './mock_data.json'


class Command(BaseCommand):
    help = f'Загружает моковые данные из {MOCK_DATA}'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаем загрузку моковых данных...')

        try:
            with open(MOCK_DATA, 'r') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл {MOCK_DATA} не найден.')
            )
            return
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('Ошибка при декодировании JSON.')
            )
            return

        users = []
        for data in json_data:
            user_data = data['user']
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={'email': user_data['email']}
            )
            users.append(user)

        collects_to_create = []
        payments_to_create = []

        for i, data in enumerate(json_data):
            user = users[i]
            for collect_data in data['collects']:
                collect = Collect(
                    author=user,
                    title=collect_data['title'],
                    occasion=collect_data['occasion'],
                    description=collect_data['description'],
                    target_amount=collect_data['target_amount'],
                    collected_amount=collect_data['collected_amount'],
                    donors_count=collect_data['donors_count'],
                    cover_image=collect_data['cover_image'],
                    end_date=datetime.fromisoformat(collect_data['end_date'])
                )
                collects_to_create.append(collect)

                for payment_data in collect_data['payments']:
                    payment = Payment(
                        collect=collect,
                        user=user,
                        amount=payment_data['amount'],
                        created_at=datetime.fromisoformat(
                            payment_data['created_at']
                        )
                    )
                    payments_to_create.append(payment)

        Collect.objects.bulk_create(collects_to_create)
        self.stdout.write(f'Создано {len(collects_to_create)} сборов.')

        Payment.objects.bulk_create(payments_to_create)
        self.stdout.write(f'Создано {len(payments_to_create)} платежей.')

        self.stdout.write('Моковые данные успешно загружены!')
