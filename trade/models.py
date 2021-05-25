from django.db import models
from django.utils.translation import gettext_lazy as _


class Manufacturer(models.Model):
    """
    Класс модели производителей товаров.
    """
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("manufacturer")
        verbose_name_plural = _("manufacturers")
        ordering = ['pk']

    def __str__(self):
        """
        Возвращает строковое представление.
        :return: если у производителя есть страна то
        вернуть строку вида f'{self.pk} | {self.name} | {self.country}'
        в противном случае вернуть только f'{self.pk} | {self.name}'
        """
        return f'{self.pk} | {self.name} | {self.country}' if self.country else f'{self.pk} | {self.name}'

    @classmethod
    def get_default_pk(cls):
        # метод создает раздел для товаров у которых производитель не известен
        obj, created = cls.objects.get_or_create(name="No manufacturer")   # создать если нет раздела
        return obj.pk


class Product(models.Model):
    """
    Класс модели товаров.
    """
    name = models.CharField(max_length=255)         # наименование продукта
    description = models.TextField()
    manufacturer = models.ForeignKey(               # связь многие к одному
        Manufacturer,                               # ссылка на производителя
        on_delete=models.SET_DEFAULT,               # при удалении подставляется значение по умолчанию
        default=Manufacturer.get_default_pk         # значение по умолчанию
    )
    cred_req = models.ForeignKey('CreditRequests',                # ссылка на заявку
                                 on_delete=models.SET_DEFAULT,
                                 default=None,
                                 blank=True,
                                 related_name='req'               # имя для обратной связи
                                 )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ['name']                     # сортировка продуктов по имени

    def __str__(self):
        """
        :return:
        Вернет строку вида Наименование продукта.
        """
        return f'{self.name}'


class CreditRequests(models.Model):
    """
    Класс кредитной заявки на товар(ы).
    """
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("credit request")
        verbose_name_plural = _("credit requests")
        ordering = ['pk']

    def __str__(self):
        """
        :return:
        Вернет строку вида (Заявка № ID).
        """
        return f'Заявка №({self.pk})'


class Contract(models.Model):
    """
    Класс модели контракт.
    """
    customer = models.CharField(max_length=255)              # имя клиента для контракта
    text = models.TextField(default="Текст контракта...")
    cred_req = models.OneToOneField("CreditRequests",        # ссылка на заявку
                                    on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('contract')
        verbose_name_plural = _('contracts')
        ordering = ['pk']

    def __str__(self):
        """
        :return:
        Вернет строку вида (Контракт №(ID) | Клиент: (имя)).
        """
        return f'Контракт № {self.pk} | Клиент: ({self.customer})'
