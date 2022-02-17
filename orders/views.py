from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderItem , Order
from cart.cart import Cart
from django.urls import reverse

@login_required
def order_create(request):
    cart = Cart(request)
    if cart.is_empty():
        messages.error(request , 'سبد خرید شما خالیست')
        return redirect('/')
    order = Order(user=request.user , email=request.user.email)
    order.save()
    for item in cart:
        OrderItem.objects.create(order=order, course=item['course'], price=item['price'])
    cart.clear()
    request.session['order_id'] = order.id
    return redirect(reverse('zarinpal:request'))

