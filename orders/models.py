from django.db import models
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    email = models.EmailField(verbose_name='ایمیل')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False,verbose_name='پرداخت شده')

    class Meta:
        verbose_name='سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.price for item in self.items.all())
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE ,verbose_name='سفارش' )
    course = models.ForeignKey(Course, related_name='order_items', on_delete=models.CASCADE,verbose_name = 'دوره')
    price = models.PositiveIntegerField(verbose_name = 'قیمت')

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name='آیتم سفارش'
        verbose_name_plural = "آیتم های سفارش"
