from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('account/', include('allauth.urls')),
    path('accounts/' , include('users.urls')),
    path('',views.home,name="home"),
    path('blog/',include('blog.urls')),
    path('contact-us/',views.contact_us,name='contact-us'),
    path('courses/',include('courses.urls')),
    path('cart/',include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('zarinpal/',include('zarinpal.urls',namespace='zarinpal')),
    path('captcha/', include('captcha.urls')),
    path('search/',views.search ,name='search'),
    path('questions/', include('questions.urls')),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('openapi', get_schema_view(
          title="Codeyad Api",
          description="API for all things …",
          version="1.0.0"
      ), name='openapi-schema'),
    path('api/swagger-ui/', TemplateView.as_view(
          template_name='swagger-ui.html',
          extra_context={'schema_url': 'openapi-schema'}
      ), name='swagger-ui'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
