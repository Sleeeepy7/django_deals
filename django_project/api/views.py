from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Deal
import io
import datetime
from .utils import check_file_extension
from django.db.models import Sum, Count
from django.db import transaction

class DealUploadView(APIView):
    """Представление для загрузки файла
       и обработки его данных.
    """
    def post(self, request):
        """Обработка POST запроса для записи информации с файла(.csv) о клиентах в базу данных

        Args:
            request (POST): запрос

        Returns:
            status: str - OK/Error
            [ok]:
                - статус об успешной обработке файла
            
            [error]:
                Desc: str - описание ошибки на русском языке
        """
        try:
            file = request.FILES.get('file')
            if file is None:
                return Response({'status': 'Error', 'Desc': 'Вы не приложили файл'})
            is_csv = check_file_extension(file)
            if not bool(is_csv):
                return Response({'status': 'Error', 'Desc': 'Ошибка обработки. Принимаются только файлы с расширением .csv'})
            decoded_file = io.TextIOWrapper(file, encoding='utf-8')
            header = ['customer', 'item', 'total', 'quantity', 'date']
            # Ранее загруженные версии файла deals.csv не должны влиять на результат обработки новых.
            # эту строчку не особо понял, но допустим добавление строчки
            # Deal.objects.all().delete() решение
            deals_to_create = []
            for line in decoded_file:
                data = line.strip().split(',')
                if data == header:
                    continue
                customer, item, total, quantity, date = data
                deal = Deal(customer=customer, item=item, total=total, quantity=int(quantity), date=datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f'))
                deals_to_create.append(deal)

            with transaction.atomic():
                Deal.objects.bulk_create(deals_to_create, batch_size=500)
                print(Deal.objects.all().count())
            return Response({'status': 'OK'})
        except Exception as e:
            return Response({'status': 'Error', 'Desc': f'Неожиданная ошибка, описание: {e}'})
    

class TopCustomersView(APIView):
    """Представление для получения информации о топ 5 клиентах
       потративших наибольшую сумму за весь период.
    """
    def get(self, request):
        """Обработка GET запроса для получении информации о клиентах в соответствующем формате.

        Args:
            request (GET): запрос

        Returns:
            - Response: обработанные данные в формате:
                username: str
                spent_money: int
                gems: list
            - status: str - Error
                [error]:
                    Desc: str - описание ошибки на русском языке
        """
        try:
            customers = Deal.objects.values('customer').annotate(spent_money=Sum('total')).order_by('-spent_money')[:5]

            # список из 5 топ покупателлей
            top_customers = [customer['customer'] for customer in customers]

            # кверисет гемов в формате {'item': 'название', 'count': Кол-во(int)}
            gems = Deal.objects.values('item').filter(customer__in=top_customers).annotate(count=Count('customer')).filter(count__gte=2).order_by('-count')
            # список названий гемов в формате ['гем1', 'гем2'...]
            gem_names = [gem['item'] for gem in gems]

            response_data = []
            for customer in customers:
                response_data.append({
                    'username': customer['customer'],
                    'spent_money': customer['spent_money'],
                    'gems': gem_names
                })

            return Response({'response': response_data})
        except Exception as e:
            return Response({'status': 'Error', 'Desc': f'Неожиданная ошибка, описание: {e}'})