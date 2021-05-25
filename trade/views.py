from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages

from .models import *
from .forms import SearchForm


def get_id(request):
    # функция-контроллер для поиска уникальных id производителя товаров по id контракта и заявки
    try:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                contract_id = form.cleaned_data['contract_id']
                if contract_id > 0:
                    request_id = CreditRequests.objects.filter(contract=contract_id)
                    products = request_id[0].req.all()        # используем related_name (req) для обратной связи
                    prod_id = []
                    for item_products in products:
                        prod_id.append(item_products.manufacturer.pk)
                    unique_manufacturer_id = set(prod_id)
                    messages.success(request, 'Успешно!')
                    return render(request, 'trade/search.html', {'credit_request': request_id[0],
                                                                 'products': list(products),
                                                                 'unique_manufacturer_id': unique_manufacturer_id
                                                                 })
                else:
                    messages.error(request, 'Ошибка валидации!')
                    return redirect('home')
            else:
                messages.error(request, 'Ошибка валидации!')
                return redirect('home')
        else:
            return redirect('home')
    except IndexError:
        print('Invalid index')
        return redirect('home')


class HomeContract(ListView):
    """
       Контроллер для отображения контрактов на главной
       странице сайта
    """
    model = Contract
    template_name = 'trade/contract.html'
    context_object_name = 'contract'

    def get_queryset(self):
        return Contract.objects.all()
