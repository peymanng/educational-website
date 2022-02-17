from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course
from django.contrib import messages
from django.urls import reverse
from .cart import Cart



def cart_add(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    if course.price == 0:
        messages.error(request , 'این دوره رایگان است')
        return redirect(reverse('course_detail',args=[course.slug]))
    cart.add(course=course)
    return redirect('cart_detail')


def cart_remove(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)

    return render(request, 'cart/detail.html',{'cart': cart})