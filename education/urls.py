from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('account/', include('allauth.urls')),
    path('accounts/' , include('users.urls')),
    path('',views.home,name="home"),
    path('contact-us/',views.contact_us,name='contact-us'),
    path('courses/',include('courses.urls')),
    path('cart/',include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('zarinpal/',include('zarinpal.urls',namespace='zarinpal')),
    path('captcha/', include('captcha.urls')),
    path('search/',views.search ,name='search'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
